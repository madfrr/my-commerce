from config import AppConfig
from data.gevent_pgsql import PostgresConnectionPool
from psycopg2.extras import DictCursor


def setup_db(config: AppConfig = AppConfig):
    return PostgresConnectionPool(
        dbname=config.Database.DBNAME,
        user=config.Database.USER,
        password=config.Database.PASSWORD,
        host=config.Database.HOST,
        port=config.Database.PORT,
        maxsize=10,
        cursor_factory=DictCursor,
    )
