from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
import enum

class TransactionStatus(str, enum.Enum):
    INITIATED = "INITIATED"
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REVERSAL_REQUESTED = "REVERSAL_REQUESTED"
    REVERSED = "REVERSED"

class TransactionType(str, enum.Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"
    TRANSFER = "TRANSFER"
    REFUND = "REFUND"
    REVERSAL = "REVERSAL"

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    reference_number = Column(String(50), unique=True, nullable=False)
    sender_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    receiver_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="INR")
    transaction_type = Column(Enum(TransactionType), nullable=False)
    channel = Column(String(50), default="INTERNAL")
    status = Column(Enum(TransactionStatus), default=TransactionStatus.INITIATED)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)
