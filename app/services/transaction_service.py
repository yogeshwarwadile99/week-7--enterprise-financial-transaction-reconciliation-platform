from sqlalchemy.orm import Session
from datetime import datetime
import random
from app.models.transaction import Transaction, TransactionStatus, TransactionType
from app.models.transaction_entry import TransactionEntry
from app.models.account import Account
from app.models.idempotency import IdempotencyKey
from app.models.audit_log import AuditLog
from app.schemas.transaction import TransactionCreate
from app.middleware.error_handler import AppException

class TransactionService:
    @staticmethod
    def generate_reference():
        return f"TXN-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"

    @staticmethod
    def create_transaction(db: Session, txn_data: TransactionCreate, user_id: int, idempotency_key: str = None):
        # Idempotency check
        if idempotency_key:
            existing = db.query(IdempotencyKey).filter(IdempotencyKey.key == idempotency_key).first()
            if existing:
                raise AppException("DUPLICATE_REQUEST", "Transaction already processed", 400)

        # Validate sender account
        sender = None
        if txn_data.sender_account_id:
            sender = db.query(Account).filter(Account.id == txn_data.sender_account_id).with_for_update().first()
            if not sender:
                raise AppException("ACCOUNT_NOT_FOUND", "Sender account not found", 404)
            if sender.available_balance < txn_data.amount:
                raise AppException("INSUFFICIENT_FUNDS", "Transaction cannot be completed due to insufficient balance", 400)

        # Validate receiver account
        receiver = None
        if txn_data.receiver_account_id:
            receiver = db.query(Account).filter(Account.id == txn_data.receiver_account_id).with_for_update().first()
            if not receiver:
                raise AppException("ACCOUNT_NOT_FOUND", "Receiver account not found", 404)

        # Create transaction
        transaction = Transaction(
            reference_number=TransactionService.generate_reference(),
            sender_account_id=txn_data.sender_account_id,
            receiver_account_id=txn_data.receiver_account_id,
            amount=txn_data.amount,
            currency=txn_data.currency,
            transaction_type=txn_data.transaction_type,
            channel=txn_data.channel,
            status=TransactionStatus.PROCESSING,
            description=txn_data.description
        )
        db.add(transaction)
        db.flush()

        # Double-entry ledger
        if sender:
            sender.available_balance -= txn_data.amount
            sender.ledger_balance -= txn_data.amount
            entry = TransactionEntry(
                transaction_id=transaction.id,
                account_id=sender.id,
                entry_type="DEBIT",
                amount=txn_data.amount,
                balance_after=sender.available_balance
            )
            db.add(entry)

        if receiver:
            receiver.available_balance += txn_data.amount
            receiver.ledger_balance += txn_data.amount
            entry = TransactionEntry(
                transaction_id=transaction.id,
                account_id=receiver.id,
                entry_type="CREDIT",
                amount=txn_data.amount,
                balance_after=receiver.available_balance
            )
            db.add(entry)

        transaction.status = TransactionStatus.SUCCESS
        transaction.completed_at = datetime.now()

        if idempotency_key:
            db.add(IdempotencyKey(key=idempotency_key, response=str(transaction.id)))

        # Audit log
        db.add(AuditLog(
            user_id=user_id,
            action="TRANSACTION_CREATED",
            resource="TRANSACTION",
            resource_id=transaction.id
        ))

        db.commit()
        db.refresh(transaction)
        return transaction

    @staticmethod
    def get_all_transactions(db: Session):
        return db.query(Transaction).all()

    @staticmethod
    def get_transaction_by_id(db: Session, txn_id: int):
        txn = db.query(Transaction).filter(Transaction.id == txn_id).first()
        if not txn:
            raise AppException("TRANSACTION_NOT_FOUND", "Transaction not found", 404)
        return txn

    @staticmethod
    def cancel_transaction(db: Session, txn_id: int, user_id: int):
        txn = TransactionService.get_transaction_by_id(db, txn_id)
        if txn.status != TransactionStatus.SUCCESS:
            raise AppException("INVALID_STATUS", "Only successful transactions can be reversed", 400)
        txn.status = TransactionStatus.REVERSAL_REQUESTED
        db.add(AuditLog(user_id=user_id, action="TRANSACTION_CANCEL_REQUESTED", resource="TRANSACTION", resource_id=txn.id))
        db.commit()
        db.refresh(txn)
        return txn
