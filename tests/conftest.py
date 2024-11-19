from asyncio import get_event_loop

import pytest
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.main import app
from models import Base
from database import TEST_DATABASE_URL, get_async_db


test_async_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestAsyncSessionLocal = sessionmaker(
    bind=test_async_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="module")
async def setup_database():
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def test_db(setup_database):
    async with TestAsyncSessionLocal() as session:
        yield session


@pytest.fixture(scope="function")
async def client(setup_database, test_db):
    async def _test_get_async_db():
        yield test_db

    app.dependency_overrides[get_async_db] = _test_get_async_db
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="module")
def event_loop():
    loop = get_event_loop()
    yield loop


@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"
