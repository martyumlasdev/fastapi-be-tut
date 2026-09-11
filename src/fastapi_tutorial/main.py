import uvicorn
from fastapi import FastAPI

from fastapi_tutorial.db import Base, engine
from fastapi_tutorial.routers.posts import router as posts_router
from fastapi_tutorial.routers.users import router as users_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI")
app.include_router(posts_router)
app.include_router(users_router)


@app.get("/")
async def root():
    return {"message": "Hello World asdfasdf asdf"}


if __name__ == "__main__":
    uvicorn.run(
        "fastapi_tutorial.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        app_dir="src",
    )
