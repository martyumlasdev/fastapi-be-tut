from typing import Any

from pydantic import BaseModel, ConfigDict


class Post(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    title: str
    content: str
    published: bool = True


class CreatePost(BaseModel):
    title: str
    content: str
    published: bool = True


class UpdatePost(BaseModel):
    title: str | None = None
    content: str | None = None
    published: bool | None = None


class SuccessResponse(BaseModel):
    message: str = "Success"
    data: Any = None


class ErrorResponse(BaseModel):
    message: str = "Request failed"
    detail: Any = None
