from fastapi import APIRouter
from loguru import logger
from starlette.responses import Response
from starlette.requests import Request
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
from typing import Dict, List, Optional, Set

from app.repository.test_repository import test_query
from app.utils.utility_function import get_trx_id
from app.models.response import DatetimeValue
from app.repository.role_mgmt import get_cache_tag_role
from app.utils.constant import TAG_TEST


router = APIRouter()
tag = TAG_TEST


# TODO: Delete this router then add router that follows this format.
@router.get(
    "/", tags=[tag], status_code=HTTP_200_OK, response_model=List[DatetimeValue]
)
async def test_api(
    request: Request, response: Response
) -> Optional[List[DatetimeValue]]:
    trx_id = get_trx_id()
    logger.info("trx_id:{} - Got incoming request {}", trx_id, request.url.path)
    results = await test_query(request.app.state.db_pool)
    if results is None:
        response.status_code = HTTP_500_INTERNAL_SERVER_ERROR
    else:
        logger.info(
            "trx_id:{} - Success processing request {}", trx_id, request.url.path
        )
    return results


# TODO: Delete this router then add router that follows this format.
@router.get("/get_cache", tags=[tag], status_code=HTTP_200_OK)
async def get_cache(
    request: Request, response: Response
) -> Optional[Dict[str, Set[str]]]:
    trx_id = get_trx_id()
    logger.info("trx_id:{} - Got incoming request {}", trx_id, request.url.path)
    results = await get_cache_tag_role(request.app.state.db_pool)
    if results is None:
        response.status_code = HTTP_500_INTERNAL_SERVER_ERROR
    else:
        logger.info(
            "trx_id:{} - Success processing request {}", trx_id, request.url.path
        )
    return results
