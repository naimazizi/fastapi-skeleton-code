import time
import sys
import uuid

import uvicorn
from fastapi import FastAPI
from loguru import logger
from starlette.requests import Request

from app import setting
from app.routes import test_route
from app.services.database import database
from app.utils.utility_function import _trx_id_ctx_var

logger.remove()
logger.add(
    sys.stdout,
    backtrace=False,
    diagnose=False)
logger.add(
    setting.LOG_NAME,
    rotation=setting.LOG_FILEROTATION,
    backtrace=False,
    diagnose=False)


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
    trx_id = uuid.uuid4()
    request_id = _trx_id_ctx_var.set(trx_id)
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["transaction_id"] = str(trx_id)
    response.headers["X-Process-Time"] = str(process_time)
    _trx_id_ctx_var.reset(request_id)
    return response


# TODO: Delete this router configuration then add router configuration that
#  follows this format.
app.include_router(
    test_route.router,
    prefix='/test',
    tags=['test'])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
