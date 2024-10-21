from fastapi.testclient import TestClient
from data.gevent_pgsql import PostgresConnectionPool
from data.repositories.abstract_repo import AbstractRepo
from data import setup_db
from server import AppConfig, create_api
import pytest
import psycopg2


def postgresql_is_responsive(db_config: AppConfig.Database):
    try:
        print("Will try to connect to postgresql")
        pgsql = PostgresConnectionPool(
            host=db_config.HOST,
            dbname=db_config.DBNAME,
            user=db_config.USER,
            password=db_config.PASSWORD,
            port=db_config.PORT,
            maxsize=db_config.MAX_SIZE,
        )
        resp = pgsql.execute("select 1 as qtd;")
        resp = AbstractRepo(None).format_output(resp)
        if resp[0]["qtd"] == 1:
            return True
        with PostgresConnectionPool(
            host=db_config.host,
            dbname=db_config.dbname,
            user=db_config.user,
            password=db_config.password,
            port=db_config.port,
            maxsize=db_config.MAX_SIZE,
        ) as conn:
            if conn:
                return True
    except psycopg2.OperationalError:
        return False


@pytest.fixture(scope="session", autouse=True)
def servicos_compose(docker_ip, docker_services):
    """Garante que os serviços estejam no ar antes de rodar os testes"""
    docker_services.wait_until_responsive(
        timeout=10, pause=2, check=lambda: postgresql_is_responsive(AppConfig.Database)
    )


@pytest.fixture()
def client(servicos_compose):
    app = TestClient(create_api(AppConfig))
    app.app.state.db = setup_db()
    return app
