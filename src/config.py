from os import getenv

from dotenv import load_dotenv
load_dotenv()


class AppConfig:
    app_prefix = '/api/my-commerce'
    application_name = getenv('APPLICATION_NAME')
    debug = bool(getenv('DEBUG', False))
    version = getenv('VERSION', '1.0.0')
    port = getenv('PORT', 5000)
    auth_token = getenv('AUTHORIZATION_TOKEN')

    docs_url = f'{app_prefix}/docs'
    redoc_url = f'{app_prefix}/redoc'

    class Database:
        CONNECTION_TIMEOUT = int(
            getenv("PGSQL_CONNECTION_TIMEOUT", 15))
        HOST = getenv("PGSQL_HOST")
        USER = getenv("PGSQL_USER")
        PASSWORD = getenv("PGSQL_PASSWORD")
        DBNAME = getenv("PGSQL_DBNAME")
        PORT = getenv("PGSQL_PORT")
