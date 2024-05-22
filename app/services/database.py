import asyncpg

from app import setting


class Database:
    """
    Database class with singleton pattern.
    All database configuration are loaded from setting.
    """

    pool = None
    _conn_url: str = "postgres://{user}:{password}" "@{host}:{port}/{database}".format(
        user=setting.DB_USERNAME,
        password=setting.DB_PASSWORD,
        host=setting.DB_HOST,
        port=setting.DB_PORT,
        database=setting.DB_NAME,
    )

    def __init__(self):
        pass

    async def connect(self) -> None:
        """
        Asynchronously create connection pool to Postgres Database.
        This method should be called on application startup.
        """
        dsn = self._conn_url
        min_size: int = setting.DB_MIN_CONN_SIZE
        max_size: int = setting.DB_MAX_CONN_SIZE
        max_queries: int = setting.DB_MAX_QUERIES
        max_conn_lifetime: int = setting.DB_MAX_INACTIVE_CONN_LIFETIME

        self.pool = await asyncpg.create_pool(
            dsn=dsn,
            min_size=min_size,
            max_size=max_size,
            max_queries=max_queries,
            max_inactive_connection_lifetime=max_conn_lifetime,
        )

    async def disconnect(self) -> None:
        """
        Asynchronously disconnect connection pool
        """
        if self.pool is not None:
            async with self.pool.acquire() as conn:
                await conn.close()
