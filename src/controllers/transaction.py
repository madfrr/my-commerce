from fastapi import APIRouter, Depends, Response, Request, HTTPException, Query
from models.transaction import CreateTransactionResponse, CreateTransaction, FilterParams
from domain.transaction import TransactionDomain
from config import AppConfig
from data.repositories.transaction_repo import TransactionRepo
from typing import Annotated


router = APIRouter()

@router.post('/transaction', response_model=CreateTransactionResponse, status_code=201)
def create_transaction(request: Request, payload: CreateTransaction, response: Response, config: AppConfig = Depends(AppConfig)):    
    repo = TransactionRepo(db=request.app.state.db)
    
    transaction = TransactionDomain(repo=repo, config=config).create(payload)
    if transaction is None:
        raise HTTPException(status_code=500)
    response.status_code = 201

    return transaction

@router.get('/transaction', response_model=None)
def read_transaction(filter_query: Annotated[FilterParams, Query()], request: Request, response: Response, config: AppConfig = Depends(AppConfig)):
    repo = TransactionRepo(db=request.app.state.db)
    result = TransactionDomain(repo=repo, config=config).read(filter_query)
    if len(result.data) == 0:
        return Response(status_code=204)
    return result
