from db import Base
from sqlalchemy import Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
class Address(Base):

    __tablename__ = 'addresses'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer,ForeignKey('users.id'))
    full_name: Mapped[str] = mapped_column(String)
    phone: Mapped[int] = mapped_column(Integer)
    address_line1: Mapped[str] = mapped_column(String(265))
    address_line2: Mapped[str] = mapped_column(String(265))
    city: Mapped[str] = mapped_column(String)
    state: Mapped[str] = mapped_column(String)
    country: Mapped[str] = mapped_column(String)
    pincode: Mapped[int] = mapped_column(Integer)
    landmark: Mapped[str] = mapped_column(String)
    is_default: Mapped[bool] = mapped_column(Boolean)

    user = relationship('User',back_populates='addresses')
