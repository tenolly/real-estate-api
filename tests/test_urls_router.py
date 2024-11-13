import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import SourceModel


@pytest.mark.anyio
async def test_create_source(client: AsyncClient, test_db: AsyncSession):
    url = "http://some.com/"
    payload = {"url": url}
    
    response = await client.post("/v1/urls/", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["url"] == url

    result = await test_db.execute(select(SourceModel).filter(SourceModel.url == url))
    source = result.scalar_one_or_none()
    assert source is not None
    assert source.url == url

"""
@pytest.mark.anyio
async def test_get_source_by_url(client: AsyncClient, test_db: AsyncSession):
    url = "http://example.com"
    new_source = SourceModel(url=url)
    test_db.add(new_source)
    await test_db.commit()
    await test_db.refresh(new_source)

    response = await client.get(f"/v1/urls/?url={url}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["url"] == url


@pytest.mark.anyio
async def test_get_source_by_uuid(client: AsyncClient, test_db: AsyncSession):
    new_source = SourceModel(url="http://example.com")
    test_db.add(new_source)
    await test_db.commit()
    await test_db.refresh(new_source)

    response = await client.get(f"/v1/urls/{new_source.uid}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["url"] == "http://example.com"


@pytest.mark.anyio
async def test_delete_source(client: AsyncClient, test_db: AsyncSession):
    new_source = SourceModel(url="http://example.com")
    test_db.add(new_source)
    await test_db.commit()
    await test_db.refresh(new_source)

    response = await client.delete(f"/v1/urls/{new_source.uid}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["detail"] == "source deleted"

    result = await test_db.execute(select(SourceModel).filter(SourceModel.uid == new_source.uid))
    source = result.scalar_one_or_none()
    assert source is None


@pytest.mark.anyio
async def test_create_source_already_exists(client: AsyncClient, test_db: AsyncSession):
    url = "http://example.com"
    new_source = SourceModel(url=url)
    test_db.add(new_source)
    await test_db.commit()

    payload = {"url": url}
    response = await client.post("/v1/urls/", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "source already exists"
"""