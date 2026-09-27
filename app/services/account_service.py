from sqlalchemy.orm import Session
from datetime import datetime
import random
from app.models.account import Account, AccountStatus
from app.schemas.account import AccountCreate, AccountStatusUpdate
from app.middleware.error_handler import AppException

class AccountService:
    @staticmethod
    def generate_account_number():
        return f"ACC{random.randint(10000, 99999)}"

    @staticmethod
    def create_account(db: Session, account_data: AccountCreate):
        account = Account(
            account_number=AccountService.generate_account_number(),
            customer_id=account_data.customer_id,
            currency=account_data.currency,
            available_balance=account_data.initial_balance,
            ledger_balance=account_data.initial_balance,
            status=AccountStatus.ACTIVE
        )
        db.add(account)
        db.commit()
        db.refresh(account)
        return account

    @staticmethod
    def get_all_accounts(db: Session):
        return db.query(Account).all()

    @staticmethod
    def get_account_by_id(db: Session, account_id: int):
        account = db.query(Account).filter(Account.id == account_id).first()
        if not account:
            raise AppException("ACCOUNT_NOT_FOUND", "Account not found", 404)
        return account

    @staticmethod
    def update_status(db: Session, account_id: int, update_data: AccountStatusUpdate):
        account = AccountService.get_account_by_id(db, account_id)
        account.status = update_data.status
        db.commit()
        db.refresh(account)
        return account
