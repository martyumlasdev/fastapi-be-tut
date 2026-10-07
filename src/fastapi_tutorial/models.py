from datetime import datetime

from sqlalchemy import Column, ForeignKey, String, Table, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_tutorial.db import Base


# ============================================================
# Association Tables
# ============================================================

post_tags = Table(
    "post_tags",
    Base.metadata,
    Column(
        "post_id",
        ForeignKey("posts.id"),
        primary_key=True,
    ),
    Column(
        "tag_id",
        ForeignKey("tags.id"),
        primary_key=True,
    ),
)


user_roles = Table(
    "user_roles",
    Base.metadata,
    Column(
        "user_id",
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "role_id",
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column(
        "role_id",
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "permission_id",
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


# ============================================================
# Models
# ============================================================


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    first_name: Mapped[str] = mapped_column(index=True)
    last_name: Mapped[str] = mapped_column(index=True)

    email: Mapped[str] = mapped_column(
        unique=True,
        index=True,
    )

    password_hash: Mapped[str]

    is_active: Mapped[bool] = mapped_column(default=True)

    posts: Mapped[list["Post"]] = relationship(
        back_populates="user",
    )

    roles: Mapped[list["Role"]] = relationship(
        secondary=user_roles,
        back_populates="users",
    )


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    title: Mapped[str] = mapped_column(index=True)
    content: Mapped[str]

    published: Mapped[bool] = mapped_column(default=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )

    user: Mapped["User"] = relationship(
        back_populates="posts",
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
    )

    tags: Mapped[list["Tag"]] = relationship(
        secondary=post_tags,
        back_populates="posts",
    )


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    name: Mapped[str] = mapped_column(
        unique=True,
        index=True,
    )

    posts: Mapped[list["Post"]] = relationship(
        secondary=post_tags,
        back_populates="tags",
    )


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
    )

    users: Mapped[list["User"]] = relationship(
        secondary=user_roles,
        back_populates="roles",
    )

    permissions: Mapped[list["Permission"]] = relationship(
        secondary=role_permissions,
        back_populates="roles",
    )


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
    )

    roles: Mapped[list["Role"]] = relationship(
        secondary=role_permissions,
        back_populates="permissions",
    )