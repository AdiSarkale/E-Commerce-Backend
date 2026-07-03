from repository.address import AddressRepository
from sqlalchemy.ext.asyncio import AsyncSession
from schema.address import AddressCreate,AddressResponse, AddressUpdate
from utils.cache import CacheManager
import json


class AddressServices:

    @staticmethod
    async def create_address(db: AsyncSession, addr: AddressCreate, user_id: int):
        result = await AddressRepository.create_address(db,addr,user_id)
        addr = AddressResponse.model_validate(result)

        return addr


    @staticmethod
    async def get_addr(db: AsyncSession, user_id : int):
        cached_key = f"address:{user_id}"

        cached = await CacheManager.get(cached_key)
        if cached:
            return [AddressResponse.model_validate(cache) for cache in cached]
        result = await AddressRepository.get_user_addr(db,user_id)
        addr = [AddressResponse.model_validate(res) for res in result]
        cache_data = [
            item.model_dump(mode="json")
            for item in addr
                ]
        await CacheManager.set(
            cached_key,
            json.dumps(cache_data),
            ttl=300
            )
        return addr

    @staticmethod
    async def get_by_id(db: AsyncSession,user_id: int, addr_id: int):
        cached_key = f"address:{user_id}"

        cached = await CacheManager.get(cached_key)
        if cached:
            return AddressResponse.model_validate(cached)
        result = await AddressRepository.get_addr_by_id(db,user_id,addr_id)
        addr = AddressResponse.model_validate(result)
        await CacheManager.set(
            cached_key,
            addr.model_dump_json(),
            ttl=300
            )

        return addr

    @staticmethod
    async def update_addr(db:AsyncSession,user_id: int, addr: AddressUpdate, addr_id: int):
        result = await AddressRepository.update_addr(db,user_id,addr,addr_id)
        address = AddressResponse.model_validate(result)

        return address

    @staticmethod
    async def delete_addr(db:AsyncSession,user_id:int,addr_id:int):
        result = await AddressRepository.delete_addr(db,addr_id,user_id)

        return result

    @staticmethod
    async def set_default(db:AsyncSession,user_id:int,addr_id: int, isDefault: bool):
        result = await AddressRepository.set_default_addr(db,addr_id,isDefault,user_id)
        address = AddressResponse.model_validate(result)

        return address

