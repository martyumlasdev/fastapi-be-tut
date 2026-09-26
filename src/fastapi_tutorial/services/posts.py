from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_tutorial.models import Post as PostModel
from fastapi_tutorial.models import User
from fastapi_tutorial.schema import CreatePost, UpdatePost


def get_posts(
    db: Session,
    q: str | None = None,
    skip: int = 0,
    limit: int = 10,
) -> list[PostModel]:

    query = select(PostModel)

    if q:
        query = query.where(PostModel.title.contains(q))

    return list(
        db.scalars(
            query.offset(skip).limit(limit)
        )
    )

def get_post(
    post_id: int,
    db: Session,
) -> PostModel:

    post = db.get(PostModel, post_id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    return post

def create_post(
    post: CreatePost,
    current_user: User,
    db: Session,
) -> PostModel:

    new_post = PostModel(
        title=post.title,
        content=post.content,
        published=post.published,
        user=current_user,
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

def update_post(
    post_id: int,
    post: UpdatePost,
    current_user: User,
    db: Session,
) -> PostModel:

    existing = _get_user_post(
        post_id=post_id,
        current_user=current_user,
        db=db,
    )

    for field, value in post.model_dump(exclude_unset=True).items():
        setattr(existing, field, value)

    db.commit()
    db.refresh(existing)

    return existing

def delete_post(
    post_id: int,
    current_user: User,
    db: Session,
) -> None:

    post = _get_user_post(
        post_id=post_id,
        current_user=current_user,
        db=db,
    )

    db.delete(post)
    db.commit()
    
def _get_post(
    post_id: int,
    db: Session,
) -> PostModel:

    post = db.get(PostModel, post_id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    return post

def _get_user_post(
    post_id: int,
    current_user: User,
    db: Session,
) -> PostModel:

    post = _get_post(
        post_id=post_id,
        db=db,
    )

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this post",
        )

    return post

def get_user_posts(
    current_user: User,
    db: Session,
    skip: int = 0,
    limit: int = 10,
) -> list[PostModel]:

    query = (
        select(PostModel)
        .where(PostModel.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
    )

    return list(db.scalars(query))

