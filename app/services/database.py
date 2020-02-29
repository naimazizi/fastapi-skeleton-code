import asyncpg

from app import setting


class Database():
    """
    Database class with singleton pattern.
    All database configuration are loaded from setting.
    """

    _instance = None
    _pool = None

    @classmethod
    async def connect(cls) -> None:
        """
        Asynchronously create connection pool to Postgres Database.
        This method should be called on application startup.
        """

        if cls._pool is None:
            dsn = cls._conn_url
            min_size = setting.DB_MIN_CONN_SIZE
            max_size = setting.DB_MAX_CONN_SIZE
            max_queries = setting.DB_MAX_QUERIES
            max_conn_lifetime = setting.DB_MAX_INACTIVE_CONN_LIFETIME

            cls._pool = await asyncpg.create_pool(
                dsn=dsn,
                min_size=min_size,
                max_size=max_size,
                max_queries=max_queries,
                max_inactive_connection_lifetime=max_conn_lifetime)

    async def disconnect(self) -> None:
        """
        Asynchronously disconnect connection pool
        """
        async with self.pool.acquire() as conn:
            await conn.close()

    @classmethod
    def get_pool(cls):
        """
        Method to get connection pool, can be used on dependency injection
        """
        yield cls._pool

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


database = Database()
