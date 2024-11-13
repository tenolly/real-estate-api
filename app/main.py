import logging
from fastapi import FastAPI
from routers.v1 import v1_router
from database import Base, get_async_db, init_db


logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="logs.log"
)

async def startup():
    await init_db()


app = FastAPI(on_startup=[startup])
app.include_router(v1_router)
