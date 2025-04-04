# MCP + FastAPI + Flet

## Описание

Проект представляет собой REST API на FastAPI, который взаимодействует с MCP сервисом, а также Flet приложением. Он включает в себя управление задачами через MCP - получение курса валюты, погоды и новостей в городе через API.

## Основные компоненты

- **FastAPI-приложение** (`api/app.py`) — создает экземпляр FastAPI и настраивает маршрутык.
- **Uvicorn-сервер** (`uvicorn_impl/uvicorn_server.py`) — запускает Uvicorn-сервер для FastAPI.
- **MCP-сервер** (`mcp_impl/server.py`) — осуществляет выполнение запросов к сторонним API.
- **MCP-клиент** (`mcp_impl/client.py`) — управляет соединением с MCP-сервером.
- **Flet-приложение** (`flet_impl/flet_app.py`) — запускает Flet-приложение в браузере для интерактивной работы пользователя.

## Установка
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/German-devth/mcp-fastapi-flet.git
   ```
2. Перейдите в папку с проектом:
   ```bash
   cd mcp-fastapi-flet
   ```
   
3. Создайте виртуальное окружение:
   ```bash
   python -m venv .venv
   ```
   либо
   ```bash
   python3 -m venv .venv
   ```
4. Активация виртуального окружения:
   ```bash
   source .venv/bin/activate  # Для Linux/macOS
   .venv\Scripts\activate  # Для Windows
   ```
5. Установите зависимости:
   ```bash
   pip install -r req.txt
   ```

## Настройка окружения

Создайте файл `.env` и укажите переменные окружения:

```ini
APP=app.fastapi_app:app
HOST=127.0.0.1
PORT=8000
WEATHER_API_KEY=
NEWS_API_KEY=
```

## Запуск MCP и FastAPI с Uvicorn


```bash
python main.py
```
либо
```bash
python3 main.py
```

### Перейти в браузере по адресу


```bash
http://127.0.0.1:8000/docs
```

## API Эндпоинты

### Получение информации о новостях в городе

```http
POST /news
```

### Получение курса обмена валют

```http
POST /exchange
```

### Получение текущего прогноза погоды в городе

```http
POST /weather
```

### Получение всех данных

```http
POST /full_data
```

## Запуск Flet-приложения*


```bash
python flet_app.py
```
либо
```bash
python3 flet_app.py
```
На запуск потребуется несколько секунд. Откроется окно браузера

\* Приложение полноценно работает при запущенном MCP и FastAPI с Uvicorn

## Кеширование

Ответы по курсу валюты и погоде кешируются с помощью Redis

