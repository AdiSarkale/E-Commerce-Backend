import os
from redis.asyncio import Redis

cached =  Redis.from_url(
    os.getenv("REDIS_URL","redis://redis:6379"),
    decode_responses=True
    )
