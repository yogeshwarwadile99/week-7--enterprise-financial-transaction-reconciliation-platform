from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.account import AccountCreate, AccountStatusUpdate
from app.services.account_service import AccountService
from app.middleware.auth import get_current_user, require_roles
from app.models.user import User

router = APIRouter(prefix="/api/v1/accounts", tags=["Accounts"])

@router.post("/")
async def create_account(account_data: AccountCreate, db: Session = Depends(get_db)):
    account = AccountService.create_account(db, account_data)
    return {"success": True, "message": "Account created", "data": account}

@router.get("/")
async def get_all_accounts(db: Session = Depends(get_db)):
    accounts = AccountService.get_all_accounts(db)
    return {"success": True, "data": accounts}

@router.get("/{account_id}")
async def get_account(account_id: int, db: Session = Depends(get_db)):
    account = AccountService.get_account_by_id(db, account_id)
    return {"success": True, "data": account}

@router.patch("/{account_id}/status")
async def update_status(account_id: int, update_data: AccountStatusUpdate,
                        current_user: User = Depends(require_roles("ADMIN", "FINANCE_MANAGER")),
                        db: Session = Depends(get_db)):
    account = AccountService.update_status(db, account_id, update_data)
    return {"success": True, "message": "Status updated", "data": account}
