from asyncpg.pool import Pool
from typing import List

from app.utils.utility_function import query_and_log
from app.models.response import DatetimeValue


# TODO: Delete this repository then add repository that follows this format.
async def test_query(
        trx_id: str,
        db_pool: Pool,
        condition: str = None) -> List[DatetimeValue]:

    query = '''
    select t1.date::timestamp as datetime, t1.count as value from (
        select
            to_timestamp(cast(timestamp/1e6 as bigint))::date as date,
            count(*) as count
        from analytics_elastic_clean
        group by 1
    ) t1;
    '''

    results = None
    async with db_pool.acquire() as connection:
        results = await query_and_log(connection, query)

    return results
