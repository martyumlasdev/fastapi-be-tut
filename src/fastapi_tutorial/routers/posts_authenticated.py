from fastapi import APIRouter, Depends, status

from fastapi_tutorial.dependencies import (
    CurrentUser,
    DBSession,
    Pagination,
    get_current_user,
)
from fastapi_tutorial.schema import CreatePost, Post, UpdatePost
from fastapi_tutorial.services.posts import _get_user_post
from fastapi_tutorial.services.posts import create_post as create_post_service
from fastapi_tutorial.services.posts import delete_post as delete_post_service
from fastapi_tutorial.services.posts import get_user_posts as get_user_posts_service
from fastapi_tutorial.services.posts import update_post as update_post_service

router = APIRouter(
    prefix="/my/posts",
    tags=["My Posts"],
)


@router.get("/", response_model=list[Post])
def read_my_posts(
    current_user: CurrentUser,
    db: DBSession,
    pagination: Pagination,
) -> list[Post]:

    return get_user_posts_service(
        current_user=current_user,
        db=db,
        **pagination
    )


@router.get("/{post_id}", response_model=Post)
def read_my_post(
    post_id: int,
    current_user: CurrentUser,
    db: DBSession,
) -> Post:

    return _get_user_post(
        post_id=post_id,
        current_user=current_user,
        db=db,
    )


@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post(
    post: CreatePost,
    current_user: CurrentUser,
    db: DBSession,
) -> Post:
    return create_post_service(post=post, current_user=current_user, db=db)


@router.put("/{post_id}", response_model=Post)
def update_post(
    post_id: int,
    post: UpdatePost,
    current_user: CurrentUser,
    db: DBSession,
) -> Post:
    return update_post_service(
        post_id=post_id,
        post=post,
        current_user=current_user,
        db=db,
    )


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    current_user: CurrentUser,
    db: DBSession,
) -> None:
    delete_post_service(post_id=post_id, current_user=current_user, db=db)
