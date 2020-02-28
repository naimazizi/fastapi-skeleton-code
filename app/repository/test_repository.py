from asyncpg import Record
from asyncpg.pool import Pool


# TODO: Delete this repository then add repository that follows this format.
async def test_query(db_pool: Pool, query: str) -> Record:
    results = None
    async with db_pool.acquire() as connection:
        results = await connection.fetch(query)
    return results
