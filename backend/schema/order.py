from datetime import datetime
from pydantic import BaseModel, ConfigDict
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = 'PENDING'
    PAID = 'PAID'
    SHIPPED = 'SHIPPED'
    DELIVERED = 'DELIVERED'
    CANCELLED = 'CANCELLED'



class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: int
    quantit: int
    price: float

class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    status: str
    total_amount: float

    order_item: list[OrderItemResponse]
    created_at: datetime


class OrderStatusUpdate(BaseModel):
    status: OrderStatus




class CheckoutRequest(BaseModel):
    pass


class CheckoutResponse(BaseModel):

    order_id: int
    total_amount: float
    status: str
