from asyncpg.pool import Pool
from fastapi import APIRouter, Depends
from loguru import logger
from starlette.responses import Response
from starlette.requests import Request
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
from typing import List

from app.repository.test_repository import test_query
from app.services.database import database
from app.utils.utility_function import get_trx_id
from app.models.response import DatetimeValue


router = APIRouter()


# TODO: Delete this router then add router that follows this format.
@router.get(
    "/",
    tags=["test"],
    status_code=HTTP_200_OK,
    response_model=List[DatetimeValue])
async def test_api(
        request: Request,
        response: Response,
        db_pool: Pool = Depends(database.get_pool)):
    trx_id = get_trx_id()
    logger.info(
        'trx_id:{} - Got incoming request {}', trx_id, request.url.path)
    results = await test_query(trx_id, db_pool)
    if results is None:
        response.status_code = HTTP_500_INTERNAL_SERVER_ERROR
    else:
        logger.info(
            'trx_id:{} - Success processing request {}',
            trx_id, request.url.path)
    return results
