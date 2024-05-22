from typing import cast
from starlette.config import Config

config = Config(".env")


DB_HOST: str = config("DB_HOST", cast=str, default="localhost")

DB_PORT: str = config("DB_PORT", cast=str, default="5432")

DB_USERNAME: str = config("DB_USERNAME", cast=str, default="root")

DB_PASSWORD: str = config("DB_PASSWORD", cast=str, default="root")

DB_NAME: str = config("DB_NAME", cast=str, default="default")

DB_MIN_CONN_SIZE: int = cast(int, config("DB_MIN_CONN_SIZE", cast=int, default=10))

DB_MAX_CONN_SIZE: int = cast(int, config("DB_MAX_CONN_SIZE", cast=int, default=10))

DB_MAX_QUERIES: int = cast(int, config("DB_MAX_QUERIES", cast=int, default=50000))

DB_MAX_INACTIVE_CONN_LIFETIME: int = cast(
    int, config("DB_MAX_INACTIVE_CONN_LIFETIME", cast=int, default=300)
)

LOG_NAME: str = config("LOG_NAME", cast=str, default="log.log")

LOG_FILEROTATION: str = config("LOG_FILEROTATION", cast=str, default="1 MB")

JWT_SECRET_KEY: str = config("JWT_ALGORITHM", cast=str)

JWT_ALGORITHM: str = config("JWT_ALGORITHM", cast=str, default="HS256")
