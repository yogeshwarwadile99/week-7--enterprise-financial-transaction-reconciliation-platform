from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.risk import RiskReviewUpdate
from app.services.risk_service import RiskService
from app.middleware.auth import require_roles
from app.models.user import User

router = APIRouter(prefix="/api/v1/risk", tags=["Risk Alerts"])

@router.get("/alerts")
async def get_alerts(current_user: User = Depends(require_roles("ADMIN", "FINANCE_MANAGER", "OPERATIONS_ANALYST")), db: Session = Depends(get_db)):
    return {"success": True, "data": RiskService.get_all_alerts(db)}

@router.get("/alerts/{alert_id}")
async def get_alert(alert_id: int, current_user: User = Depends(require_roles("ADMIN", "FINANCE_MANAGER", "OPERATIONS_ANALYST")), db: Session = Depends(get_db)):
    return {"success": True, "data": RiskService.get_alert_by_id(db, alert_id)}

@router.patch("/alerts/{alert_id}/review")
async def review_alert(alert_id: int, update_data: RiskReviewUpdate,
                       current_user: User = Depends(require_roles("ADMIN", "FINANCE_MANAGER")),
                       db: Session = Depends(get_db)):
    alert = RiskService.review_alert(db, alert_id, update_data.status, current_user.id)
    return {"success": True, "message": "Alert reviewed", "data": alert}
