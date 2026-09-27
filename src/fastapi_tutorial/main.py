import uvicorn
from fastapi import FastAPI

from fastapi_tutorial.db import Base, engine
from fastapi_tutorial.routers import api_router
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI")
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return {"message": "Hello World asdfasdf asdf"}


if __name__ == "__main__":
    uvicorn.run(
        "fastapi_tutorial.main:app",
        host="127.0.0.1",
        port=8001,
        reload=True,
        app_dir="src",
    )
