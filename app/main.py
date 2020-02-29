from fastapi import FastAPI, Depends
from starlette.status import HTTP_200_OK
from starlette.responses import Response
from starlette.requests import Request
import uvicorn
from loguru import logger
from asyncpg.pool import Pool
import time

from app import setting
from app.services.database import Database
from app.repository.test_repository import test_query

logger.add(setting.LOG_NAME, rotation=setting.LOG_FILEROTATION)


app = FastAPI()

database = Database()


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


# TODO: Delete this router then add router that follows this format.
@app.get("/test", tags=["test"], status_code=HTTP_200_OK)
async def test_api(
        response: Response,
        db_pool: Pool = Depends(database.get_pool)):

    logger.info('Got incoming request')
    query = 'select * from analytics_elastic_clean limit 100'
    return await test_query(db_pool, query)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
