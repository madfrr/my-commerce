from config import AppConfig
from data.gevent_pgsql import PostgresConnectionPool
from psycopg2.extras import DictCursor


def setup_db(config: AppConfig = AppConfig):
    return PostgresConnectionPool(
        dbname=config.StonelogDatabase.DBNAME,
        user=config.StonelogDatabase.USER,
        password=config.StonelogDatabase.PASSWORD,
        host=config.StonelogDatabase.HOST,
        port=config.StonelogDatabase.PORT,
        maxsize=10,
        cursor_factory=DictCursor)
