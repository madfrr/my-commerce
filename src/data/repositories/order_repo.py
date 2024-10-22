from data.gevent_pgsql import AbstractDatabaseConnectionPool
from data.repositories.abstract_repo import AbstractRepo
from typing import List
from models.order import CreateOrder, UpdateOrder


class OrderRepo(AbstractRepo):
    def __init__(self, db):
        self.db: AbstractDatabaseConnectionPool = db

    def create_order(self, order: CreateOrder) -> str:
        query = """
        insert into "order"(transaction_id, advertising_id, price)
        values %s
        RETURNING id;
        """
        data = ((order.transaction_id, order.advertising_id, order.price),)
        id = self.db.execute_values(insert_query=query, data=data, fetch=True)
        return id[0][0]

    def update_order(self, order: UpdateOrder):
        query = """
        UPDATE "order"
        SET (transaction_id, advertising_id, price) = (%s, %s, %s)
        WHERE id= %s;
        """
        data = (
            order.transaction_id,
            order.advertising_id,
            order.price,
            order.id,
        )
        return self.db.execute(query, data)

    def read_order(
        self,
        id: int = None,
        transaction_id: str = None,
        advertising_id: int = None,
        format_output=False,
    ) -> List[dict]:
        query = """
        select 
            id, 
            transaction_id,
            advertising_id,
            price,
            created_at
        from "order"
        where 1=1 
        """
        params = []
        if id is not None:
            query += "\nand id = %s"
            params.append(id)

        if transaction_id is not None:
            query += "\nand transaction_id = %s"
            params.append(transaction_id)

        if advertising_id is not None:
            query += "\nand advertising_id = %s"
            params.append(advertising_id)

        result = self.db.execute(query, tuple(params))
        if format_output:
            return self.format_output(result)
        return result

    def delete_order(self, id: int) -> bool:
        query = """
        DELETE FROM "order"
        where id = %s
        """

        return self.db.execute(query, (id,))
