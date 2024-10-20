from data.repositories.abstract_repo import AbstractRepo
from typing import List
from models.product import UpdateProduct


class ProductRepo(AbstractRepo):
    def __init__(self, db):
        super().__init__(db)

    def create_product(self, ProductDTO) -> str:
        query = """
        insert into product("name", description, pictures)
        values %s
        RETURNING id;
        """
        data = ((ProductDTO.name, ProductDTO.description, ProductDTO.pictures),)
        id = self.db.execute_values(insert_query=query, data=data, fetch=True)
        return id[0][0]

    def update_product(self, product: UpdateProduct):
        query = """
        UPDATE product
        SET ("name", description, pictures) = (%s, %s, %s)
        WHERE id= %s;
        """
        data = (product.name, product.description, product.pictures, product.id)
        return self.db.execute(query, data)

    def read_product(self, id: str=None, name: str=None, format_output=False) -> List[dict]:
        query = """
        select id, "name", description, pictures
        from product
        where 1=1 
        """
        params = []
        if id is not None:
            query += "\nand id = %s"
            params.append(id)

        if name is not None:
            query += "\nand name = %s"
            params.append(name)

        result = self.db.execute(query, tuple(params))
        if format_output:
            return self.format_output(result)
        return result
    
    def delete_product(self, id: str) -> bool:
        query = """
        DELETE FROM product
        where id = %s
        """

        return self.db.execute(query, (id,))