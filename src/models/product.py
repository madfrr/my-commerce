from pydantic import BaseModel
from typing import List


class CreateProductResponse(BaseModel):
    id: int


class CreateProduct(BaseModel):
    name: str
    description: str
    pictures: List[str]


class UpdateProduct(BaseModel):
    id: int
    name: str | None
    description: str | None
    pictures: List[str] | List


class ProductDTO(BaseModel):
    id: int | None
    name: str | None
    description: str | None
    pictures: List[str] | List


class ListProductDTO(BaseModel):
    data: List[ProductDTO]


class FilterParams(BaseModel):
    id: int | None = None
    name: str | None = None


class CreatedFilesResponse(BaseModel):
    files: List[str] = []
