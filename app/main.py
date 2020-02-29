import time

import uvicorn
from fastapi import FastAPI
from loguru import logger
from starlette.requests import Request

from app import setting
from app.routes import test_route
from app.services.database import database

logger.add(setting.LOG_NAME, rotation=setting.LOG_FILEROTATION)


app = FastAPI()


@app.on_event('startup')
async def startup() -> None:
    logger.info('Starting web services')
    logger.info('Creating connection to database')
    await database.connect()
    logger.info('Connection to database has been successfully created')


@app.on_event('shutdown')
async def shutdown() -> None:
    logger.info('Closing connection to database')
    await database.disconnect()
    logger.info('Connection to database has been successfully closed')
    logger.info('Web services has been shutdown')


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(
    test_route.router,
    prefix='/test',
    tags=['test'])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
