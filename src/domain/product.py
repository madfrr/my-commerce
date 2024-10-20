from data.repositories.product_repo import ProductRepo
from data.repositories.file_repo import FileRepo
from models.product import CreateProduct, CreateProductResponse, ProductDTO, ListProductDTO, FilterParams, UpdateProduct, CreatedFilesResponse
from exceptions import ProductDoesNotExist, InvalidImageType, FileTooBig
import uuid

ALLOWED_IMAGE_TYPES = (
    'image/jpeg',
    'image/png',
    'image/jpg'
)

class ProductDomain:
    def __init__(self, repo:ProductRepo, config):
        self.repo:ProductRepo | FileRepo = repo
        self.config = config

    def create(self, product: CreateProduct) -> CreateProductResponse:  
        id = self.repo.create_product(product)
        return CreateProductResponse(id=id)

    def _validate_image_time(self, content_type):
        if content_type not in ALLOWED_IMAGE_TYPES:
            raise InvalidImageType(content_type, ALLOWED_IMAGE_TYPES)

    def _validate_max_file_size(self, file_size: int):
        '''
        file_size: Image file size in Bytes. Ex.: 40.04KB -> 41000B
        max_file_size = 5MB
        '''
        MAX_FILE_SIZE = 5 * 1024 * 1024
        if file_size > MAX_FILE_SIZE:
            raise FileTooBig()

    def _generate_file_name(self, user_id: str, filename: str):
        extension = filename.split(".")[-1]
        return user_id + "_" + str(uuid.uuid4()) + "." + extension

    def create_file(self, user_id:str , files: list) -> CreatedFilesResponse:
        links = []
        for file in files:
            self._validate_image_time(file.content_type)
            self._validate_max_file_size(file.size)

            file_name = self._generate_file_name(user_id, file.filename)
            link = self.repo.save_picture(
                file=file.file.read(),
                file_name=file_name,
                bucket_name="my_commerce_product_images",
                content_type=file.content_type,
            )
            links.append(link)
        return CreatedFilesResponse(files=links)

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