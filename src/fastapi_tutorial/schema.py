from typing import Any

from pydantic import BaseModel


class Item(BaseModel):
    id: int | None = None
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class CreateItem(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class UpdateItem(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float | None = None


class SuccessResponse(BaseModel):
    message: str = "Success"
    data: Any = None


class ErrorResponse(BaseModel):
    message: str = "Request failed"
    detail: Any = None
