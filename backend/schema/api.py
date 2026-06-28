from pydantic import BaseModel
from typing import Generic, Any, TypeVar

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: T | None = None
