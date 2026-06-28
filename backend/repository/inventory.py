from models.inventory import Inventory
from sqlalchemy import select


class InventoryRepository:

    @staticmethod
    async def create(
        db,
        product_id:int,
        quantity: int):

        inventory =  Inventory(
            product_id = product_id,
            quantity = quantity
            )

        db.add(inventory)
        await db.flush()

        return inventory


    @staticmethod
    async def get_by_product(
        db,
        product_id: int):

        result = await db.execute(
            select(Inventory).where(Inventory.product_id == product_id))

        prd = result.scalar_one_or_none()
        if not prd:
            raise ValueError('No Products with ID : {product_id} Exists')


    @staticmethod
    async def reduce_stock(
        inventory,
        quantity: int):

        inventory.quantity -= quantity


    @staticmethod
    async def increase_stock(
        db,
        inventory: Inventory,
        quantity: int
    ):
        inventory.quantity += quantity

        await db.commit()
        await db.refresh(inventory)

        return inventory


    @staticmethod
    async def update_stock(
        db,
        product_id: int,
        quantity: int
    ):

        result = await db.execute(
            select(Inventory)
            .where(
                Inventory.product_id == product_id
            )
        )

        inventory = result.scalar_one_or_none()

        if not inventory:
            raise ValueError(
                "Inventory not found"
            )

        if  quantity < inventory.quantity:
            raise ValueError(
                "Entered Quantity is lower than the stock existing"
            )

        inventory.quantity += quantity

        await db.flush()
        await db.refresh(inventory)

        return inventory
