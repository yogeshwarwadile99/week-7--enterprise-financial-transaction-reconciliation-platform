from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum

class ReconciliationStatus(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class ReconciliationRun(Base):
    __tablename__ = "reconciliation_runs"
    
    id = Column(Integer, primary_key=True, index=True)
    run_date = Column(DateTime, server_default=func.now())
    status = Column(Enum(ReconciliationStatus), default=ReconciliationStatus.PENDING)
    total_internal = Column(Integer, default=0)
    total_external = Column(Integer, default=0)
    matched = Column(Integer, default=0)
    mismatched = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)
