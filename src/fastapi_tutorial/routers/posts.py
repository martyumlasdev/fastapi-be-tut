from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_tutorial.db import get_db
from fastapi_tutorial.dependencies import (
    get_current_page,
    get_current_user,
    get_pagination,
)
from fastapi_tutorial.models import Post as PostModel, User as UserModel
from fastapi_tutorial.schema import CreatePost, PaginatedPosts, Post, UpdatePost

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=PaginatedPosts)
def read_posts(
    q: str | None = None,
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination),
    page: int = Depends(get_current_page),
) -> PaginatedPosts:
    query = select(PostModel)
    if q:
        query = query.where(PostModel.title.contains(q))
    posts = list(
        db.scalars(query.offset(pagination["skip"]).limit(pagination["limit"]))
    )

    return {
        "page": page,
        "skip": pagination["skip"],
        "limit": pagination["limit"],
        "posts": posts,
    }


@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post(post: CreatePost, db: Session = Depends(get_db)) -> Post:

    user = db.get(UserModel, post.user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    new_post = PostModel(
        title=post.title,
        content=post.content,
        published=post.published,
        user=user,
    )
    new_post.user = user
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put("/{post_id}", response_model=Post)
def update_post(post_id: int, post: UpdatePost, db: Session = Depends(get_db)) -> Post:
    existing = db.get(PostModel, post_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Post not found")

    for field, value in post.model_dump(exclude_unset=True).items():
        setattr(existing, field, value)
    db.commit()
    db.refresh(existing)
    return existing


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)) -> None:
    post = db.get(PostModel, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()


@router.get("/my-posts")
def read_my_posts(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return current_user.posts


@router.get("/{post_id}", response_model=Post)
def read_post(post_id: int, db: Session = Depends(get_db)) -> Post:
    post = db.get(PostModel, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
