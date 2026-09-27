from sqlalchemy.orm import Session
from datetime import datetime
from app.models.transaction import Transaction
from app.models.reconciliation import ReconciliationRun, ReconciliationStatus
from app.models.reconciliation_record import ReconciliationRecord

class ReconciliationService:
    @staticmethod
    def run_reconciliation(db: Session, external_records: list):
        run = ReconciliationRun(status=ReconciliationStatus.IN_PROGRESS, total_external=len(external_records))
        db.add(run)
        db.flush()

        internal_txns = db.query(Transaction).all()
        internal_map = {t.reference_number: t for t in internal_txns}
        external_map = {r["reference_number"]: r for r in external_records}

        matched = 0
        mismatched = 0

        # Check internal vs external
        for ref, txn in internal_map.items():
            if ref in external_map:
                ext = external_map[ref]
                if abs(txn.amount - ext["amount"]) > 0.01:
                    db.add(ReconciliationRecord(run_id=run.id, reference_number=ref,
                        internal_amount=txn.amount, external_amount=ext["amount"],
                        mismatch_type="AMOUNT_MISMATCH"))
                    mismatched += 1
                elif txn.status != ext["status"]:
                    db.add(ReconciliationRecord(run_id=run.id, reference_number=ref,
                        internal_status=txn.status, external_status=ext["status"],
                        mismatch_type="STATUS_MISMATCH"))
                    mismatched += 1
                else:
                    matched += 1
            else:
                db.add(ReconciliationRecord(run_id=run.id, reference_number=ref,
                    internal_amount=txn.amount, mismatch_type="MISSING_EXTERNAL"))
                mismatched += 1

        # Check external missing in internal
        for ref, ext in external_map.items():
            if ref not in internal_map:
                db.add(ReconciliationRecord(run_id=run.id, reference_number=ref,
                    external_amount=ext["amount"], mismatch_type="MISSING_INTERNAL"))
                mismatched += 1

        run.total_internal = len(internal_txns)
        run.matched = matched
        run.mismatched = mismatched
        run.status = ReconciliationStatus.COMPLETED
        run.completed_at = datetime.now()
        db.commit()
        db.refresh(run)
        return run

    @staticmethod
    def get_all_runs(db: Session):
        return db.query(ReconciliationRun).all()

    @staticmethod
    def get_mismatches(db: Session):
        return db.query(ReconciliationRecord).all()

    @staticmethod
    def get_run_by_id(db: Session, run_id: int):
        return db.query(ReconciliationRun).filter(ReconciliationRun.id == run_id).first()
