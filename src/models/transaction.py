from pydantic import BaseModel
from typing import List
from datetime import datetime

class CreateTransactionResponse(BaseModel):
    id: str

class CreateTransaction(BaseModel):
    buyer_id: str
    seller_id: str
    value: float
    created_at: datetime = None

class UpdateTransaction(BaseModel):
    id: str
    buyer_id: str | None
    seller_id: str | None
    value: float | None

class TransactionDTO(BaseModel):
    id: str | None = None
    buyer_id: str | None = None
    seller_id: str | None = None
    value: float | None = None
    created_at: datetime | None = None

class ListTransactionDTO(BaseModel):
    data: List[TransactionDTO]

class FilterParams(BaseModel):
    id: str | None = None
    buyer_id: str | None = None
    seller_id: str | None = None
