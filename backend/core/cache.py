from redis.asyncio import Redis
import os

cached = Redis.from_url(
    os.getenv(
        "REDIS_URL",
        "redis://redis:6379/0"
    ),
    decode_responses=True
)


def get_redis() -> Redis:
    return cached
