from fastapi import APIRouter, Depends, Response, Request, HTTPException, Query
from models.advertising import (
    CreateAdvertisingResponse,
    CreateAdvertising,
    FilterParams,
    UpdateAdvertising,
)
from domain.advertising import AdvertisingDomain
from config import AppConfig
from data.repositories.advertising_repo import AdvertisingRepo
from typing import Annotated


router = APIRouter()


@router.post("/advertising", response_model=CreateAdvertisingResponse, status_code=201)
def create_advertising(
    request: Request,
    payload: CreateAdvertising,
    response: Response,
    config: AppConfig = Depends(AppConfig),
):
    repo = AdvertisingRepo(db=request.app.state.db)

    advertising = AdvertisingDomain(repo=repo, config=config).create(payload)
    if advertising is None:
        raise HTTPException(status_code=500)
    response.status_code = 201

    return advertising


@router.get("/advertising", response_model=None)
def read_advertising(
    filter_query: Annotated[FilterParams, Query()],
    request: Request,
    response: Response,
    config: AppConfig = Depends(AppConfig),
):
    repo = AdvertisingRepo(db=request.app.state.db)
    result = AdvertisingDomain(repo=repo, config=config).read(filter_query)
    if len(result.data) == 0:
        return Response(status_code=204)
    return result


@router.patch("/advertising", response_model=None)
def update_advertising(
    request: Request,
    payload: UpdateAdvertising,
    response: Response,
    config: AppConfig = Depends(AppConfig),
):
    repo = AdvertisingRepo(db=request.app.state.db)
    AdvertisingDomain(repo=repo, config=config).update(payload)
    return Response(status_code=200)


@router.delete("/advertising", response_model=None)
def delete_advertising(
    request: Request,
    response: Response,
    id: str,
    config: AppConfig = Depends(AppConfig),
):
    repo = AdvertisingRepo(db=request.app.state.db)
    AdvertisingDomain(repo=repo, config=config).delete(id)
    return Response(status_code=200)
