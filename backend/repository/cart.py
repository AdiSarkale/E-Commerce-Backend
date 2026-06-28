from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession


from models.cart import Cart
from repository.inventory import InventoryRepository
from models.cart_item import CartItem
from sqlalchemy.orm import selectinload
from schema.inventory import InventoryResponse
from repository.product import ProductRepository


class CartRepository:
    @staticmethod
    async def get_user_cart(
        db: AsyncSession,
        user_id: int):
        result = await db.execute(select(Cart).where(Cart.user_id == user_id).options(selectinload(Cart.items)))
        return result.scalar_one_or_none()


    @staticmethod
    async def create_cart(
        db:AsyncSession,
        user_id: int):

        new_cart = Cart(user_id=user_id)
        db.add(new_cart)
        await db.flush()

        return new_cart

    @staticmethod
    async def add_item(
        db: AsyncSession,
        cart_id: int,
        product_id: int,
        quantity: int):


        existing = await CartRepository.check_existing(db,cart_id,product_id)

        if existing:
            return existing

        product = await ProductRepository.get_by_id(db,product_id)

        inv = await InventoryRepository.get_by_product(db,product_id)
        res = InventoryResponse.model_validate(inv)
        if res.quantity < quantity:
            raise ValueError(f'Deficit of Stock in Inventory for Product with ID : {res.product_id}')

        item = CartItem(
            cart_id = cart_id,
            product_id = product_id,
            quantity = quantity,
            price = product.price
            )

        db.add(item)
        await db.flush()

        return item

    @staticmethod
    async def check_existing(
        db: AsyncSession,
        cart_id,
        product_id,
        ):
         #check if that product id already in cart
        existing_item = await db.execute(
            select(CartItem).where(
                CartItem.cart_id == cart_id,
                CartItem.product_id == product_id
            )
        )
        existing_item = existing_item.scalar_one_or_none()

        if existing_item:
            ch = await CartRepository.increase_by_one(db, existing_item)
            await db.flush()
            return ch
        return None



    @staticmethod
    async def get_item(
        db: AsyncSession,
        item_id: int):

        result = await db.execute(
            select(CartItem)
            .where(CartItem.id == item_id)
            )

        return result.scalars().all()

    @staticmethod
    async def get_cart_items(
        db: AsyncSession,
        cart_id: int):
        result = await db.execute(
            select(CartItem).where(CartItem.cart_id == cart_id).options(selectinload(CartItem.product)))

        return result.scalars().all()

    @staticmethod
    async def get_cart_by_id(
        db: AsyncSession,
        cart_id: int
        ):

        result = await db.execute(select(Cart).where(Cart.id == cart_id).options(selectinload(Cart.items)))

        return result.scalar_one_or_none()

    @staticmethod
    async def delete_item(
        db:AsyncSession,
        item):

        await db.delete(item)


    @staticmethod
    async def increase_by_one(db,
        existing_item):

        if existing_item:
            existing_item.quantity += 1
            await db.flush()
            return existing_item
        return None

    @staticmethod
    async def dsc_one(db,cart_id,product_id):
        existing_item = await db.execute(
            select(CartItem).where(
                CartItem.cart_id == cart_id,
                CartItem.product_id == product_id
            )
        )
        existing_item = existing_item.scalar_one_or_none()
        if existing_item and existing_item.quantity > 0:
            existing_item.quantity -= 1
            await db.flush()
            return existing_item


    @staticmethod
    async def quantity_change(db,quantity,cart_id,product_id):
        #check if that product id already in cart
        existing_item = await db.execute(
            select(CartItem).where(
                CartItem.cart_id == cart_id,
                CartItem.product_id == product_id
            )
        )

        if existing_item:
            existing_item.quantity = quantity if quantity > 0 else 0
            await db.flush()
            return existing_item


    @staticmethod
    async def clear_cart(
        db,cart_id:int):

        await db.execute(
            delete(CartItem).where(CartItem.cart_id == cart_id))
