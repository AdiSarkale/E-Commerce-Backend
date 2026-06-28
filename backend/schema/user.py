from pydantic import BaseModel, ConfigDict
from datetime import datetime


class UserResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    name: str
    created_at: datetime

class UserCreate(BaseModel):
    name: str
    email: str
    hashed_password: str


class UserUpdate(BaseModel):

    name: str | None = None
    email: str | None = None
    hashed_password: str | None = None
