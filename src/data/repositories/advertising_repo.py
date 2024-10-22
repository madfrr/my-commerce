from data.gevent_pgsql import AbstractDatabaseConnectionPool
from data.repositories.abstract_repo import AbstractRepo
from typing import List
from models.advertising import UpdateAdvertising, CreateAdvertising


class AdvertisingRepo(AbstractRepo):
    def __init__(self, db):
        self.db: AbstractDatabaseConnectionPool = db

    def create_advertising(self, advertising: CreateAdvertising) -> str:
        query = """
        insert into advertising(user_id, product_id, status, expiration_timestamp, quantity, unit_price)
        values %s
        RETURNING id;
        """
        data = (
            (
                advertising.user_id,
                advertising.product_id,
                advertising.status,
                advertising.expiration_timestamp,
                advertising.quantity,
                advertising.unit_price,
            ),
        )
        id = self.db.execute_values(insert_query=query, data=data, fetch=True)
        return id[0][0]

    def update_advertising(self, advertising: UpdateAdvertising):
        query = """
        UPDATE advertising
        SET (user_id, product_id, status, expiration_timestamp, quantity, unit_price) = (%s, %s, %s, %s, %s, %s)
        WHERE id= %s;
        """
        data = (
            advertising.user_id,
            advertising.product_id,
            advertising.status,
            advertising.expiration_timestamp,
            advertising.quantity,
            advertising.unit_price,
            advertising.id,
        )
        return self.db.execute(query, data)

    def read_advertising(
        self,
        id: int = None,
        user_id: str = None,
        product_id: int = None,
        format_output=False,
    ) -> List[dict]:
        query = """
        select 
            id, 
            user_id,
            product_id,
            status,
            expiration_timestamp,
            quantity,
            unit_price
        from advertising
        where 1=1 
        """
        params = []
        if id is not None:
            query += "\nand id = %s"
            params.append(id)

        if user_id is not None:
            query += "\nand user_id = %s"
            params.append(user_id)

        if product_id is not None:
            query += "\nand product_id = %s"
            params.append(product_id)

        result = self.db.execute(query, tuple(params))
        if format_output:
            return self.format_output(result)
        return result

    def delete_advertising(self, id: str) -> bool:
        query = """
        DELETE FROM advertising
        where id = %s
        """

        return self.db.execute(query, (id,))
