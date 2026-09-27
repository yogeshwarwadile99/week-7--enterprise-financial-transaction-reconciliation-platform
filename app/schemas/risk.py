from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RiskAlertResponse(BaseModel):
    id: int
    transaction_id: Optional[int]
    account_id: Optional[int]
    rule_triggered: str
    severity: str
    description: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class RiskReviewUpdate(BaseModel):
    status: str
