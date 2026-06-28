from db import Base
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from typing import Dict, List


class Api(Base):
    __tablename__ = 'api'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    success: Mapped[bool] = mapped_column(Boolean)
    data: Mapped[dict | list] = mapped_column(Dict,List)
