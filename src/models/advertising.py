from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta


class CreateAdvertisingResponse(BaseModel):
    id: int


class CreateAdvertising(BaseModel):
    user_id: str
    product_id: int
    status: str
    expiration_timestamp: datetime | None = datetime.now() + timedelta(days=7)
    quantity: int
    unit_price: float


class UpdateAdvertising(BaseModel):
    id: int
    user_id: str | None
    product_id: int | None
    status: str | None
    expiration_timestamp: datetime | None
    quantity: int | None
    unit_price: float | None


class AdvertisingDTO(BaseModel):
    id: int | None = None
    user_id: str | None = None
    product_id: int | None = None
    status: str | None = None
    expiration_timestamp: datetime | None = None
    quantity: int | None = None
    unit_price: float | None = None


class ListAdvertisingDTO(BaseModel):
    data: List[AdvertisingDTO]


class FilterParams(BaseModel):
    id: int | None = None
    user_id: str | None = None
    product_id: int | None = None
