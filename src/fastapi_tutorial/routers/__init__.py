from fastapi import APIRouter

from fastapi_tutorial.routers.auth import router as auth_router
from fastapi_tutorial.routers.posts_authenticated import (
    router as authenticated_posts_router,
)
from fastapi_tutorial.routers.posts_public import router as public_posts_router
from fastapi_tutorial.routers.users import router as users_router

api_router = APIRouter()
# Register authenticated static paths before the public /{post_id} route.
api_router.include_router(authenticated_posts_router)
api_router.include_router(public_posts_router)
api_router.include_router(users_router)
api_router.include_router(auth_router)
