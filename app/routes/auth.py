from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserLogin
from app.services.auth_service import AuthService
from app.middleware.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

@router.post("/register")
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    user = AuthService.register(db, user_data)
    return {"success": True, "message": "User registered successfully",
            "data": {"id": user.id, "name": user.name, "email": user.email, "role": user.role}}

@router.post("/login")
async def login(login_data: UserLogin, db: Session = Depends(get_db)):
    result = AuthService.login(db, login_data.email, login_data.password)
    return {"success": True, "message": "Login successful", "data": result}

@router.post("/refresh")
async def refresh():
    return {"success": True, "message": "Token refreshed"}

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    return {"success": True, "message": "Logged out successfully"}

@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return {"success": True, "data": {
        "id": current_user.id, "name": current_user.name,
        "email": current_user.email, "role": current_user.role}}
