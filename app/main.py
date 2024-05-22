import time
import sys
import uuid

from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from loguru import logger
from starlette.requests import Request

from app import setting
from app.routes import test_route
from app.services.database import Database
from app.utils.utility_function import _trx_id_ctx_var
from app.services.authentication import auth
from app.repository.role_mgmt import get_cache_tag_role

logger.remove()
logger.add(sys.stdout, backtrace=False, diagnose=False)
logger.add(
    setting.LOG_NAME, rotation=setting.LOG_FILEROTATION, backtrace=False, diagnose=False
)


# Logic to be executed at startup and shutdown of the webservices
@asynccontextmanager
async def lifespan(app: FastAPI):
    database = Database()
    try:
        logger.info("Starting web services")
        logger.info("Creating connection to database")
        await database.connect()
        app.state.db_pool = database.pool
        if app.state.db_pool is not None:
            cache_tag_roles = await get_cache_tag_role(app.state.db_pool)
        if cache_tag_roles is not None:
            auth.set_cache(cache_tag_roles)
        logger.info("Connection to database has been successfully created")
        yield
    finally:
        logger.info("Closing connection to database")
        await database.disconnect()
        logger.info("Connection to database has been successfully closed")
        logger.info("Web services has been shutdown")


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    trx_id = uuid.uuid4()
    request_id = _trx_id_ctx_var.set(str(trx_id))
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["transaction_id"] = str(trx_id)
    response.headers["X-Process-Time"] = str(process_time)
    _trx_id_ctx_var.reset(request_id)
    return response


# TODO: Delete this router configuration then add router configuration that follows this format.
app.include_router(test_route.router, prefix="/test", tags=["test"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
