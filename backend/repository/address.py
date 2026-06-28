from models.address import Address
from sqlalchemy.ext.asyncio import AsyncSession
from schema.address import AddressCreate, AddressUpdate, AddressResponse
from sqlalchemy import select,func, update
from utils.cache import CacheManager


class AddressRepository:

    @staticmethod
    async def create_address(db: AsyncSession, addr:AddressCreate,user_id: int):

        cache_key = f"addresses count{addr.phone}"
        cached = await CacheManager.get(cache_key)

        if cached:
            count = int(cached)
        else:
            stmt = select(func.count(Address.id)).where(Address.user_id == user_id)
            count = await db.scalar(stmt)
            print(count)
            await CacheManager.set(cache_key, str(count))


        address = Address(
            user_id = user_id,
            full_name = addr.full_name,
            phone = addr.phone,
            address_line1 = addr.address_line1,
            address_line2 = addr.address_line2,
            city = addr.city,
            state = addr.state,
            country = addr.country,
            pincode = addr.pincode,
            landmark = addr.landmark,
            is_default= (count == 0)
            )
        db.add(address)
        await db.commit()
        await db.refresh(address)
        # if count == 0:
        #     await AddressRepository.set_default_addr(db,address.id,True,user_id)

        # await AddressRepository.set_default_addr(db,address.id,False,user_id)
        return address

    @staticmethod
    async def get_user_addr(db: AsyncSession, user_id:int):
        query = await db.execute(select(Address).where(Address.user_id == user_id))
        user_addr = query.scalars().all()
        return user_addr

    @staticmethod
    async def get_addr_by_id(db: AsyncSession, user_id:int, addr_id: int,):
        query = await db.execute(select(Address).where(Address.id == addr_id, Address.user_id == user_id))
        addr = query.scalar_one_or_none()
        if not addr:
            raise ValueError(f"No Address with ID {addr_id}")

        return addr

    @staticmethod
    async def update_addr(db: AsyncSession,user_id: int, addr: AddressUpdate, addr_id: int):
        query = await db.execute(select(Address).where(Address.id == addr_id, Address.user_id == user_id))
        address = query.scalar_one_or_none()
        if not address:
            raise ValueError(f"No Such Address with ID : {addr_id}")

        address.full_name = addr.full_name
        address.phone = addr.phone
        address.address_line1 = addr.address_line1
        address.address_line2 = addr.address_line2
        address.city = addr.city
        address.state = addr.state
        address.country = addr.country
        address.pincode = addr.pincode
        address.landmark = addr.landmark
        address.is_default = addr.is_default

        await db.commit()
        await db.refresh(address)
        return address

    @staticmethod
    async def get_addr_by_adid_uid(db:AsyncSession,addr_id:int,user_id:int):
        query = await (
            db.execute(select(Address)
            .where(
                Address.id == addr_id,
                Address.user_id == user_id
                )
                       )
            )
        result = query.scalar_one_or_none()

        return result


    @staticmethod
    async def delete_addr(db: AsyncSession, addr_id: int,user_id:int):
        check_existing = await AddressRepository.get_addr_by_adid_uid(db,addr_id,user_id)
        if not check_existing:
            raise ValueError(f"No Such Address with ID : {addr_id} for User with id: {user_id}")
        await db.delete(check_existing)
        await db.commit()


    @staticmethod
    async def check_already_default_address(db: AsyncSession,isDefault:bool, user_id: int):
        stmt = update(Address).where(Address.user_id == user_id).values(is_default=False)
        await db.execute(stmt)
        await db.commit()


    @staticmethod
    async def get_addr_by_id_for_isdefault(db: AsyncSession, user_id:int, addr_id: int,):
        query = await db.execute(select(Address).where(Address.id == addr_id, Address.user_id == user_id))
        addr = query.scalar_one()
        print(addr)
        if not addr:
            raise ValueError(f"No Address with ID {addr_id} {addr}")
        return addr


    @staticmethod
    async def set_default_addr(db: AsyncSession, addr_id: int, isDefault: bool,user_id: int):
        check_existing = await AddressRepository.get_addr_by_id_for_isdefault(db,user_id,addr_id)
        if not check_existing:
            raise ValueError(f"No Such Address with ID : {addr_id}")
        await AddressRepository.check_already_default_address(db,isDefault,user_id)
        check_existing.is_default = True
        await db.commit()
        await db.refresh(check_existing)
        return check_existing
