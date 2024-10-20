from fastapi import APIRouter, Depends, Response, Request, HTTPException, Query
from models.product import CreateProductResponse, CreateProduct, FilterParams, UpdateProduct
from domain.product import ProductDomain
from config import AppConfig
from data.repositories.product_repo import ProductRepo
from typing import Annotated


router = APIRouter()

@router.post('/product', response_model=CreateProductResponse, status_code=201)
def create_product(request: Request, payload: CreateProduct, response: Response, config: AppConfig = Depends(AppConfig)):    
    repo = ProductRepo(db=request.app.state.db)
    
    product = ProductDomain(repo=repo, config=config).create(payload)
    if product is None:
        raise HTTPException(status_code=500)
    response.status_code = 201

    return product

@router.get('/product', response_model=None)
def read_product(filter_query: Annotated[FilterParams, Query()], request: Request, response: Response, config: AppConfig = Depends(AppConfig)):
    repo = ProductRepo(db=request.app.state.db)
    result = ProductDomain(repo=repo, config=config).read(filter_query)
    if len(result.data) == 0:
        return Response(status_code=204)
    return result

@router.patch('/product', response_model=None)
def update_product(request: Request, payload: UpdateProduct, response: Response, config: AppConfig = Depends(AppConfig)):
    repo = ProductRepo(db=request.app.state.db)
    ProductDomain(repo=repo, config=config).update(payload)
    return Response(status_code=200)
    
@router.delete('/product', response_model=None)
def delete_product(request: Request, response: Response, id: str, config: AppConfig = Depends(AppConfig)):
    repo = ProductRepo(db=request.app.state.db)
    ProductDomain(repo=repo, config=config).delete(id)
    return Response(status_code=200)
