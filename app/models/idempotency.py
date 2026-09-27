from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class IdempotencyKey(Base):
    __tablename__ = "idempotency_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False, index=True)
    response = Column(String(500), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
