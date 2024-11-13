import logging
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends

from pydantic import HttpUrl
from models import SourceModel
from database import get_async_db
from api.schemas.source import SourceItem, SourceCreateRequest
from api.exceptions.source import SourceNotFoundException, SourceAlreadyExistsException


source_items_router = APIRouter(prefix="/source-items")
SOURCE_ITEMS_LOGGER = logging.getLogger(__name__)


@source_items_router.get("/", response_model=SourceItem)
async def get_source_by_url(url: HttpUrl, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(SourceModel).filter(SourceModel.url == str(url)))
    if (source := result.scalar_one_or_none()) is None:
        raise SourceNotFoundException()
    
    return source


@source_items_router.get("/{uid}", response_model=SourceItem)
async def get_source_by_uuid(uid: UUID, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(SourceModel).filter(SourceModel.uid == uid))
    if (source := result.scalar_one_or_none()) is None:
        raise SourceNotFoundException()
    
    return source


@source_items_router.post("/new", response_model=SourceItem)
async def create_source(request: SourceCreateRequest, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(SourceModel).filter(SourceModel.url == str(request.url)))
    if (source := result.scalar_one_or_none()):
        raise SourceAlreadyExistsException()
    
    new_source = SourceModel(url=str(request.url))
    db.add(new_source)
    await db.commit()
    await db.refresh(new_source)

    return new_source


@source_items_router.post("/", response_model=SourceItem)
async def get_and_update_source_by_url(url: HttpUrl, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(SourceModel).filter(SourceModel.url == str(url)))
    if (source := result.scalar_one_or_none()) is None:
        raise SourceNotFoundException()
    
    # TODO: Perform updates to `source` here

    await db.commit()
    await db.refresh(source)

    return source


@source_items_router.post("/{uid}", response_model=SourceItem)
async def get_and_update_source_by_uuid(uid: UUID, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(SourceModel).filter(SourceModel.uid == uid))
    if (source := result.scalar_one_or_none()) is None:
        raise SourceNotFoundException()
    
    # TODO: Perform updates to `source` here

    await db.commit()
    await db.refresh(source)

    return source


@source_items_router.delete("/{uid}")
async def delete_source(uid: UUID, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(SourceModel).filter(SourceModel.uid == uid))
    if (source := result.scalar_one_or_none()) is None:
        raise SourceNotFoundException()
    
    await db.delete(source)
    await db.commit()

    return {"detail": "source deleted"}
