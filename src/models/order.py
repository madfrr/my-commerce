from pydantic import BaseModel
from typing import List
from datetime import datetime

class CreateOrderResponse(BaseModel):
    id: str

class OrderDTO(BaseModel):
    name: str
    transaction_id: str
    advertising_id: int
    price: float
    created_at: datetime = None
