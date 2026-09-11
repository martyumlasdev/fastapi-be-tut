from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_tutorial.db import get_db
from fastapi_tutorial.models import Post as PostModel
from fastapi_tutorial.schema import CreatePost, Post, UpdatePost

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=list[Post])
def read_posts(
    q: str | None = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
) -> list[Post]:
    query = select(PostModel)
    if q:
        query = query.where(PostModel.title.contains(q))
    return list(db.scalars(query.offset(skip).limit(limit)))


@router.get("/{post_id}", response_model=Post)
def read_post(post_id: int, db: Session = Depends(get_db)) -> Post:
    post = db.get(PostModel, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post(post: CreatePost, db: Session = Depends(get_db)) -> Post:
    new_post = PostModel(**post.model_dump())
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
