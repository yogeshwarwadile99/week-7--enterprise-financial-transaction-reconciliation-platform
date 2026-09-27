from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AccountCreate(BaseModel):
    customer_id: int
    currency: str = "INR"
    initial_balance: float = 0

class AccountStatusUpdate(BaseModel):
    status: str

class AccountResponse(BaseModel):
    id: int
    account_number: str
    customer_id: int
    currency: str
    available_balance: float
    ledger_balance: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
