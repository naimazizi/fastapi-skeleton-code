from loguru import logger
from asyncpg.pool import PoolConnectionProxy
from asyncpg.exceptions import (
    UndefinedColumnError,
    UndefinedObjectError,
    UndefinedTableError,
    UndefinedParameterError,
    AmbiguousAliasError,
    WrongObjectTypeError,
)
from asyncpg import Record
from contextvars import ContextVar
from typing import List, Optional


_trx_id_ctx_var: ContextVar[Optional[str]] = ContextVar("trx_id", default=None)


def get_trx_id() -> Optional[str]:
    return _trx_id_ctx_var.get()


async def query_and_log(
    connection: PoolConnectionProxy, query: str, *args
) -> Optional[List[Record]]:
    results = None
    try:
        results = await connection.fetch(query, *args)
    except (
        ValueError,
        UndefinedColumnError,
        UndefinedObjectError,
        UndefinedParameterError,
        UndefinedTableError,
        AmbiguousAliasError,
        WrongObjectTypeError,
    ):
        logger.opt(exception=True, depth=1).error(
            "Found error on query result, check used query: \n{}", query
        )
    except Exception:
        logger.opt(exception=True, depth=1).error("Could not get database pool")
    return results


async def insert_and_log(connection: PoolConnectionProxy, query: str, *args) -> None:
    try:
        await connection.execute(query, *args)
    except (
        ValueError,
        UndefinedColumnError,
        UndefinedObjectError,
        UndefinedParameterError,
        UndefinedTableError,
        AmbiguousAliasError,
        WrongObjectTypeError,
    ):
        logger.opt(exception=True, depth=1).error(
            "Found error on insert query, check used query: \n{}", query
        )
    except Exception:
        logger.opt(exception=True, depth=1).error("Could not get database pool")
