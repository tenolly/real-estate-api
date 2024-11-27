import os
import logging

from fastapi import FastAPI

from routers.v1 import v1_router
from parsers.core import ParserManager


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="logs.log",
)

ParserManager.init()

app = FastAPI()
app.include_router(v1_router)
