from typing import List
from models.user import UpdateUser, CreateUser
from data.repositories.abstract_repo import AbstractRepo


class UserRepo(AbstractRepo):
    def __init__(self, db):
        super().__init__(db)

    def create_user(self, UserDTO: CreateUser) -> str:
        query = """
        insert into "user"(name, email)
        values %s
        RETURNING id;
        """
        data = ((UserDTO.name, UserDTO.email),)
        id = self.db.execute_values(insert_query=query, data=data, fetch=True)
        return id[0][0]

    def update_user(self, user: UpdateUser):
        query = """
        UPDATE "user"
        SET ("name", email) = (%s, %s)
        WHERE id= %s;
        """
        data = (user.name, user.email, user.id)
        return self.db.execute(query, data)

    def read_user(self, id: str=None, email: str=None, format_output=False) -> List[dict]:
        query = """
        select id, "name", email
        from "user"
        where 1=1 
        """
        params = []
        if id is not None:
            query += "\nand id = %s"
            params.append(id)
        if email is not None:
            query += "\nand email = %s"
            params.append(email)

        result = self.db.execute(query, tuple(params))
        if format_output:
            return self.format_output(result)
        return result
    
    def delete_user(self, id: str) -> bool:
        query = """
        DELETE FROM "user"
        where id = %s
        """

        return self.db.execute(query, (id,))