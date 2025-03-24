from contextlib import AsyncExitStack
from typing import Optional, Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClient:
    """
    Клиент MCP для установления соединения с сервером через stdio

    Этот класс управляет жизненным циклом соединения
    с сервером, используя асинхронный контекстный стек
    для автоматического закрытия ресурсов
    """

    def __init__(self) -> None:
        """
        Инициализирует экземпляр MCPClient.

        Атрибуты:
            session (Optional[ClientSession]):
                Сессия клиента для общения с сервером
            exit_stack (AsyncExitStack): А
                синхронный стек для управления ресурсами
            write:
                Канал записи данных в сервер
            stdio:
                Канал чтения данных от сервера
        """
        self.session: Optional[ClientSession] = None
        self.exit_stack: AsyncExitStack = AsyncExitStack()
        self.write = None
        self.stdio = None

    async def connect_to_server(self, server_script_path: str) -> None:
        """
        Устанавливает соединение с сервером MCP
        Запускает сервер с указанным скриптом и устанавливает клиентскую
        сессию для общения с ним

        Args:
            server_script_path (str):
                Путь к серверному скрипту, который нужно запустить

        Raises:
            Exception:
                Пробрасывает исключения, возникшие при установлении
                соединения или инициализации сессии
        """
        server_params: StdioServerParameters = StdioServerParameters(
            command="python",
            args=[server_script_path],
            env=None
        )
        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.stdio, self.write = stdio_transport

        # Создаем и инициализируем клиентскую сессию
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )
        await self.session.initialize()

    async def cleanup(self) -> None:
        """
        Завершает работу клиента и освобождает все занятые ресурсы
        Закрывает все контекстные менеджеры, зарегистрированные в exit_stack
        """
        await self.exit_stack.aclose()
