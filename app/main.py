import logging

from fastapi import FastAPI

from update import UpdateService
from routers.v1 import v1_router
from parsers.core import ParserManager


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="app.log",
)

ParserManager.init()


async def startup():
    service = UpdateService()
    service.start()


app = FastAPI(on_startup=[startup])
app.include_router(v1_router)
