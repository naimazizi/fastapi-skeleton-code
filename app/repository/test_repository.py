from asyncpg.pool import Pool
from typing import List, Optional, cast
from datetime import date

from app.utils.utility_function import query_and_log
from app.models.response import DatetimeValue


# TODO: Delete this repository then add repository that follows this format.
async def test_query(
    db_pool: Pool, condition: Optional[str] = None
) -> Optional[List[DatetimeValue]]:
    query = """
    select t1.date::timestamp as datetime, t1.count as value from (
        select
            to_timestamp(cast(timestamp/1e6 as bigint))::date as date,
            count(*) as count
        from analytics_elastic_clean
        where
            to_timestamp(cast(timestamp/1e6 as bigint))::date >= $1
            and to_timestamp(cast(timestamp/1e6 as bigint))::date <= $2
        group by 1
    ) t1;
    """

    results = None
    async with db_pool.acquire() as connection:
        results = await query_and_log(
            connection, query, date(2010, 1, 1), date(2020, 1, 20)
        )

    return cast(List[DatetimeValue], results)
