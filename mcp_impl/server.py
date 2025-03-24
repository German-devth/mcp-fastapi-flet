import logging
from typing import Optional, List, Dict, Any

import data_fetchers
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.DEBUG)
mcp = FastMCP("MCP-FastAPI")


@mcp.resource("exchange://{currency}")
async def get_exchange_rate(currency: str = "USD") -> Optional[str]:
    """
    Получает курс обмена для заданной валюты
    Args:
        currency:
            Код валюты в виде строки (по умолчанию USD)
    Returns:
        Курс обмена в виде строки или None если данные недоступны
    """
    return data_fetchers.get_exchange(currency)


@mcp.resource("news://{city}")
async def get_news(city: str) -> List[str]:
    """
    Получает новости для заданного города
    Args:
        city:
            Название города в виде строки
    Returns:
        Список заголовков новостей в виде строк
    """
    return data_fetchers.get_news(city)


@mcp.resource("weather://{city}")
async def get_weather(city: str) -> Dict[str, Any]:
    """
    Получает данные о погоде для заданного города
    Args:
        city:
            Название города в виде строки
    Returns:
        Словарь с информацией о погоде
    """
    return data_fetchers.get_weather(city)


if __name__ == '__main__':
    mcp.run(transport="stdio")
