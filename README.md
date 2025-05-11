# gemini-api-proxy

A proxy service for the Google Gemini API with key management and a web interface.

## Description

This project provides a simple proxy service for the Google Gemini API. It allows you to manage multiple Google API keys, automatically rotating between them based on usage statistics (successful and error requests). It also includes a basic web interface for viewing and managing the API keys stored in an SQLite database.

The proxy accepts requests with a user-defined API key (checked against `USER_KEYS`) and forwards them to the Google Gemini API using one of the configured Google API keys. This is useful for scenarios where you need to pool multiple API keys or add an extra layer of access control.

## Features

*   **API Key Management:** Store and manage multiple Google API keys in an SQLite database.
*   **Automatic Key Rotation:** Automatically selects the "best" available Google API key based on recent success/error rates.
*   **Web Interface:** A basic web interface (`/admin/keys`) to view key statistics, enable/disable keys, and add new keys.
*   **Basic Authentication:** Protects the web interface using Basic Auth against configured `USER_KEYS`.
*   **Proxying:** Forwards requests to the Google Gemini API (`/v1beta/*`).
*   **Streaming Support:** Handles streaming responses from the Gemini API.
*   **Docker Support:** Easily deployable using Docker Compose.
*   **Systemd Service Files:** Includes example systemd service files for running the proxy and Traefik.

## Installation

### Using Docker Compose

The easiest way to run the proxy is using Docker Compose.

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-repo/gemini-api-proxy.git
    cd gemini-api-proxy
    ```
    (Replace `https://github.com/your-repo/gemini-api-proxy.git` with the actual repository URL)

2.  Create a `.env` file in the project root with your API keys:
    ```env
    USER_KEYS="your_user_key_1|your_user_key_2"
    GOOGLE_KEYS="your_google_key_1|your_google_key_2"
    # Optional: Specify keys to remove on startup (e.g., if you removed them from GOOGLE_KEYS)
    # REMOVE_GOOGLE_KEYS="key_to_remove_1|key_to_remove_2"
    # Optional: Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    # LOG_LEVEL="INFO"
    ```
    *   `USER_KEYS`: A pipe-separated list of keys that your users will include in their requests to the proxy. These are used for basic authentication to the web interface.
    *   `GOOGLE_KEYS`: A pipe-separated list of your actual Google API keys. These will be added to the internal database on startup.
    *   `REMOVE_GOOGLE_KEYS`: (Optional) A pipe-separated list of keys to mark as removed in the database on startup. Useful if you've removed keys from `GOOGLE_KEYS` and want to disable them in the database.
    *   `LOG_LEVEL`: (Optional) Sets the logging level for the proxy service. Defaults to `DEBUG`.

3.  Build and run the Docker containers:
    ```bash
    docker-compose up --build -d
    ```

The proxy service will be running on `http://localhost:5001`.

### Using Systemd (Advanced)

Example systemd service files (`systemd-services/gemini-proxy.service` and `systemd-services/traefik.service`) are provided for running the service directly on a Linux system, potentially with Traefik as a reverse proxy. Refer to these files for configuration details if you choose this method.

## Configuration

Configuration is primarily done via environment variables, especially when using Docker Compose.

*   `USER_KEYS`: (Required) Pipe-separated list of user API keys for proxy access and web interface authentication.
*   `GOOGLE_KEYS`: (Required) Pipe-separated list of Google API keys to be managed by the proxy. These are added to the internal database on startup.
*   `REMOVE_GOOGLE_KEYS`: (Optional) Pipe-separated list of Google API keys to be marked as removed in the database on startup.
*   `LOG_LEVEL`: (Optional) Sets the logging level for the proxy service (DEBUG, INFO, WARNING, ERROR, CRITICAL). Defaults to `DEBUG`.

The proxy uses an SQLite database file named `keys.db` to store key statistics. This file will be created in the service's working directory.

## Web Interface

A web interface is available at `/admin/keys` (e.g., `http://localhost:5001/admin/keys`). You will be prompted for basic authentication. Use any of the keys specified in the `USER_KEYS` environment variable as the password (the username can be anything).

The web interface allows you to:
*   View all managed Google API keys and their statistics (successful requests, error requests, etc.).
*   Sort the key list by different columns.
*   Enable or disable individual keys. Disabled keys will not be used by the proxy.
*   Add new Google API keys to the database.

## Usage

To use the proxy, send your requests to the proxy service URL (`http://localhost:5001` by default) instead of the direct Google API endpoint. Include one of your `USER_KEYS` in the request, either in the `X-Goog-Api-Key` header, `X-API-Key` header, or as a query parameter `key`.

The proxy will then forward the request to the Google Gemini API using one of the configured `GOOGLE_KEYS`.

Example using `curl`:

```bash
curl -X POST \
  http://localhost:5001/v1beta/models/gemini-pro:generateContent \
  -H 'X-API-Key: your_user_key_1' \
  -H 'Content-Type: application/json' \
  -d '{
    "contents": [
      {"parts":[{"text":"Write a short story about a cat."}]}
    ]
  }'
```

