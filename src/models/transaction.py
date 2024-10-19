from pydantic import BaseModel
from typing import List
from datetime import datetime

class CreateTransactionResponse(BaseModel):
    id: str

class TransactionDTO(BaseModel):
    name: str
    buyer_id: str
    seller_id: str
    value: float
    created_at: datetime = None

# create table transaction(
# id UUID primary key DEFAULT (uuid_generate_v4()) NOT null,
# buyer_id UUID NOT NULL,
# seller_id UUID NOT NULL,
# value float not null,
# created_at TIMESTAMP NOT NULL DEFAULT (NOW() AT TIME ZONE 'America/Sao_Paulo'),
# FOREIGN KEY (buyer_id) REFERENCES "user"(id),
# FOREIGN KEY (seller_id) REFERENCES "user"(id)
# );
