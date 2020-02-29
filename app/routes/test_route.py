from asyncpg.pool import Pool
from fastapi import APIRouter, Depends
from loguru import logger
from starlette.responses import Response
from starlette.status import HTTP_200_OK

from app.repository.test_repository import test_query
from app.services.database import database

router = APIRouter()


# TODO: Delete this router then add router that follows this format.
@router.get("/", tags=["test"], status_code=HTTP_200_OK)
async def test_api(
        response: Response,
        db_pool: Pool = Depends(database.get_pool)):

    logger.info('Got incoming request')
    query = 'select * from analytics_elastic_clean limit 100'
    return await test_query(db_pool, query)
