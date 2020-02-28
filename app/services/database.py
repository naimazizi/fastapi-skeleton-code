import asyncpg
from loguru import logger


class Database():
    def __init__(
            self, user: str,
            password: str,
            database: str,
            host: str,
            port: str):

        self._conn_url = 'postgres://{user}:{password}'\
            '@{host}:{port}/{database}'.format(
                user=user, password=password, host=host,
                port=port, database=database)
        self.pool = None

    async def connect(self) -> None:
        if self.pool is None:
            self.pool = await asyncpg.create_pool(
                dsn=self._conn_url,
                min_size=10,  # in bytes,
                max_size=10,  # in bytes,
                max_queries=50000,
                max_inactive_connection_lifetime=300
                )
        else:
            raise asyncpg.exceptions.TooManyConnectionsError(
                'Connection pool has been created')

    async def disconnect(self) -> None:
        async with self.pool.acquire() as conn:
            await conn.close()

    def get_pool(self):
        try:
            yield self.pool
        except Exception:
            logger.error('Could not get database pool', catch=True)
