from fastapi import Depends, Header, HTTPException, Query
from sqlalchemy.orm import Session

from fastapi_tutorial.db import get_db
from fastapi_tutorial.models import User as UserModel


def get_pagination(skip: int = 0, limit: int = Query(default=10, le=100)):
    return {"skip": skip, "limit": limit}


def get_current_page(
    pagination: dict = Depends(get_pagination),
):
    return pagination["skip"] // pagination["limit"] + 1


def get_current_user(
        user_id: int, 
        db: Session = Depends(get_db)          
) -> UserModel:

    user = db.get(UserModel, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def verify_api_key(
    x_api_key: str | None = Header(default=None),
):
    if x_api_key != "my-secret-key":
        raise HTTPException(
            status_code=401,
            detail="Invalid API key",
        )