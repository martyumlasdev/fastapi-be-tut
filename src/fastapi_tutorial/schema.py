from typing import Any

from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    email: str
    is_active: bool = True


class CreateUser(BaseModel):
    email: str
    first_name: str
    last_name: str
    password: str
    is_active: bool = True


class UpdateUser(BaseModel):
    email: str | None = None
    password: str | None = None
    is_active: bool | None = None


class UserSummary(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)
    
class Post(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    title: str
    content: str
    published: bool = True
    user: UserSummary
    


class CreatePost(BaseModel):
    title: str
    content: str
    published: bool = True
    user_id: int

class UpdatePost(BaseModel):
    title: str | None = None
    content: str | None = None
    published: bool | None = None


