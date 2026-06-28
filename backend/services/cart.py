from sqlalchemy.ext.asyncio import AsyncSession
from schema.cart import CartResponse
from repository.cart import CartRepository
from repository.product import ProductRepository

from utils.cache import CacheManager
import json

class CartService:


    @staticmethod
    async def create_cart(
        db:AsyncSession,
        id: int):
        created = await CartRepository.create_cart(db=db, user_id=id)
        await db.commit()
        await db.refresh(created)
        return created

    @staticmethod
    async def add_to_cart(
        db: AsyncSession,
        user_id: int,
        product_id: int,
        quantity: int):

        cache_key = f'cart:{user_id}'

        # print(product_id)
        # print(type(product_id))
        product = await ProductRepository.get_by_id(db,product_id)

        if not product:
            raise ValueError(f"Product with id: {product_id} doesn't exists")



        cart = await CartRepository.get_user_cart(db,user_id)
        print(cart)
        print(type(cart))

        if not cart:
            print(Exception)

        item = await CartRepository.add_item(
            db,cart.id,product_id,quantity)

        await db.commit()

        # response = CartResponse.model_validate(item)

        # await CacheManager.set(
        #     cache_key,
        #     response.model_dump_json(),
            # ttl=300)
        await CacheManager.delete(cache_key)
        return item

    @staticmethod
    async def get_cart(
        db:AsyncSession,
        user_id: int
        ):

        cache_key = f'cart:{user_id}'

        cached = await CacheManager.get(cache_key)
        if cached:
           return CartResponse.model_validate_json(cached)
        cart = await CartRepository.get_user_cart(db,user_id)

        if not cart:
            return None

        result = await CartRepository.get_cart_by_id(db,cart.id)

        response = CartResponse.model_validate(result)

        await CacheManager.set(
            cache_key,
            response.model_dump_json(),
            ttl=300)

        return response


    @staticmethod
    async def quantity_update(db,user_id,quantity, product_id):
        cache_key = f'cart:{user_id}'
        updated = await CartRepository.quantity_change(db,user_id,quantity,product_id)

        await CacheManager.delete(cache_key)

        return updated

    @staticmethod
    async def delete_cart_item(db:AsyncSession,user_id:int, item_id: int):

        cache_key = f'cart:{user_id}'
        cart = await CartRepository.get_user_cart(db,user_id)
        if not cart:
            return None


        item = await CartRepository.get_item(db,item_id)
        if not item:
            return None

        deleted = await CartRepository.delete_item(db,item)

        await CacheManager.delete(cache_key)

        return deleted


