from core.cache import cached

class CacheManager:

    @staticmethod
    async def get(key: str):
        return await(cached.get(key))

    @staticmethod
    async def set(
        key: str,
        value: str,
        ttl: int = 300):

        await cached.set(
            key,
            value,
            ex=ttl)


    @staticmethod
    async def delete(key: str):
        await cached.delete(key)

