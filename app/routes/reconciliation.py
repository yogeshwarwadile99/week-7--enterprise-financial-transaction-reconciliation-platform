from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.reconciliation import ExternalRecord
from app.services.reconciliation_service import ReconciliationService
from app.middleware.auth import require_roles
from app.models.user import User

router = APIRouter(prefix="/api/v1/reconciliation", tags=["Reconciliation"])

@router.post("/run")
async def run_reconciliation(
    external_records: List[ExternalRecord],
    current_user: User = Depends(require_roles("ADMIN", "FINANCE_MANAGER", "OPERATIONS_ANALYST")),
    db: Session = Depends(get_db)
):
    records = [r.dict() for r in external_records]
    run = ReconciliationService.run_reconciliation(db, records)
    return {"success": True, "message": "Reconciliation completed", "data": run}

@router.get("/runs")
async def get_runs(current_user: User = Depends(require_roles("ADMIN", "FINANCE_MANAGER")), db: Session = Depends(get_db)):
    return {"success": True, "data": ReconciliationService.get_all_runs(db)}

@router.get("/mismatches")
async def get_mismatches(current_user: User = Depends(require_roles("ADMIN", "FINANCE_MANAGER", "OPERATIONS_ANALYST")), db: Session = Depends(get_db)):
    return {"success": True, "data": ReconciliationService.get_mismatches(db)}

@router.get("/{run_id}")
async def get_run(run_id: int, current_user: User = Depends(require_roles("ADMIN", "FINANCE_MANAGER")), db: Session = Depends(get_db)):
    return {"success": True, "data": ReconciliationService.get_run_by_id(db, run_id)}
