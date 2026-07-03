from db import Base
from sqlalchemy import Float, Integer, String, Boolean, DateTime, func, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from enum import Enum

class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"


class OrderStatus(str, Enum):
    PENDING = 'PENDING'
    PAID = 'PAID'
    SHIPPED = 'SHIPPED'
    DELIVERED = 'DELIVERED'
    CANCELLED = 'CANCELLED'



class Orders(Base):

    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    total_amount: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    status: Mapped[OrderStatus] = mapped_column(SQLEnum(OrderStatus), default=OrderStatus.PENDING)


    payment_status: Mapped[PaymentStatus] = mapped_column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING)
    payment_method: Mapped[str] = mapped_column(String, default='Card', nullable=True)
    razorpay_order_id: Mapped[str] = mapped_column(String, default='Card', nullable=True)
    razorpay_payment_id: Mapped[str] = mapped_column(String, default='Card', nullable=True)
    razorpay_signature: Mapped[str] = mapped_column(String, default='Card', nullable=True)

    paid_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=func.now())

    user = relationship('User' ,back_populates='order')
    order_item = relationship('OrderItem', back_populates='order')
