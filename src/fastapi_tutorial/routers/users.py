from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_tutorial.db import get_db
from fastapi_tutorial.models import User as UserModel
from fastapi_tutorial.schema import CreateUser, UpdateUser, User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[User])
def read_users(
    q: str | None = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
) -> list[User]:
    query = select(UserModel)
    if q:
        query = query.where(UserModel.email.contains(q))
    return list(db.scalars(query.offset(skip).limit(limit)))


@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)) -> User:
    user = db.get(UserModel, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)],) -> User:
    existing = db.scalar(select(UserModel).where(UserModel.email == user.email))
    if existing is not None:
        raise HTTPException(status_code=409, detail="Email already registered")

    new_user = UserModel(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user: UpdateUser, db: Session = Depends(get_db)) -> User:
    existing = db.get(UserModel, user_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="User not found")

    updates = user.model_dump(exclude_unset=True)
    if "email" in updates:
        email_owner = db.scalar(
            select(UserModel).where(
                UserModel.email == updates["email"], UserModel.id != user_id
            )
        )
        if email_owner is not None:
            raise HTTPException(status_code=409, detail="Email already registered")

    for field, value in updates.items():
        setattr(existing, field, value)
    db.commit()
    db.refresh(existing)
    return existing


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)) -> None:
    user = db.get(UserModel, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
