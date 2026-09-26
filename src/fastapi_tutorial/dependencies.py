from typing import Annotated

import jwt
from fastapi import Depends, Header, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from fastapi_tutorial.core.config import settings
from fastapi_tutorial.db import get_db
from fastapi_tutorial.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_pagination(
        skip: int = 0, 
        limit: int = Query(default=10, le=100)
    ):
    
    return {"skip": skip, "limit": limit}


def get_current_page(
    pagination: Annotated[dict, Depends(get_pagination)],
):
    return pagination["skip"] // pagination["limit"] + 1


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception

    user = db.get(User, int(user_id))

    if user is None:
        raise credentials_exception

    return user


def verify_api_key(
    x_api_key: str | None = Header(default=None),
):
    if x_api_key != "my-secret-key":
        raise HTTPException(
            status_code=401,
            detail="Invalid API key",
        )


CurrentUser = Annotated[User, Depends(get_current_user)]
DBSession = Annotated[Session, Depends(get_db)]
Pagination = Annotated[dict, Depends(get_pagination)]