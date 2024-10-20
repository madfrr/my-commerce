from data.gevent_pgsql import AbstractDatabaseConnectionPool
from data.repositories.abstract_repo import AbstractRepo
from typing import List
from models.transaction import CreateTransaction


class TransactionRepo(AbstractRepo):
    def __init__(self, db):
        self.db: AbstractDatabaseConnectionPool = db

    def create_transaction(self, transaction: CreateTransaction) -> str:
        query = """
        insert into transaction(buyer_id, seller_id, "value")
        values %s
        RETURNING id;
        """
        data = ((transaction.buyer_id, transaction.seller_id, transaction.value),)
        id = self.db.execute_values(insert_query=query, data=data, fetch=True)
        return id[0][0]

    def read_transaction(
        self,
        id: int = None,
        buyer_id: str = None,
        seller_id: int = None,
        format_output=False,
    ) -> List[dict]:
        query = """
        select 
            id, 
            buyer_id,
            seller_id,
            value,
            created_at
        from transaction
        where 1=1 
        """
        params = []
        if id is not None:
            query += "\nand id = %s"
            params.append(id)

        if buyer_id is not None:
            query += "\nand buyer_id = %s"
            params.append(buyer_id)

        if seller_id is not None:
            query += "\nand seller_id = %s"
            params.append(seller_id)

        result = self.db.execute(query, tuple(params))
        if format_output:
            return self.format_output(result)
        return result