Replace `your_user_key_1` with one of the keys from your `USER_KEYS` environment variable.

## API Reference

This project is designed to proxy requests to the Google Gemini API. For detailed information on the available API endpoints and request/response formats, refer to the following documents:

*   [Gemini API Video Understanding](gemini-api-reference/gemini-api_video.md)
*   [Gemini Audio](gemini-api-reference/gemini-audio.md)
*   [Gemini Code Execution](gemini-api-reference/gemini-code-execution.md)
*   [Gemini Document Processing](gemini-api-reference/gemini-document-processing.md)
*   [Gemini Function Calling](gemini-api-reference/gemini-function-calling.md)
*   [Gemini Grounding Search Suggestions](gemini-api-reference/gemini-grounding-search-suggestions.md)
*   [Gemini Grounding](gemini-api-reference/gemini-grounding.md)
*   [Gemini Image Generation](gemini-api-reference/gemini-image-generation.md)
*   [Gemini Image Understanding](gemini-api-reference/gemini-image-understanding.md)
*   [Gemini Long Context](gemini-api-reference/gemini-long-context.md)
*   [Gemini Structured Output](gemini-api-reference/gemini-structured-output.md)
*   [Gemini Text Generation](gemini-api-reference/gemini-text-generation.md)
*   [Gemini Thinking](gemini-api-reference/gemini-thinking.md)
*   [Gemini Video Understanding](gemini-api-reference/gemini-video-understanding.md)

These documents provide examples and details on how to interact with different Gemini API capabilities through the proxy.

## License

