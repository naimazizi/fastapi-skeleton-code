from starlette.config import Config

config = Config('.env')

DB_HOST = config("DB_HOST", cast=str, default="localhost")
DB_PORT = config("DB_PORT", cast=str, default='5432')
DB_USERNAME = config("DB_USERNAME", cast=str, default="root")
DB_PASSWORD = config("DB_PASSWORD", cast=str, default="root")
DB_NAME = config("DB_NAME", cast=str, default="default")
