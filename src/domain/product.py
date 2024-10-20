from data.repositories.product_repo import ProductRepo
from data.repositories.file_repo import FileRepo
from models.product import (
    CreateProduct,
    CreateProductResponse,
    ProductDTO,
    ListProductDTO,
    FilterParams,
    UpdateProduct,
    CreatedFilesResponse,
)
from exceptions import ProductDoesNotExist, InvalidImageType, FileTooBig, FileNotExists
from typing import List
from utils.logger import logger
import uuid

ALLOWED_IMAGE_TYPES = ("image/jpeg", "image/png", "image/jpg")
TAG = "[ProductDomain] |"


class ProductDomain:
    def __init__(self, product_repo: ProductRepo = None, file_repo: FileRepo = None, config=None):
        self.product_repo: ProductRepo = product_repo
        self.file_repo: FileRepo = file_repo

        self.config = config

    def _check_if_pictures_exists(self, pictures: List[str]):
        for pic in pictures:
            if not self.file_repo.file_exists(pic):
                raise FileNotExists(pic)

    def create(self, product: CreateProduct) -> CreateProductResponse:
        self._check_if_pictures_exists(product.pictures)
        id = self.product_repo.create_product(product)
        return CreateProductResponse(id=id)

    def _validate_image_time(self, content_type):
        if content_type not in ALLOWED_IMAGE_TYPES:
            raise InvalidImageType(content_type, ALLOWED_IMAGE_TYPES)

    def _validate_max_file_size(self, file_size: int):
        """
        file_size: Image file size in Bytes. Ex.: 40.04KB -> 41000B
        max_file_size = 5MB
        """
        MAX_FILE_SIZE = 5 * 1024 * 1024
        if file_size > MAX_FILE_SIZE:
            raise FileTooBig()

    def _generate_file_name(self, user_id: str, filename: str):
        extension = filename.split(".")[-1]
        return user_id + "_" + str(uuid.uuid4()) + "." + extension

    def create_file(self, user_id: str, files: list) -> CreatedFilesResponse:
        links = []
        for file in files:
            self._validate_image_time(file.content_type)
            self._validate_max_file_size(file.size)

            file_name = self._generate_file_name(user_id, file.filename)
            link = self.file_repo.save_picture(
                file=file.file.read(),
                file_name=file_name,
                content_type=file.content_type,
            )
            links.append(link)
        return CreatedFilesResponse(files=links)

    def update(self, product: UpdateProduct):
        self._check_if_pictures_exists(product.pictures)
        return self.product_repo.update_product(product)

    def read(self, filter_query: FilterParams) -> ListProductDTO:
        user_id = filter_query.id
        name = filter_query.name
        products = self.product_repo.read_product(user_id, name)
        data = [ProductDTO(**product) for product in products]
        return ListProductDTO(data=data)

    def delete_files(self, files: List[str]):
        for file in files:
            self.file_repo.delete_file(file_uri=file)

    def delete(self, id: str):
        product = self.product_repo.read_product(id, format_output=True)
        if len(product) == 0:
            raise ProductDoesNotExist()

        product = product[0]
        id = product.get("id")
        files = product.get("pictures")

        success_deleted = self.product_repo.delete_product(id)

        if not success_deleted:
            logger.error(f"{TAG} {success_deleted}")

        self.delete_files(files)
