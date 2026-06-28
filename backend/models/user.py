from db import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
class User(Base):
    __tablename__ = 'users'

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(265))
    name: Mapped[str] = mapped_column(String(50))
    hashed_password : Mapped[str] = mapped_column(String(265))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    isDeleted: Mapped[bool] = mapped_column(Boolean,default=False)

    cart = relationship("Cart",back_populates='user')
    order = relationship('Orders', back_populates='user')
    addresses = relationship('Address',back_populates='user',cascade='all, delete-orphan')
