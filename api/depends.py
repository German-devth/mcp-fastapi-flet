from starlette.requests import Request
from typing import Any

async def get_mcp_client(request: Request) -> Any:
    """
    Возвращает экземпляр клиента MCP из состояния приложения
    Args:
         request:
            Объект запроса
    Returns:
         Клиент MCP, сохранённый в состоянии приложения
    """
    return request.app.state.client

async def get_redis(request: Request) -> Any:
    """
    Возвращает экземпляр Redis из состояния приложения
    Args:
         request:
            Объект запроса
    Returns:
         Соединение Redis, сохранённое в состоянии приложения
    """
    return request.app.state.redis
