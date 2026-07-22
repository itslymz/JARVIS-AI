"""Redis cache management."""

import json
from typing import Any, Optional

import redis.asyncio as aioredis

from app.config import settings

redis_client: Optional[aioredis.Redis] = None


async def init_cache() -> None:
    """Initialize Redis cache."""
    global redis_client
    try:
        redis_client = await aioredis.from_url(settings.REDIS_URL)
        # Test connection
        await redis_client.ping()
    except Exception as e:
        print(f"Redis connection failed: {e}")


async def get_cache(key: str) -> Optional[Any]:
    """Get value from cache."""
    if not redis_client:
        return None
    try:
        value = await redis_client.get(key)
        if value:
            return json.loads(value)
    except Exception as e:
        print(f"Cache get failed: {e}")
    return None


async def set_cache(key: str, value: Any, expire: int = 3600) -> bool:
    """Set value in cache."""
    if not redis_client:
        return False
    try:
        await redis_client.setex(key, expire, json.dumps(value))
        return True
    except Exception as e:
        print(f"Cache set failed: {e}")
    return False


async def delete_cache(key: str) -> bool:
    """Delete value from cache."""
    if not redis_client:
        return False
    try:
        await redis_client.delete(key)
        return True
    except Exception as e:
        print(f"Cache delete failed: {e}")
    return False


async def flush_cache() -> bool:
    """Flush all cache."""
    if not redis_client:
        return False
    try:
        await redis_client.flushdb()
        return True
    except Exception as e:
        print(f"Cache flush failed: {e}")
    return False
