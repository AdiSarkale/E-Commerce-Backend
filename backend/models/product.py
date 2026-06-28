from db import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from datetime import datetime


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(265))
    description: Mapped[str] = mapped_column(String(265))
    price: Mapped[float] = mapped_column(Float)
    sku: Mapped[str] = mapped_column(String(265), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    inventory = relationship('Inventory', back_populates='product')
    items = relationship('CartItem', back_populates='product')
    order_item = relationship('OrderItem', back_populates='product')
