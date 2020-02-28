from fastapi import FastAPI, Depends
from starlette.status import HTTP_200_OK
from starlette.responses import Response
import uvicorn
from loguru import logger
from asyncpg.pool import Pool

import setting
from services.database import Database
from repository.test_repository import test_query

logger.add("service.log", rotation='10 MB')
logger.info('Starting web services')


app = FastAPI()


database = Database(
    user=setting.DB_USERNAME,
    password=setting.DB_PASSWORD,
    database=setting.DB_NAME,
    host=setting.DB_HOST,
    port=setting.DB_PORT
)


@app.on_event('startup')
async def startup() -> None:
    logger.info('Creating connection to database')
    await database.connect()
    logger.info('Connection to database has been successfully created')


@app.on_event('shutdown')
async def shutdown() -> None:
    logger.info('Closing connection to database')
    await database.disconnect()
    logger.info('Connection to database has been successfully closed')
    logger.info('Web services has been shutdown')


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
