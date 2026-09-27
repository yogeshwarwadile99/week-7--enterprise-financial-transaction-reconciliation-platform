from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ExternalRecord(BaseModel):
    reference_number: str
    amount: float
    status: str

class ReconciliationRunResponse(BaseModel):
    id: int
    run_date: datetime
    status: str
    total_internal: int
    total_external: int
    matched: int
    mismatched: int

    class Config:
        from_attributes = True

class MismatchResponse(BaseModel):
    id: int
    reference_number: str
    internal_amount: Optional[float]
    external_amount: Optional[float]
    internal_status: Optional[str]
    external_status: Optional[str]
    mismatch_type: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
