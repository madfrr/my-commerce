from data.gevent_pgsql import AbstractDatabaseConnectionPool

class Repo:
    def __init__(self, db):
        self.db:AbstractDatabaseConnectionPool = db

    def create_user(self, UserDTO) -> str:
        query = """
        insert into "user"(name, email)
        values %s
        RETURNING id;
        """
        data = ((UserDTO.name, UserDTO.email),)
        id = self.db.execute_values(insert_query=query, data=data, fetch=True)
        return id[0][0]
