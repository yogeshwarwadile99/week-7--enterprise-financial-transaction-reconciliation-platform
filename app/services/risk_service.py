from sqlalchemy.orm import Session
from app.models.risk_alert import RiskAlert
from app.models.transaction import Transaction

class RiskService:
    @staticmethod
    def get_all_alerts(db: Session):
        return db.query(RiskAlert).all()

    @staticmethod
    def get_alert_by_id(db: Session, alert_id: int):
        return db.query(RiskAlert).filter(RiskAlert.id == alert_id).first()

    @staticmethod
    def review_alert(db: Session, alert_id: int, status: str, user_id: int):
        alert = RiskService.get_alert_by_id(db, alert_id)
        if not alert:
            return None
        alert.status = status
        alert.reviewed_by = user_id
        db.commit()
        db.refresh(alert)
        return alert
