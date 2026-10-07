from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_tutorial.db import SessionLocal
from fastapi_tutorial.models import Post, Tag, User
from fastapi_tutorial.security import get_password_hash
from fastapi_tutorial.seed.factories import (
    create_post,
    create_tag,
    create_user,
)


def get_or_create_user(
    db: Session,
    *,
    first_name: str,
    last_name: str,
    email: str,
    password_hash: str,
) -> User:
    user = db.scalar(
        select(User).where(User.email == email)
    )

    if user:
        return user

    return create_user(
        db,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password_hash=password_hash,
    )


def get_or_create_tag(
    db: Session,
    *,
    name: str,
) -> Tag:
    tag = db.scalar(
        select(Tag).where(Tag.name == name)
    )

    if tag:
        return tag

    return create_tag(
        db,
        name=name,
    )


def get_or_create_post(
    db: Session,
    *,
    title: str,
    content: str,
    user_id: int,
    published: bool = True,
) -> Post:
    post = db.scalar(
        select(Post).where(
            Post.title == title,
            Post.user_id == user_id,
        )
    )

    if post:
        return post

    return create_post(
        db,
        title=title,
        content=content,
        user_id=user_id,
        published=published,
    )


def add_tag_to_post(
    post: Post,
    tag: Tag,
) -> None:
    if tag not in post.tags:
        post.tags.append(tag)


def seed_database() -> None:
    db = SessionLocal()

    try:
        # ---------------------------------------------------------
        # Users
        # ---------------------------------------------------------

        user1 = get_or_create_user(
            db,
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password_hash=get_password_hash("password"),
        )

        user2 = get_or_create_user(
            db,
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com",
            password_hash=get_password_hash("password"),
        )

        # ---------------------------------------------------------
        # Tags
        # ---------------------------------------------------------

        python_tag = get_or_create_tag(
            db,
            name="Python",
        )

        fastapi_tag = get_or_create_tag(
            db,
            name="FastAPI",
        )

        sqlalchemy_tag = get_or_create_tag(
            db,
            name="SQLAlchemy",
        )

        # ---------------------------------------------------------
        # Posts
        # ---------------------------------------------------------

        post1 = get_or_create_post(
            db,
            title="Learning FastAPI",
            content="Building APIs with FastAPI.",
            user_id=user1.id,
        )

        post2 = get_or_create_post(
            db,
            title="Learning SQLAlchemy",
            content="Working with SQLAlchemy ORM.",
            user_id=user1.id,
        )

        post3 = get_or_create_post(
            db,
            title="Python Type Hints",
            content="Understanding Python type hints.",
            user_id=user2.id,
        )

        # ---------------------------------------------------------
        # Post ↔ Tag relationships
        # ---------------------------------------------------------

        add_tag_to_post(post1, python_tag)
        add_tag_to_post(post1, fastapi_tag)

        add_tag_to_post(post2, python_tag)
        add_tag_to_post(post2, sqlalchemy_tag)

        add_tag_to_post(post3, python_tag)

        # ---------------------------------------------------------
        # Commit
        # ---------------------------------------------------------

        db.commit()

        print("Database seeded successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()