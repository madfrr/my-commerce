from pydantic import BaseModel
from typing import List
from datetime import datetime


class CreateOrderResponse(BaseModel):
    id: int


class CreateOrder(BaseModel):
    transaction_id: str
    advertising_id: int
    price: float
    created_at: datetime | None = None


class UpdateOrder(BaseModel):
    id: int
    transaction_id: str | None
    advertising_id: int | None
    price: float | None


class OrderDTO(BaseModel):
    id: int | None = None
    transaction_id: str | None = None
    advertising_id: int | None = None
    price: float | None = None
    created_at: datetime | None = None


class ListOrderDTO(BaseModel):
    data: List[OrderDTO]


class FilterParams(BaseModel):
    id: str | None = None
    transaction_id: str | None = None
    advertising_id: int | None = None
