from fastapi import APIRouter

from fastapi_tutorial.routers.auth import router as auth_router
from fastapi_tutorial.routers.posts import router as posts_router
from fastapi_tutorial.routers.users import router as users_router

api_router = APIRouter()
api_router.include_router(posts_router)
api_router.include_router(users_router)
api_router.include_router(auth_router)