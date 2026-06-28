from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models.order import Orders
from models.order_item import OrderItem


class OrderRepository:

    @staticmethod
    async def create_order(
        db,user_id: int,total_amount: float):

        order = Orders(
            user_id = user_id,
            total_amount = total_amount,
            status= 'PENDING')

        db.add(order)

        await db.flush()

        return order


    @staticmethod
    async def creat_order_item(
        db,
        order_id: int,
        product_id: int,
        quantity: int,
        price: float):

        item = OrderItem(
            order_id = order_id,
            product_id = product_id,
            quantit = quantity,
            price = price)

        db.add(item)

        await db.flush()
        return item


    @staticmethod
    async def get_users_orders(
        db,
        user_id:int):

        res = await db.execute(
            select(Orders).where(Orders.user_id == user_id).options(selectinload(Orders.order_item)))

        user_order = res.scalars().all()

        if not user_order:
            raise ValueError(f'No Orders for {user_id}')

        return user_order
