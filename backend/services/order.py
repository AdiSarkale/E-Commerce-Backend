from repository.cart import CartRepository
from repository.inventory import InventoryRepository
from repository.order import OrderRepository

from repository.user import UserRepository
from utils.cache import CacheManager
from api.inventory import InventoryResponse
from schema.order import OrderResponse
from tasks.order_task import send_order_confirmation
import json


class OrderService:

    @staticmethod
    async def checkout(
        db,
        user_id: int):

        email = await UserRepository.get_mail_by_id(db,user_id)
        cart = await CartRepository.get_user_cart(db,user_id)

        if not cart:
            raise ValueError('Cart not found')

        items = await CartRepository.get_cart_items(db,cart.id)
        print(items)
        if not items:
            raise ValueError('No items in Cart')


        total_amount = 0

        for item in items:
            product = item.product

            total_amount += (
                product.price *  item.quantity)

        try:
            # db.rollback()
            # async with db.begin():
            orders = await OrderRepository.create_order(db,user_id,total_amount)

            for item in items:
                inventory = await InventoryRepository.get_by_product(db,product_id=item.product_id)

                if not inventory:
                    raise ValueError(
                        'Inventory not found')
                print(f"HEERE IS THE INV QUANTITY {inventory.quantity} \n HERE IS TE ITEM QUANTITY {item.quantity}")
                if inventory.quantity < item.quantity:
                    raise ValueError('Insufficient Stock')


                await OrderRepository.creat_order_item(
                    db=db,
                    order_id=orders.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price = item.price)

                await InventoryRepository.reduce_stock(inventory,item.quantity)

                await CartRepository.clear_cart(db,cart_id=cart.id)

                await db.commit()

                # Celery Function to send email to the user
                send_order_confirmation.delay(email,orders.id)

            return {
                "order_id" : orders.id,
                "status": orders.status,
                "total_amount": orders.total_amount
                }
        except Exception:
            db.rollback()
            raise
    @staticmethod
    async def get_orders(
        db,
        user_id):

        cached_key = f"user{user_id}"
        cached = await CacheManager.get(cached_key)

        if cached:
            return OrderResponse.model_validate_json(cached)

        res = await OrderRepository.get_users_orders(db,user_id)

        response = [OrderResponse.model_validate(r) for r in res]

        cache_data = [
            item.model_dump(mode="json")
            for item in response
                ]

        await CacheManager.set(
            cached_key,
            json.dumps(cache_data)
        )


        return response
