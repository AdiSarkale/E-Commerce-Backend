from db import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id")
    )

    product_id: Mapped[int]= mapped_column(
        ForeignKey("products.id")
    )

    quantit: Mapped[int] = mapped_column(Integer)

    price: Mapped[Float] = mapped_column(Float)

    order = relationship('Orders', back_populates='order_item')
    product = relationship('Product', back_populates='order_item')
