from data.repositories.product_repo import ProductRepo
from models.product import CreateProduct, CreateProductResponse, ProductDTO, ListProductDTO, FilterParams, UpdateProduct
from exceptions import ProductDoesNotExist

class ProductDomain:
    def __init__(self, repo:ProductRepo, config):
        self.repo:ProductRepo = repo
        self.config = config

    def create(self, product: CreateProduct) -> CreateProductResponse:  
        id = self.repo.create_product(product)
        return CreateProductResponse(id=id)
    
    def update(self, product: UpdateProduct):
        return self.repo.update_product(product)
        
    def read(self, filter_query: FilterParams) -> ListProductDTO:
        user_id = filter_query.id
        name = filter_query.name
        products = self.repo.read_product(user_id, name)
        data = [ProductDTO(**product) for product in products]
        return ListProductDTO(data=data)
    
    def delete(self, id: str):
        product = self.repo.read_product(id, format_output=True)
        if len(product) == 0:
            raise ProductDoesNotExist()
        
        id = product[0].get("id")
        return self.repo.delete_product(id)