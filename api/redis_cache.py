from typing import Optional

async def cache_data(redis, key: str, expire: int, value: str) -> None:
    """
    Кэширует данные в Redis с заданным ключом, временем истечения и значением
    Args:
         redis:
            Экземпляр Redis для работы с кэшем
         key:
            Ключ для сохранения данных
         expire:
            Время жизни кэша
         value:
            Значение для сохранения
    Returns:
         None
    """
    await redis.setex(key, expire, value)


async def get_cached_data(redis, key: str) -> Optional[str]:
    """
    Получает кэшированные данные по заданному ключу
    Args:
         redis:
            Экземпляр Redis для работы с кэшем
         key:
            Ключ для получения данных в виде строки
    Returns:
         Значение кэша в виде строки или None если данные не найдены
    """
    return await redis.get(key)
