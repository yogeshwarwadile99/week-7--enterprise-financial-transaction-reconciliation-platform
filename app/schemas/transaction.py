from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TransactionCreate(BaseModel):
    sender_account_id: Optional[int] = None
    receiver_account_id: Optional[int] = None
    amount: float
    currency: str = "INR"
    transaction_type: str
    channel: str = "INTERNAL"
    description: Optional[str] = None

class TransactionResponse(BaseModel):
    id: int
    reference_number: str
    sender_account_id: Optional[int]
    receiver_account_id: Optional[int]
    amount: float
    currency: str
    transaction_type: str
    channel: str
    status: str
    description: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True
