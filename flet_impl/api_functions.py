import httpx
from typing import Any

async def fetch_exchange(currency: str) -> Any:
    """
    Выполняет POST запрос для получения курса обмена
    Args:
         currency: Код валюты в виде строки
    Returns:
         Ответ httpx.Response
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:8000/exchange",
            data={"currency": currency}
        )
    return response

async def fetch_weather(city: str) -> Any:
    """
    Выполняет POST запрос для получения данных о погоде
    Args:
         city: Название города в виде строки
    Returns:
         Ответ httpx.Response
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:8000/weather",
            data={"city": city}
        )
    return response

async def fetch_news(city: str) -> Any:
    """
    Выполняет POST запрос для получения новостей
    Args:
         city: Название города в виде строки
    Returns:
         Ответ httpx.Response
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:8000/news",
            data={"city": city}
        )
    return response
