import os

import uvicorn
from dotenv import load_dotenv


class UvicornServer:
    """
    Класс для запуска Uvicorn сервера (инкапсулирует логику запуска FastAPI)
    """

    def __init__(self, app: str, host: str, port: int):
        """
        Инициализация сервера

        :param app:
            Имя приложения FastAPI
        :param host:
            Хост для запуска сервера (например, 'localhost')
        :param port:
            Порт для запуска сервера
        """
        self.app = app
        self.host = host
        self.port = port

    def start(self) -> None:
        uvicorn.run(
            app=self.app,
            host=self.host,
            port=self.port,
            reload=True
        )


def create_uvicorn_server() -> UvicornServer:
    """
    Создание экземпляра UvicornServer с параметрами, загруженными из .env

    :return:
        Экземпляр класса UvicornServer
    """
    load_dotenv()
    app = os.getenv("APP")
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))

    return UvicornServer(app=app, host=host, port=port)
