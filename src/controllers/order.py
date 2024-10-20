from fastapi import APIRouter, Depends, Response, Request, HTTPException, Query
from models.order import CreateOrderResponse, CreateOrder, FilterParams, UpdateOrder
from domain.order import OrderDomain
from config import AppConfig
from data.repositories.order_repo import OrderRepo
from typing import Annotated


router = APIRouter()

@router.post('/order', response_model=CreateOrderResponse, status_code=201)
def create_order(request: Request, payload: CreateOrder, response: Response, config: AppConfig = Depends(AppConfig)):    
    repo = OrderRepo(db=request.app.state.db)
    
    order = OrderDomain(repo=repo, config=config).create(payload)
    if order is None:
        raise HTTPException(status_code=500)
    response.status_code = 201

    return order

@router.get('/order', response_model=None)
def read_order(filter_query: Annotated[FilterParams, Query()], request: Request, response: Response, config: AppConfig = Depends(AppConfig)):
    repo = OrderRepo(db=request.app.state.db)
    result = OrderDomain(repo=repo, config=config).read(filter_query)
    if len(result.data) == 0:
        return Response(status_code=204)
    return result

@router.patch('/order', response_model=None)
def update_order(request: Request, payload: UpdateOrder, response: Response, config: AppConfig = Depends(AppConfig)):
    repo = OrderRepo(db=request.app.state.db)
    OrderDomain(repo=repo, config=config).update(payload)
    return Response(status_code=200)
    
@router.delete('/order', response_model=None)
def delete_order(request: Request, response: Response, id: str, config: AppConfig = Depends(AppConfig)):
    repo = OrderRepo(db=request.app.state.db)
    OrderDomain(repo=repo, config=config).delete(id)
    return Response(status_code=200)
