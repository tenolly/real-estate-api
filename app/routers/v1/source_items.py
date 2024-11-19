import logging
from uuid import UUID
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Query

from pydantic import HttpUrl
from models import SourceModel
from database import get_async_db
from utils.raise_if import raise_if_none, raise_if_not_none
from api.schemas.source import SourceItem, SourceCreateRequest
from api.exceptions.source import SourceNotFoundException, SourceAlreadyExistsException
from app.api.exceptions.body import InvalidBodyAndQueryParamsException


source_items_router = APIRouter(prefix="/source-items")
SOURCE_ITEMS_LOGGER = logging.getLogger(__name__)


@source_items_router.get("/", response_model=SourceItem)
async def get_source_by_url(url: HttpUrl, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(SourceModel).filter(SourceModel.url == str(url)))
    return raise_if_none(result.scalar_one_or_none(), SourceNotFoundException())


@source_items_router.get("/{uid}", response_model=SourceItem)
async def get_source_by_uuid(uid: UUID, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(SourceModel).filter(SourceModel.uid == uid))
    return raise_if_none(result.scalar_one_or_none(), SourceNotFoundException())


@source_items_router.post("/", response_model=SourceItem)
async def create_or_get_and_update_source(
    request: Optional[SourceCreateRequest] = None,
    url: Optional[HttpUrl] = Query(None),
    db: AsyncSession = Depends(get_async_db),
):
    if request:
        result = await db.execute(
            select(SourceModel).filter(SourceModel.url == str(request.url))
        )
        raise_if_not_none(result.scalar_one_or_none(), SourceAlreadyExistsException())

        new_source = SourceModel(url=str(request.url))
        db.add(new_source)
        await db.commit()
        await db.refresh(new_source)

        return new_source
    elif url:
        result = await db.execute(
            select(SourceModel).filter(SourceModel.url == str(url))
        )
        source = raise_if_none(result.scalar_one_or_none(), SourceNotFoundException())

        # TODO: Perform updates to `source` here

        await db.commit()
        await db.refresh(source)

        return source
    else:
        raise InvalidBodyAndQueryParamsException()


@source_items_router.post("/{uid}", response_model=SourceItem)
async def get_and_update_source_by_uuid(
    uid: UUID, db: AsyncSession = Depends(get_async_db)
):
    result = await db.execute(select(SourceModel).filter(SourceModel.uid == uid))
    source = raise_if_none(result.scalar_one_or_none(), SourceNotFoundException())

    # TODO: Perform updates to `source` here

    await db.commit()
    await db.refresh(source)

    return source


@source_items_router.delete("/{uid}")
async def delete_source(uid: UUID, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(SourceModel).filter(SourceModel.uid == uid))
    source = raise_if_none(result.scalar_one_or_none(), SourceNotFoundException())

    await db.delete(source)
    await db.commit()

    return {"detail": "source deleted"}
