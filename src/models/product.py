from pydantic import BaseModel
from typing import List

class CreateProductResponse(BaseModel):
    id: str

class CreateProduct(BaseModel):
    name: str
    description: str
    pictures: List[str] = []

class UpdateProduct(BaseModel):
    id: str
    name: str | None
    description: str | None
    pictures: List[str] | List

class ProductDTO(BaseModel):
    id: str | None
    name: str | None
    description: str | None
    pictures: List[str] | List

class ListProductDTO(BaseModel):
    data: List[ProductDTO]

class FilterParams(BaseModel):
    id: str | None = None
    name: str | None = None
