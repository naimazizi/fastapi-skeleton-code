import asyncpg
from loguru import logger
from app import setting


class Database():
    """
    Database class with singleton pattern.
    All database configuration are loaded from setting.
    """

    _instance = None

    def __init__(self):
        self.pool = None

    async def connect(self) -> None:
        """
        Asynchronously create connection pool to Postgres Database.
        This method should be called on application startup.
        """

        if self.pool is None:
            dsn = self._conn_url
            min_size = setting.DB_MIN_CONN_SIZE
            max_size = setting.DB_MAX_CONN_SIZE
            max_queries = setting.DB_MAX_QUERIES
            max_conn_lifetime = setting.DB_MAX_INACTIVE_CONN_LIFETIME

            self.pool = await asyncpg.create_pool(
                dsn=dsn,
                min_size=min_size,
                max_size=max_size,
                max_queries=max_queries,
                max_inactive_connection_lifetime=max_conn_lifetime)
        else:
            raise asyncpg.exceptions.TooManyConnectionsError(
                'Connection pool has been created')

    async def disconnect(self) -> None:
        """
        Asynchronously disconnect connection pool
        """
        async with self.pool.acquire() as conn:
            await conn.close()

    def get_pool(self):
        """
        Method to get connection pool, can be used on dependency injection
        """
        try:
            yield self.pool
        except Exception:
            logger.error('Could not get database pool', catch=True)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._conn_url = 'postgres://{user}:{password}'\
                '@{host}:{port}/{database}'.format(
                    user=setting.DB_USERNAME,
                    password=setting.DB_PASSWORD,
                    host=setting.DB_HOST,
                    port=setting.DB_PORT,
                    database=setting.DB_NAME)
        return cls._instance
