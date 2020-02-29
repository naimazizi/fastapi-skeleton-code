from starlette.config import Config

config = Config('.env')


DB_HOST = config("DB_HOST", cast=str, default="localhost")

DB_PORT = config("DB_PORT", cast=str, default='5432')

DB_USERNAME = config("DB_USERNAME", cast=str, default="root")

DB_PASSWORD = config("DB_PASSWORD", cast=str, default="root")

DB_NAME = config("DB_NAME", cast=str, default="default")

DB_MIN_CONN_SIZE = config("DB_MIN_CONN_SIZE", cast=int, default="10")

DB_MAX_CONN_SIZE = config("DB_MAX_CONN_SIZE", cast=int, default="10")

DB_MAX_QUERIES = config("DB_MAX_QUERIES", cast=int, default="50000")

DB_MAX_INACTIVE_CONN_LIFETIME = config(
    "DB_MAX_INACTIVE_CONN_LIFETIME",
    cast=int,
    default="300")

LOG_NAME = config("LOG_NAME", cast=str, default="log.log")

LOG_FILEROTATION = config("LOG_FILEROTATION", cast=str, default="1 MB")
