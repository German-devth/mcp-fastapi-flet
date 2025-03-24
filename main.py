import asyncio

from uvicorn_impl.uvicorn_server import create_uvicorn_server


async def main():
    create_uvicorn_server().start()

if __name__ == "__main__":
    asyncio.run(main())