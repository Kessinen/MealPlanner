from fastapi import FastAPI
from contextlib import asynccontextmanager


from routes.meals import meal_router
from lib.logger import logger
from db import test_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    if not test_connection():
        logger.error("Database connection failed")
        exit(1)
    yield
    logger.info("Shutting down application...")


app = FastAPI(lifespan=lifespan)

app.include_router(meal_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
