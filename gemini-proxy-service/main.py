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
GOOGLE_KEYS = [key.strip() for key in os.environ.get("GOOGLE_KEYS", "").split("|") if key.strip()]


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
    if user_api_key in USER_KEYS:
        # Используем логику выбора ключа из key_manager
        available_keys = get_sorted_keys()
        if not available_keys:
            logging.warning("Нет доступных Google API ключей в БД.")
            return Response("No available Google API keys", status=500)

        last_exception = None
        for current_key in available_keys:
            logging.info(f"Попытка с Google API ключом из БД: {current_key}")

            # Формирование URL для запроса к Google API
            google_api_url = f"https://generativelanguage.googleapis.com/v1beta/{subpath}"
            logging.debug(f"URL для запроса к Google API: {google_api_url}")

            # Подготовка заголовков и параметров запроса для текущей попытки
            # Remove potential incoming key headers to avoid duplication
            headers = {key: value for key, value in request.headers if key.lower() not in ['host', 'x-api-key', 'x-goog-api-key']}

            params = request.args.copy()
            # Remove potential incoming key query param
            if 'key' in params:
                del params['key']

            # Add the key back based on where it was received
            if key_location == 'header_goog':
                headers['X-Goog-Api-Key'] = current_key
                logging.debug("Ключ добавлен в заголовок X-Goog-Api-Key для запроса к Google API")
            elif key_location == 'header_xapi':
                 headers['X-API-Key'] = current_key
                 logging.debug("Ключ добавлен в заголовок X-API-Key для запроса к Google API")
            else: # query
                params['key'] = current_key
                logging.debug("Ключ добавлен в параметры запроса к Google API")

            logging.debug(f"Заголовки запроса к Google API: {headers}")
            logging.debug(f"Параметры запроса к Google API: {params}")

            try:
                # Обработка стриминга
                if request.headers.get('Accept') == 'text/event-stream' or request.args.get('alt') == 'sse' or 'streamGenerateContent' in subpath:
                    logging.info("Обработка стримингового запроса")
                    req = requests.request(
                        method=request.method,
                        url=google_api_url,
                        headers=headers,
                        params=params,
                        data=request.data,
                        stream=True
                    )
                    req.raise_for_status()
                    logging.info(f"Получен ответ от Google API (стриминг): {req.status_code}")
                    update_key_stats(current_key, success=True)

                    def generate():
                        for chunk in req.iter_content(chunk_size=8192):
                            yield chunk

                    response_headers = dict(req.headers)
                    if 'Transfer-Encoding' in response_headers:
                        del response_headers['Transfer-Encoding']
                    return Response(stream_with_context(generate()), headers=response_headers)
                else:
                    logging.info("Обработка обычного запроса")
                    req = requests.request(
                        method=request.method,
                        url=google_api_url,
                        headers=headers,
                        params=params,
                        data=request.data
                    )
                    req.raise_for_status()
                    logging.info(f"Получен ответ от Google API: {req.status_code}")
                    update_key_stats(current_key, success=True)

                    response_headers = dict(req.headers)
                    # Удаляем заголовок Transfer-Encoding, так как requests уже декодировал ответ
                    if 'Transfer-Encoding' in response_headers:
                        del response_headers['Transfer-Encoding']
                    return Response(req.content, status=req.status_code, headers=response_headers)

            except requests.exceptions.RequestException as e:
                logging.error(f"Ошибка при запросе к Google API с ключом {current_key}: {e}")
                last_exception = e
                update_key_stats(current_key, success=False)
                # Продолжаем цикл, чтобы попробовать следующий ключ

        # Если цикл завершился (все ключи перепробованы) и не было успешного ответа
        logging.error("Все доступные Google API ключи исчерпаны или не работают.")
        return Response(str(last_exception), status=500)

    elif user_api_key:
        google_api_key = user_api_key
        logging.info(f"Используется user_api_key как Google API ключ: {google_api_key}")

        if not google_api_key:
            logging.warning("API ключ отсутствует")
            return Response("API key is missing", status=401)

        # Формирование URL для запроса к Google API
        google_api_url = f"https://generativelanguage.googleapis.com/v1beta/{subpath}"
        logging.debug(f"URL для запроса к Google API: {google_api_url}")

        # Подготовка заголовков и параметров запроса
        # Remove potential incoming key headers to avoid duplication
        headers = {key: value for key, value in request.headers if key.lower() not in ['host', 'x-api-key', 'x-goog-api-key']}

        params = request.args.copy()
        # Remove potential incoming key query param
        if 'key' in params:
            del params['key']

        # Add the key back based on where it was received
        if key_location == 'header_goog':
            headers['X-Goog-Api-Key'] = google_api_key
            logging.debug("Ключ добавлен в заголовок X-Goog-Api-Key для запроса к Google API")
        elif key_location == 'header_xapi':
             headers['X-API-Key'] = google_api_key
             logging.debug("Ключ добавлен в заголовок X-API-Key для запроса к Google API")
        else: # query
            params['key'] = google_api_key
            logging.debug("Ключ добавлен в параметры запроса к Google API")


        logging.debug(f"Заголовки запроса к Google API: {headers}")
        logging.debug(f"Параметры запроса к Google API: {params}")

        try:
            # Обработка стриминга
            if request.headers.get('Accept') == 'text/event-stream' or request.args.get('alt') == 'sse' or 'streamGenerateContent' in subpath:
                logging.info("Обработка стримингового запроса")
                req = requests.request(
                    method=request.method,
                    url=google_api_url,
                    headers=headers,
                    params=params,
                    data=request.data,
                    stream=True
                )
                req.raise_for_status()
                logging.info(f"Получен ответ от Google API (стриминг): {req.status_code}")

                def generate():
                    for chunk in req.iter_content(chunk_size=8192):
                        yield chunk

                response_headers = dict(req.headers)
                if 'Transfer-Encoding' in response_headers:
                    del response_headers['Transfer-Encoding']
                update_key_stats(google_api_key, success=True) # Обновление метрик для успешного стримингового запроса
                return Response(stream_with_context(generate()), headers=response_headers)
            else:
                logging.info("Обработка обычного запроса")
                req = requests.request(
                    method=request.method,
                    url=google_api_url,
                    headers=headers,
                    params=params,
                    data=request.data
                )
                req.raise_for_status()
                logging.info(f"Получен ответ от Google API: {req.status_code}")
                response_headers = dict(req.headers)
                # Удаляем заголовок Transfer-Encoding, так как requests уже декодировал ответ
                if 'Transfer-Encoding' in response_headers:
                    del response_headers['Transfer-Encoding']
                update_key_stats(google_api_key, success=True) # Обновление метрик для успешного запроса
                return Response(req.content, status=req.status_code, headers=response_headers)

        except requests.exceptions.RequestException as e:
            logging.error(f"Ошибка при запросе к Google API: {e}")
            update_key_stats(google_api_key, success=False) # Обновление метрик для ошибочного запроса
            return Response(str(e), status=500)

    else:
        logging.warning("API ключ отсутствует")
        return Response("API key is missing", status=401)


if __name__ == '__main__':
    # Для запуска в продакшене следует использовать более надежный сервер, например Gunicorn
    app.run(debug=True, host='0.0.0.0', port=5001)