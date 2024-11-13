from fastapi import APIRouter

from .source_items import source_items_router


v1_router = APIRouter(prefix="/v1")
v1_router.include_router(source_items_router)
