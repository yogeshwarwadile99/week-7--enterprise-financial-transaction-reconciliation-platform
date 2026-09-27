from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.audit_log import AuditLog
from app.middleware.auth import require_roles
from app.models.user import User

router = APIRouter(prefix="/api/v1/audit", tags=["Audit Logs"])

@router.get("/logs")
async def get_logs(current_user: User = Depends(require_roles("ADMIN")), db: Session = Depends(get_db)):
    logs = db.query(AuditLog).all()
    return {"success": True, "data": logs}
