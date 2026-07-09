from core.cache import get_cache

class CacheManager:

    @staticmethod
    async def get(key):
        return await get_cache().get(key)

    @staticmethod
    async def set(key, value, ttl=300):
        await get_cache().set(key, value, ex=ttl)

    @staticmethod
    async def delete(key):
        await get_cache().delete(key)

