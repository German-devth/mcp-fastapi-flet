import json
from functools import wraps

from api.redis_cache import cache_data, get_cached_data

def redis_cache(expire):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            redis = kwargs.get("redis")
            if redis is None:
                raise ValueError("Redis instance is required for the caching decorator")
            filtered_kwargs = {k: v for k, v in kwargs.items() if k not in ("client", "redis")}
            cache_key = f"{func.__name__}:{filtered_kwargs}"
            cached_value = await get_cached_data(redis, cache_key)
            if cached_value is not None:
                return json.loads(cached_value)
            result = await func(*args, **kwargs)
            try:
                serializable_result = result.dict() if hasattr(result, "dict") else result
            except Exception:
                serializable_result = result
            await cache_data(redis, cache_key, expire, json.dumps(serializable_result))
            return result
        return wrapper
    return decorator
