from fastapi import APIRouter, Depends, Response, Request, HTTPException, Query
from models.user import CreateUserResponse, CreateUser, FilterParams, UpdateUser
from domain.user import UserDomain
from config import AppConfig
from data.repositories.user_repo import UserRepo
from typing import Annotated


router = APIRouter()

@router.post('/user', response_model=CreateUserResponse, status_code=201)
def create_user(request: Request, payload: CreateUser, response: Response, config: AppConfig = Depends(AppConfig)):    
    repo = UserRepo(db=request.app.state.db)
    
    user = UserDomain(
        repo=repo, config=config).create(payload)
    if user is None:
        raise HTTPException(status_code=500)
    response.status_code = 201

    return user

@router.get('/user', response_model=None)
def read_user(filter_query: Annotated[FilterParams, Query()], request: Request, response: Response, config: AppConfig = Depends(AppConfig)):
    repo = UserRepo(db=request.app.state.db)
    result = UserDomain(repo=repo, config=config).read(filter_query)
    if len(result) == 0:
        return Response(status_code=204)
    return result

@router.patch('/user', response_model=None)
def update_user(request: Request, payload: UpdateUser, response: Response, config: AppConfig = Depends(AppConfig)):
    repo = UserRepo(db=request.app.state.db)
    UserDomain(repo=repo, config=config).update(payload)
    return Response(status_code=200)
    
@router.delete('/user', response_model=None)
def delete_user(request: Request, response: Response, id: str, config: AppConfig = Depends(AppConfig)):
    repo = UserRepo(db=request.app.state.db)
    UserDomain(repo=repo, config=config).delete(id)
    return Response(status_code=200)
