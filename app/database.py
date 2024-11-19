import asyncio

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from models import Base
from config import Config


CONFIG = Config()
DATABASE_URL_PREFIX = f"postgresql+asyncpg://{CONFIG.POSTGRES_USER}:{CONFIG.POSTGRES_PASSWORD}@{CONFIG.POSTGRES_HOST}:{CONFIG.POSTGRES_PORT}/"


# Production

DATABASE_URL = DATABASE_URL_PREFIX + CONFIG.POSTGRES_DB
async_engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session


# Pytest

TEST_DATABASE_URL = DATABASE_URL_PREFIX + CONFIG.POSTGRES_TEST_DB


# Init database


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def init_db():
    await create_tables()


if __name__ == "__main__":
    asyncio.run(init_db())
