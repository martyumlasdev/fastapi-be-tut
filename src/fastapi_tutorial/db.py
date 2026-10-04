from collections.abc import AsyncGenerator

from sqlalchemy import create_engine

# from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_engine('sqlite:///./app.db', connect_args={"check_same_thread": False})

# engine = create_async_engine("sqlite+aiosqlite:///./app.db", echo=True)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# AsyncSessionLocal = async_sessionmaker(
#     bind=engine, class_=AsyncSession, expire_on_commit=False
# )

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# async def get_db() -> AsyncGenerator[AsyncSession, None]:
#     async with AsyncSessionLocal() as db:
#         yield db