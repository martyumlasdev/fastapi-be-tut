from sqlalchemy.orm import Session

from fastapi_tutorial.models import Post, Tag, User


def create_user(
    db: Session,
    *,
    first_name: str,
    last_name: str,
    email: str,
    password_hash: str,
) -> User:
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password_hash=password_hash,
    )

    db.add(user)
    db.flush()

    return user

def create_tag(
    db: Session,
    *,
    name: str,
) -> Tag:
    tag = Tag(
        name=name,
    )

    db.add(tag)
    db.flush()

    return tag

def create_post(
    db: Session,
    *,
    title: str,
    content: str,
    user_id: int,
    published: bool = True,
) -> Post:
    post = Post(
        title=title,
        content=content,
        published=published,
        user_id=user_id,
    )

    db.add(post)
    db.flush()

    return post