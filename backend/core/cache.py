from redis.asyncio import Redis
import os

_cached = None

def get_cache() -> Redis:
    global _cached

    if _cached is None:
        _cached = Redis.from_url(
            os.getenv(
                "REDIS_URL",
                "redis://redis:6379/0"
            ),
            decode_responses=True,
        )

    return _cached


def get_redis():
    return get_cache()
