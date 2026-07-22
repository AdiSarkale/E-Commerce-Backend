from sqlalchemy.ext.asyncio import AsyncSession
from repository.inventory import InventoryRepository
from schema.inventory import InventoryResponse
from utils.cache import CacheManager

from tasks.inventory_tasks import send_low_task_alert

class InventoryService:

    @staticmethod
    async def create_inventory(db: AsyncSession, product_id: int,  quantity: int):

        inv = await InventoryRepository.create(db,product_id,quantity)

        if not inv:
            return None

        await db.commit()
        await db.refresh(inv)

        return inv


    @staticmethod
    async def get_by_id(db:AsyncSession,product_id:int):
        cached_key = f'inv:{product_id}'
        cached = await CacheManager.get(cached_key)
        if cached:
            return InventoryResponse.model_validate(cached)
        res = await InventoryRepository.get_by_product(db, product_id)
        response = InventoryResponse.model_validate(res)

        await CacheManager.set(
            cached_key,
            response.model_dump_json(),
            ttl=300)
        return InventoryResponse.model_validate(res)


    @staticmethod
    async def restock(db: AsyncSession,product_id:int, quantity: int):
        inv = await InventoryRepository.get_by_product(db,product_id)

        if not inv:
            raise ValueError("Inventory Doesn't Exists")

        await InventoryRepository.increase_stock(inv,quantity)
        await db.commit()

        return inv
    @staticmethod
    async def checkstock(db: AsyncSession, product_id:int):

        inv = await InventoryRepository.get_by_product(db,product_id)

        if not inv:
            raise ValueError("Inventory Doesb't Exists")

        if inv.quantity < 10:
           return send_low_task_alert.delay(product_id)


