import os
import logging
from fastapi import FastAPI

from database import init_db
from routers.v1 import v1_router
from parsers.core import ParserManager


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="logs.log",
)


async def startup():
    ParserManager.load_parsers_from_yaml(
        os.path.join(os.path.dirname(__file__), "providers.yaml")
    )
    await init_db()


app = FastAPI(on_startup=[startup])
app.include_router(v1_router)
