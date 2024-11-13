from fastapi import APIRouter

from .urls import urls_router


v1_router = APIRouter(prefix="/v1")
v1_router.include_router(urls_router)
