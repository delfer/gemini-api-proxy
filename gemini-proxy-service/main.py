import os
import logging
from flask import Flask, request, Response, stream_with_context
import requests
from key_manager import select_best_key, update_key_stats, initialize_db, add_keys_from_env, remove_keys_from_env, get_sorted_keys, DATABASE_FILE
from web_interface import register_web_interface

app = Flask(__name__)

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
def proxy_gemini_api(subpath):
    logging.info(f"Получен запрос: {request.method} {request.url}")
    logging.debug(f"Заголовки запроса: {request.headers}")

    user_api_key = None
    key_location = None # To track where the key was found

    if request.headers.get('X-Goog-Api-Key'):
        user_api_key = request.headers.get('X-Goog-Api-Key')
        key_location = 'header_goog'
    elif request.headers.get('X-API-Key'):
        user_api_key = request.headers.get('X-API-Key')
        key_location = 'header_xapi'
    elif request.args.get('key'):
        user_api_key = request.args.get('key')
        key_location = 'query'

    logging.info(f"Получен user_api_key: {user_api_key} из {key_location}")

    google_api_key = None

    def make_google_api_request(api_key, subpath, request, key_location):
        """Helper function to make the request to Google API."""
        google_api_url = f"https://generativelanguage.googleapis.com/v1beta/{subpath}"
        logging.debug(f"URL для запроса к Google API: {google_api_url}")

        headers = {key: value for key, value in request.headers if key.lower() not in ['host', 'x-api-key', 'x-goog-api-key']}
        params = request.args.copy()

        if 'key' in params:
            del params['key']

        if key_location == 'header_goog':
            headers['X-Goog-Api-Key'] = api_key
            logging.debug("Ключ добавлен в заголовок X-Goog-Api-Key для запроса к Google API")
        elif key_location == 'header_xapi':
             headers['X-API-Key'] = api_key
             logging.debug("Ключ добавлен в заголовок X-API-Key для запроса к Google API")
        else: # query
            params['key'] = api_key
            logging.debug("Ключ добавлен в параметры запроса к Google API")

        logging.debug(f"Заголовки запроса к Google API: {headers}")
        logging.debug(f"Параметры запроса к Google API: {params}")

        try:
            is_streaming = request.headers.get('Accept') == 'text/event-stream' or request.args.get('alt') == 'sse' or 'streamGenerateContent' in subpath
            logging.info(f"Обработка {'стримингового' if is_streaming else 'обычного'} запроса")

            req = requests.request(
                method=request.method,
                url=google_api_url,
                headers=headers,
                params=params,
                data=request.data,
                stream=is_streaming # Set stream based on the condition
            )
            req.raise_for_status()
            logging.info(f"Получен ответ от Google API ({'стриминг' if is_streaming else 'обычный'}): {req.status_code}")

            response_headers = dict(req.headers)
            if 'Transfer-Encoding' in response_headers:
                del response_headers['Transfer-Encoding']

            if is_streaming:
                def generate():
                    for chunk in req.iter_content(chunk_size=8192):
                        yield chunk
                return Response(stream_with_context(generate()), headers=response_headers), True # Return response and success status
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

            current_key = available_keys[current_key_index]

            logging.info(f"Попытка {attempts + 1}/{max_attempts} с Google API ключом из БД: {current_key}")
            response, success = make_google_api_request(current_key, subpath, request, key_location)
            update_key_stats(current_key, success=success)

            if success:
                logging.info(f"Успешный запрос с ключом: {current_key}")
                return response
            else:
                last_exception = response.data.decode('utf-8') # Capture the error message
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

        response, success = make_google_api_request(google_api_key, subpath, request, key_location)
        update_key_stats(google_api_key, success=success)
        return response

    else:
        logging.warning("API ключ отсутствует")
        return Response("API key is missing", status=401)


if __name__ == '__main__':
    # Для запуска в продакшене следует использовать более надежный сервер, например Gunicorn
    app.run(debug=True, host='0.0.0.0', port=5001)