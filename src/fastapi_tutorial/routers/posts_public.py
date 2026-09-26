from fastapi import APIRouter

from fastapi_tutorial.dependencies import DBSession
from fastapi_tutorial.schema import Post
from fastapi_tutorial.services.posts import get_post, get_posts

router = APIRouter(prefix="/posts", tags=["public posts"])


@router.get("/", response_model=list[Post])
def read_posts(
    db: DBSession,
    q: str | None = None,
    skip: int = 0,
    limit: int = 10,
) -> list[Post]:
    return get_posts(db=db, q=q, skip=skip, limit=limit)


@router.get("/{post_id}", response_model=Post)
def read_post(post_id: int, db: DBSession) -> Post:
    return get_post(post_id=post_id, db=db)
