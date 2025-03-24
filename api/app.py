import subprocess
import aioredis
from fastapi import FastAPI
from contextlib import asynccontextmanager

from starlette.datastructures import State

from api.handlers import router as main_router
from mcp_impl.client import MCPClient

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управляет жизненным циклом приложения
    """
    app.state = State()

    # Ждем запуск Redis
    try:
        redis = await aioredis.from_url("redis://localhost",
                                        decode_responses=True)
        await redis.ping()
    except Exception:
        subprocess.Popen(["redis-server"])

    while True:
        try:
            redis = await aioredis.from_url("redis://localhost",
                                            decode_responses=True)
            await redis.ping()
            break
        except Exception:
            pass

    app.state.redis = redis

    # Подключаем MCPClient
    client = MCPClient()
    await client.connect_to_server(server_script_path="./mcp_impl/server.py")
    app.state.client = client

    yield

    # Завершаем сессии redis и MCPClient
    await redis.close()
    await client.cleanup()


fastapi_app = FastAPI(lifespan=lifespan)
fastapi_app.include_router(main_router)
