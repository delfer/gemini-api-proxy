import os
import logging
import codecs
from quart import Quart, request, Response
import requests
import asyncio
from key_manager import select_best_key, update_key_stats, initialize_db, add_keys_from_env, remove_keys_from_env, get_sorted_keys, DATABASE_FILE
from web_interface import register_web_interface

app = Quart(__name__, template_folder='.')

# Register web interface routes and filters
register_web_interface(app)

# Initial database setup and key loading
initialize_db()
add_keys_from_env()
remove_keys_from_env()

# http://localhost:5001
# Настройка логирования
log_level = os.environ.get('LOG_LEVEL', 'DEBUG').upper()
log_levels = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}
logging.basicConfig(level=log_levels.get(log_level, logging.DEBUG), format='%(asctime)s - %(levelname)s - %(message)s')

# Получение ключей из переменных окружения
USER_KEYS = [key.strip() for key in os.environ.get("USER_KEYS", "").split("|") if key.strip()]


@app.route('/v1beta/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE'])
async def proxy_gemini_api(subpath):
    logging.info(f"Получен запрос: {request.method} {request.url}")
    logging.debug(f"Заголовки запроса: {request.headers}")

    user_api_key = None
    key_location = None # To track where the key was found

    if request.headers.get('Authorization', '').startswith('Bearer '):
        user_api_key = request.headers.get('Authorization').split(' ')[1]
        key_location = 'header_bearer'
        logging.debug(f"API ключ найден в заголовке Authorization (Bearer)")
    elif request.headers.get('X-Goog-Api-Key'):
        user_api_key = request.headers.get('X-Goog-Api-Key')
        key_location = 'header_goog'
        logging.debug(f"API ключ найден в заголовке X-Goog-Api-Key")
    elif request.headers.get('X-API-Key'):
        user_api_key = request.headers.get('X-API-Key')
        key_location = 'header_xapi'
        logging.debug(f"API ключ найден в заголовке X-API-Key")
    elif request.args.get('key'):
        user_api_key = request.args.get('key')
        key_location = 'query'
        logging.debug(f"API ключ найден в параметрах запроса")

    logging.info(f"Получен user_api_key: {user_api_key} из {key_location}")

    google_api_key = None

    async def make_google_api_request(api_key, subpath, request, key_location):
        """Helper function to make the request to Google API."""
        google_api_url = f"https://generativelanguage.googleapis.com/v1beta/{subpath}"
        logging.debug(f"URL для запроса к Google API: {google_api_url}")

        # Удаляем заголовки, которые могут вызвать проблемы или не нужны для проксирования, включая Remote-Addr
        # Восстанавливаем Accept-Encoding для корректной работы сжатия
        # Удаляем заголовки, которые могут вызвать проблемы или не нужны для проксирования, включая Remote-Addr и Authorization
        # Восстанавливаем Accept-Encoding для корректной работы сжатия
        headers = {key: value for key, value in request.headers if key.lower() not in ['host', 'x-api-key', 'x-goog-api-key', 'remote-addr', 'authorization']}
        params = request.args.copy()

        if 'key' in params:
            del params['key']

        if key_location == 'header_bearer' or key_location == 'query':
            params['key'] = api_key
            logging.debug("Ключ добавлен в параметры запроса к Google API")
        elif key_location == 'header_goog':
            headers['X-Goog-Api-Key'] = api_key
            logging.debug("Ключ добавлен в заголовок X-Goog-Api-Key для запроса к Google API")
        elif key_location == 'header_xapi':
             headers['X-API-Key'] = api_key
             logging.debug("Ключ добавлен в заголовок X-API-Key для запроса к Google API")

        logging.debug(f"Заголовки запроса к Google API: {headers}")
        logging.debug(f"Параметры запроса к Google API: {params}")

        try:
            is_streaming = request.headers.get('Accept') == 'text/event-stream' or request.args.get('alt') == 'sse' or 'streamGenerateContent' in subpath
            logging.info(f"Обработка {'стримингового' if is_streaming else 'обычного'} запроса")

            # Await request.data before passing it to the synchronous requests call
            request_data = await request.data

            # Use asyncio.to_thread for the synchronous requests call
            req = await asyncio.to_thread(
                requests.request,
                method=request.method,
                url=google_api_url,
                headers=headers,
                params=params,
                data=request_data, # Pass the awaited data
                stream=is_streaming # Set stream based on the condition
            )
            req.raise_for_status()
            logging.info(f"Получен ответ от Google API ({'стриминг' if is_streaming else 'обычный'}): {req.status_code}")

            response_headers = dict(req.headers)
            if 'Transfer-Encoding' in response_headers:
                del response_headers['Transfer-Encoding']
            if 'Content-Encoding' in response_headers:
                del response_headers['Content-Encoding']

            if is_streaming:
                # Для текстового стриминга (SSE, streamGenerateContent) ожидаем UTF-8.
                # Устанавливаем req.encoding, чтобы requests.iter_content(decode_unicode=True) работал корректно.
                if req.encoding is None or req.encoding.lower() != 'utf-8':
                    logging.debug(f"Original req.encoding for streaming: '{req.encoding}'. Forcing to 'utf-8'.")
                    req.encoding = 'utf-8'
                else:
                    logging.debug(f"Using req.encoding for streaming: '{req.encoding}'.")

                async def generate():
                    decoder = codecs.getincrementaldecoder('utf-8')(errors='replace') # Возвращаем 'replace' для большей устойчивости
                    # Use asyncio.to_thread for iter_content as well
                    for i, byte_chunk in enumerate(await asyncio.to_thread(req.iter_content, chunk_size=1024, decode_unicode=False)): # Получаем сырые байты
                         logging.debug(f"Streaming byte_chunk {i}: type={type(byte_chunk)}, len={len(byte_chunk)}, content[:100]='{byte_chunk[:100]}'")
                         try:
                             # Декодируем инкрементально. final=False важно для стриминга.
                             str_chunk = decoder.decode(byte_chunk, final=False)
                             if str_chunk: # Отдаем только если есть результат декодирования
                                 logging.debug(f"Manually decoded str_chunk {i} (replace): type={type(str_chunk)}, len={len(str_chunk)}, content[:100]='{str_chunk[:100]}'")
                                 yield str_chunk
                         except UnicodeDecodeError as e: # Эта ветка теперь менее вероятна с 'replace', но оставим для полноты
                             logging.error(f"REPLACE UnicodeDecodeError in manual decode for chunk {i}: {e}. Input bytes: {byte_chunk[:200]}")
                             # 'replace' должен был справиться, но если ошибка все же возникла, логируем и продолжаем
                             yield f"ERROR_REPLACE_DECODING_CHUNK_{i}\n"
                             continue
                    # После цикла, декодируем все оставшиеся байты в буфере декодера
                    try:
                         str_chunk_final = decoder.decode(b'', final=True)
                         if str_chunk_final:
                             logging.debug(f"Final manually decoded str_chunk (replace): type={type(str_chunk_final)}, len={len(str_chunk_final)}, content[:100]='{str_chunk_final[:100]}'")
                             yield str_chunk_final
                    except UnicodeDecodeError as e: # Аналогично, менее вероятна
                         logging.error(f"REPLACE UnicodeDecodeError in final manual decode: {e}")
                         yield "ERROR_REPLACE_DECODING_FINAL_CHUNK\n"

                # Обновляем Content-Type в заголовках ответа, чтобы он точно был UTF-8.
                # Quart Response будет использовать это для кодирования строк из generate() обратно в байты.
                # Условие is_streaming уже предполагает текстовый поток (SSE/streamGenerateContent).
                response_headers['Content-Type'] = 'text/event-stream; charset=utf-8'

                # Content-Length не применим для потоковых ответов и может вызвать проблемы
                if 'Content-Length' in response_headers:
                    del response_headers['Content-Length']

                return Response(generate(), headers=response_headers), True # Return response and success status
            else:
                return Response(req.content, status=req.status_code, headers=response_headers), True # Return response and success status

        except requests.exceptions.RequestException as e:
            logging.error(f"Ошибка при запросе к Google API с ключом {api_key}: {e}")
            # Attempt to get a more specific error message from the response if available
            error_message = str(e)
            if e.response is not None:
                 try:
                     error_message = e.response.text
                 except:
                     pass # Ignore if response text is not accessible

            return Response(error_message, status=e.response.status_code if e.response is not None else 500), False # Return error response and failure status


    if user_api_key in USER_KEYS:
        available_keys = get_sorted_keys()

        if not available_keys:
            logging.warning("Нет доступных Google API ключей в БД.")
            return Response("No available Google API keys", status=500)

        current_key_index = 0
        current_key_usage_count = 0

        last_exception = None
        attempts = 0
        max_attempts = len(available_keys) * 2 # Allow 2 attempts per key

        while attempts < max_attempts:
            # Ensure index is within bounds (in case keys were removed or list changed)
            if current_key_index >= len(available_keys):
                current_key_index = 0
                current_key_usage_count = 0 # Reset usage count when wrapping around

            if not available_keys: # Check if available_keys became empty during attempts
                 logging.error("Все доступные Google API ключи исчерпаны или не работают после всех попыток.")
                 return Response(last_exception if last_exception else "No available Google API keys", status=500)

            current_key = available_keys[current_key_index]

            logging.info(f"Попытка {attempts + 1}/{max_attempts} с Google API ключом из БД: {current_key}")
            response, success = await make_google_api_request(current_key, subpath, request, key_location) # Await the async function
            update_key_stats(current_key, success=success)

            if success:
                logging.info(f"Успешный запрос с ключом: {current_key}")
                return response
            else:
                last_exception_bytes = await response.data # Capture the error message bytes
                last_exception = last_exception_bytes.decode('utf-8') # Decode the bytes
                logging.warning(f"Неудачный запрос с ключом {current_key}. Ошибка: {last_exception}")

                current_key_usage_count += 1
                if current_key_usage_count >= 2:
                    current_key_index += 1
                    current_key_usage_count = 0 # Reset usage count for the next key
            attempts += 1

        logging.error("Все доступные Google API ключи исчерпаны или не работают после всех попыток.")
        return Response(last_exception, status=500)

    elif user_api_key:
        google_api_key = user_api_key
        logging.info(f"Используется user_api_key как Google API ключ: {google_api_key}")

        if not google_api_key:
            logging.warning("API ключ отсутствует")
            return Response("API key is missing", status=401)

        response, success = await make_google_api_request(google_api_key, subpath, request, key_location) # Await the async function
        update_key_stats(google_api_key, success=success)
        return response

    else:
        logging.warning("API ключ отсутствует")
        return Response("API key is missing", status=401)
