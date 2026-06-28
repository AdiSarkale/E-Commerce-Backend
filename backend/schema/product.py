from pydantic import BaseModel
from datetime import datetime


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    created_at: datetime

    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    name: str
    description: str | None
    price: float


class ProductUpdate(BaseModel):
    name: str
    description: str | None = None
    price: float | None = None


class ProductDeleteResponse(BaseModel):
    id: int
