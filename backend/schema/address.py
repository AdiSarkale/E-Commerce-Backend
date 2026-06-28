from pydantic import BaseModel, ConfigDict
from typing import Optional

class AddressCreate(BaseModel):
    user_id: int
    full_name: str
    phone: int
    address_line1: str
    address_line2: str
    city: str
    state: str
    country: str
    pincode: int
    landmark: str
    is_default: bool


class AddressUpdate(AddressCreate):
    full_name: Optional[str] = None
    phone: Optional[int] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    pincode: Optional[int] = None
    landmark: Optional[str] = None
    is_default: bool

class AddressResponse(AddressCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