[Specify your project's license here, e.g., MIT, Apache 2.0, etc.]

---

# gemini-api-proxy

Прокси-сервис для Google Gemini API с управлением ключами и веб-интерфейсом.

## Описание

Этот проект предоставляет простой прокси-сервис для Google Gemini API. Он позволяет управлять несколькими ключами Google API, автоматически ротируя их на основе статистики использования (успешные и ошибочные запросы). Он также включает базовый веб-интерфейс для просмотра и управления ключами API, хранящимися в базе данных SQLite.

Прокси принимает запросы с пользовател��ским API ключом (проверяется по списку `USER_KEYS`) и перенаправляет их в Google Gemini API, используя один из настроенных ключей Google API. Это полезно в сценариях, когда вам нужно объединить несколько ключей API или добавить дополнительный уровень контроля доступа.

## Возможности

*   **Управление ключами API:** Хранение и управление несколькими ключами Google API в базе данных SQLite.
*   **Автоматическая ротация ключей:** Автоматический выбор "лучшего" доступного ключа Google API на основе недавней статистики успешных запросов и ошибок.
*   **Веб-интерфейс:** Базовый веб-интерфейс (`/admin/keys`) для просмотра статистики ключей, включения/отключения ключей и добавления новых ключей.
*   **Базовая аутентификация:** Защита веб-интерфейса с использованием Basic Auth по настроенным `USER_KEYS`.
*   **Проксирование:** Перенаправление запросов в Google Gemini API (`/v1beta/*`).
*   **Поддержка стриминга:** Обработка стриминговых ответов от Gemini API.
*   **Поддержка Docker:** Легко развертывается с использованием Docker Compose.
*   **Файлы сервисов Systemd:** Включает примеры файлов сервисов systemd для запуска прокси и Traefik.

## Установка

### Использование Docker Compose

Самый простой способ запустить прокси - использовать Docker Compose.

1.  Клонируйте репозиторий:
    ```bash
    git clone https://github.com/your-repo/gemini-api-proxy.git
    cd gemini-api-proxy
    ```
    (Замените `https://github.com/your-repo/gemini-api-proxy.git` на фактический URL репозитория)

2.  Создайте файл `.env` в корне проекта с вашими ключами API:
    ```env
    USER_KEYS="ваш_пользовательский_ключ_1|ваш_пользовательский_ключ_2"
    GOOGLE_KEYS="ваш_ключ_google_1|ваш_ключ_google_2"
    # Опционально: Укажите ключи для удаления при запуске (например, если вы удалили их из GOOGLE_KEYS)
    # REMOVE_GOOGLE_KEYS="ключ_для_удаления_1|ключ_для_удаления_2"
    # Опционально: Установите уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    # LOG_LEVEL="INFO"
    ```
    *   `USER_KEYS`: Список пользовательских ключей API, разделенных символом `|`, которые ваши пользователи будут включать в свои запросы к прокси. Они используются для базовой аутентификации в веб-интерфейсе.
    *   `GOOGLE_KEYS`: Список ваших фактических ключей Google API, разделенных символом `|`. Они будут добавлены во внутреннюю базу данных при запуске.
    *   `REMOVE_GOOGLE_KEYS`: (Опционально) Список ключей, разделенных символом `|`, которые нужно пометить как удаленные в базе данных при запуске. Полезно, если вы удалили ключи из `GOOGLE_KEYS` и хотите отключить их в базе данных.
    *   `LOG_LEVEL`: (Опционально) Устанавливает уровень логирования для прокси-сервиса. По умолчанию `DEBUG`.

3.  Соберите и запустите Docker контейнеры:
    ```bash
    docker-compose up --build -d
    ```

Прокси-сервис будет запущен на `http://localhost:5001`.

### Использование Systemd (Продвинутый вариант)

Примеры файлов сервисов systemd (`systemd-services/gemini-proxy.service` и `systemd-services/traefik.service`) предоставлены для запуска сервиса непосредственно в системе Linux, возможно, с Traefik в качестве обратного прокси. Обратитесь к этим файлам для получения подробностей конфигурации, если вы выберете этот метод.

## Конфигурация

Конфигурация в основном осуществляется через переменные окружения, особенно при использовании Docker Compose.

*   `USER_KEYS`: (Обязательно) Список пользовательских ключей API, разделенных символом `|`, для доступа к прокси и аутентификации в веб-интерфейсе.
*   `GOOGLE_KEYS`: (Обязательно) Список ключей Google API, разделенных символом `|`, которые будут управляться прокси. Они добавляются во внутреннюю базу данных при запуске.
*   `REMOVE_GOOGLE_KEYS`: (Опционально) Список ключей Google API, разделенных символом `|`, которые нужно пометить как удаленные в базе данных при запуске.
*   `LOG_LEVEL`: (Опционально) Устанавливает уровень логирования для прокси-сервиса (DEBUG, INFO, WARNING, ERROR, CRITICAL). По умолчанию `DEBUG`.

Прокси использует файл базы данных SQLite с именем `keys.db` для хранения статистики ключей. Этот файл будет создан в рабочей директории сервиса.

## Веб-интерфейс

Веб-интерфейс доступен по адресу `/admin/keys` (например, `http://localhost:5001/admin/keys`). Вам будет предложено пройти базовую аутентификацию. Используйте любой из ключей, указанных в переменной окружения `USER_KEYS`, в качестве пароля (имя пользователя может быть любым).

Веб-интерфейс позволяет:
*   Просматривать все управляемые ключи Google API и их статистику (успешные запросы, ошибочные запросы и т.д.).
*   Сортировать список ключей по различным столбцам.
*   Включать или отключать отдельные ключи. Отключенные ключи не будут использоваться прокси.
*   Добавлять новые ключи Google API в базу данных.

## Использование

Чтобы использовать прокси, отправляйте свои запросы на URL прокси-сервиса (по умолчанию `http://localhost:5001`) вместо прямого адреса Google API. Включите один из ваших `USER_KEYS` в запрос, либо в заголов��к `X-Goog-Api-Key`, заголовок `X-API-Key`, либо как параметр запроса `key`.

Затем прокси перенаправит запрос в Google Gemini API, используя один из настроенных `GOOGLE_KEYS`.

Пример использования `curl`:

```bash
curl -X POST \
  http://localhost:5001/v1beta/models/gemini-pro:generateContent \
  -H 'X-API-Key: ваш_пользовательский_ключ_1' \
  -H 'Content-Type: application/json' \
  -d '{
    "contents": [
      {"parts":[{"text":"Напишите короткий рассказ о кошке."}]}
    ]
  }'
```

Замените `ваш_пользовательский_ключ_1` на один из ключей из вашей переменной окружения `USER_KEYS`.

## Справочник API

Этот проект предназначен для проксирования запросов к Google Gemini API. Подробную информацию о доступных конечных точках API и форматах запросов/ответов можно найти в следующих документах:

*   [Gemini API Video Understanding](gemini-api-reference/gemini-api_video.md)
*   [Gemini Audio](gemini-api-reference/gemini-audio.md)
*   [Gemini Code Execution](gemini-api-reference/gemini-code-execution.md)
*   [Gemini Document Processing](gemini-api-reference/gemini-document-processing.md)
*   [Gemini Function Calling](gemini-api-reference/gemini-function-calling.md)
*   [Gemini Grounding Search Suggestions](gemini-api-reference/gemini-grounding-search-suggestions.md)
*   [Gemini Grounding](gemini-api-reference/gemini-grounding.md)
*   [Gemini Image Generation](gemini-api-reference/gemini-image-generation.md)
*   [Gemini Image Understanding](gemini-api-reference/gemini-image-understanding.md)
*   [Gemini Long Context](gemini-api-reference/gemini-long-context.md)
*   [Gemini Structured Output](gemini-api-reference/gemini-structured-output.md)
*   [Gemini Text Generation](gemini-api-reference/gemini-text-generation.md)
*   [Gemini Thinking](gemini-api-reference/gemini-thinking.md)
*   [Gemini Video Understanding](gemini-api-reference/gemini-video-understanding.md)

Эти документы содержат примеры и подробности о том, как взаимодействовать с различными возможностями Gemini API через прокси.

## Лицензия

[Укажите лицензию вашего проекта здесь, например, MIT, Apache 2.0 и т.д.]