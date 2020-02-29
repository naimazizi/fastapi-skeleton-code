from asyncpg.pool import Pool
from typing import Dict, Set, Optional

from app.utils.utility_function import query_and_log


async def get_cache_tag_role(
        db_pool: Pool,
        condition: str = None) -> Optional[Dict[str, Set[str]]]:

    query = '''
    select tag, array_agg(role) as roles
    from tag_auth ta
    group by 1
    '''

    results = None
    async with db_pool.acquire() as connection:
        results = await query_and_log(connection, query)

    if results is not None:
        _result = dict()
        for res in results:
            _result[res['tag']] = set(res['roles'])
        results = _result
    return results
