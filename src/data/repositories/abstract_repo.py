from data.gevent_pgsql import AbstractDatabaseConnectionPool


class AbstractRepo:
    def __init__(self, db):
        self.db: AbstractDatabaseConnectionPool = db

    def format_output(self, cursor):
        columns = [value.name for value in cursor.description]
        data = [dict(zip(columns, row)) for row in cursor]
        return data
