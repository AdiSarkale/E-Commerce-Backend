from pydantic import BaseModel, ConfigDict, Field
from schema.cart_item import CartItemResponse




class CartAddItem(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)

class CartUpdateItem(BaseModel):
    quantity: int = Field(gt=0)


class CartResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    items: list[CartItemResponse]


