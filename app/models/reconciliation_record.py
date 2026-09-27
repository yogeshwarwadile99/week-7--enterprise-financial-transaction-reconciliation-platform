from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class ReconciliationRecord(Base):
    __tablename__ = "reconciliation_records"
    
    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("reconciliation_runs.id"), nullable=False)
    reference_number = Column(String(50), nullable=False)
    internal_amount = Column(Float, nullable=True)
    external_amount = Column(Float, nullable=True)
    internal_status = Column(String(20), nullable=True)
    external_status = Column(String(20), nullable=True)
    mismatch_type = Column(String(30), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
