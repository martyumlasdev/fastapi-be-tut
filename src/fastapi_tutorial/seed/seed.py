from faker import Faker

from fastapi_tutorial.db import SessionLocal
from fastapi_tutorial.models import Post
from fastapi_tutorial.security import get_password_hash
from fastapi_tutorial.seed.factories import (
    create_post,
    create_tag,
    create_user,
)

fake = Faker()
fake.seed_instance(12345)


def seed_database() -> None:
    db = SessionLocal()

    try:
        # ---------------------------------------------------------
        # Users
        # ---------------------------------------------------------

        users = []

        for _ in range(20):
            user = create_user(
                db,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.unique.email(),
                password_hash=get_password_hash("password"),
            )

            users.append(user)

        # ---------------------------------------------------------
        # Tags
        # ---------------------------------------------------------

        tag_names = [
            "Python",
            "FastAPI",
            "SQLAlchemy",
            "Docker",
            "AWS",
            "Testing",
            "Backend",
            "API",
            "Programming",
            "Web Development",
        ]

        tags = []

        for name in tag_names:
            tag = create_tag(
                db,
                name=name,
            )

            tags.append(tag)

        # ---------------------------------------------------------
        # Posts
        # ---------------------------------------------------------

                # Posts
        posts = []

        for _ in range(1_000):
            user = fake.random_element(users)

            post = Post(
                title=fake.sentence(nb_words=6),
                content=fake.paragraph(nb_sentences=5),
                published=True,
                user_id=user.id,
            )

            db.add(post)
            posts.append(post)

        # Flush once so all posts are synchronized with the database.
        db.flush()

        # ---------------------------------------------------------
        # Post ↔ Tag relationships
        # ---------------------------------------------------------

        for post in posts:
            number_of_tags = fake.random_int(
                min=1,
                max=3,
            )

            post_tags = fake.random_elements(
                elements=tags,
                length=number_of_tags,
                unique=True,
            )

            post.tags.extend(post_tags)

        # ---------------------------------------------------------
        # Commit everything
        # ---------------------------------------------------------

        db.commit()

        print("Database seeded successfully.")
        print(f"Users: {len(users)}")
        print(f"Tags: {len(tags)}")
        print(f"Posts: {len(posts)}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()