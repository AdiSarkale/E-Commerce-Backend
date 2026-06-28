from pydantic import BaseModel,Field, ConfigDict

class InventoryCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class InventoryUpdate(BaseModel):
    quantity: int = Field(gt=0)


class InventoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity: int
    reserved_quantity: int


