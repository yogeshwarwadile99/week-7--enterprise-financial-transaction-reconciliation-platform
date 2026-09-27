from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.schemas.transaction import TransactionCreate
from app.services.transaction_service import TransactionService
from app.middleware.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/v1/transactions", tags=["Transactions"])

@router.post("/")
async def create_transaction(
    txn_data: TransactionCreate,
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    txn = TransactionService.create_transaction(db, txn_data, current_user.id, idempotency_key)
    return {"success": True, "message": "Transaction processed", "data": txn}

@router.get("/")
async def get_all_transactions(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    txns = TransactionService.get_all_transactions(db)
    return {"success": True, "data": txns}

@router.get("/{txn_id}")
async def get_transaction(txn_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    txn = TransactionService.get_transaction_by_id(db, txn_id)
    return {"success": True, "data": txn}

@router.post("/{txn_id}/cancel")
async def cancel_transaction(txn_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    txn = TransactionService.cancel_transaction(db, txn_id, current_user.id)
    return {"success": True, "message": "Cancellation requested", "data": txn}
