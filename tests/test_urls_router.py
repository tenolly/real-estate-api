import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import SourceModel


URLS_ENDPOINT = "/v1/source-items/"


@pytest.mark.anyio
async def test_create_bad_source(client: AsyncClient):
    url = "http://some.com/"
    payload = {"url": url}

    response = await client.post(URLS_ENDPOINT, json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "source type could not be determined"


@pytest.mark.anyio
async def test_miss_body_and_query_params(client: AsyncClient):
    response = await client.post(URLS_ENDPOINT)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        response.json()["detail"]
        == "either json body or 'url' query parameter must be provided"
    )


@pytest.mark.anyio
async def test_create_valid_avito_source(client: AsyncClient):
    url = "https://www.avito.ru/sankt-peterburg/travel?cd=1"
    payload = {"url": url}

    response = await client.post(URLS_ENDPOINT, json=payload)
    assert response.status_code == 200
    assert response.json()["url"] == url

    response = await client.post(URLS_ENDPOINT, json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "source already exists"


@pytest.mark.anyio
async def test_get_avito_source_by_url(client: AsyncClient, test_db: AsyncSession):
    url = "https://www.avito.ru/sankt-peterburg/travel?cd=2"
    new_source = SourceModel(url=url, source_type="avito")
    test_db.add(new_source)
    await test_db.commit()
    await test_db.refresh(new_source)

    response = await client.get(f"{URLS_ENDPOINT}?url={url}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["url"] == url


@pytest.mark.anyio
async def test_get_avito_source_by_wrong_url(
    client: AsyncClient, test_db: AsyncSession
):
    url = "https://www.avito.ru/sankt-peterburg/ererg"
    response = await client.get(f"{URLS_ENDPOINT}?url={url}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "source not found"


@pytest.mark.anyio
async def test_get_avito_source_by_uuid(client: AsyncClient, test_db: AsyncSession):
    url = "https://www.avito.ru/sankt-peterburg/travel?cd=3"
    new_source = SourceModel(url=url, source_type="avito")
    test_db.add(new_source)
    await test_db.commit()
    await test_db.refresh(new_source)

    response = await client.get(f"{URLS_ENDPOINT}{new_source.uid}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["url"] == url


@pytest.mark.anyio
async def test_delete_avito_source_by_uuid(client: AsyncClient, test_db: AsyncSession):
    url = "https://www.avito.ru/sankt-peterburg/travel?cd=4"
    new_source = SourceModel(url=url, source_type="avito")
    test_db.add(new_source)
    await test_db.commit()
    await test_db.refresh(new_source)

    response = await client.delete(f"{URLS_ENDPOINT}{new_source.uid}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["detail"] == "source deleted"
