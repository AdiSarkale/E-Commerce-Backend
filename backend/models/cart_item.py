from db import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column,relationship
from datetime import datetime

class CartItem(Base):
    __tablename__ = 'cart_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cart_id: Mapped[int] = mapped_column(Integer, ForeignKey('carts.id'))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id'))

    quantity: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Float)

    product = relationship("Product",back_populates='items')
    cart = relationship("Cart", back_populates='items')
