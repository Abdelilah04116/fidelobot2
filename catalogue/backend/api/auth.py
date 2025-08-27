from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from SMA.core.auth import create_user, authenticate_user, create_access_token, get_current_active_user
from datetime import timedelta
from SMA.core.config import settings

router = APIRouter()

# --- Schemas ---
class RegisterRequest(BaseModel):
    email: str
    password: str
    username: str

class LoginRequest(BaseModel):
    email: str
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

class PreferencesRequest(BaseModel):
    preferences: dict

class DeactivateRequest(BaseModel):
    reason: Optional[str] = None

# --- Endpoints ---
@router.post("/register")
def register_user(req: RegisterRequest):
    user = create_user(email=req.email, username=req.username, password=req.password)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer", "user_id": user.id}

@router.post("/login")
def login_user(req: LoginRequest):
    user = authenticate_user(email=req.email, password=req.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    # Placeholder: un vrai refresh_token serait signé et stocké
    refresh_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(days=7))
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer", "user_id": user.id}

@router.post("/refresh")
def refresh_token(req: RefreshRequest):
    # Simplification: accepter tout refresh_token non vide et ré émettre un access token court
    if not req.refresh_token:
        raise HTTPException(status_code=400, detail="refresh_token manquant")
    # En réel: décoder/valider le refresh token et émettre un access token
    # Ici on renvoie un token court générique
    access_token = create_access_token(data={"sub": "refresh"}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def get_current_user_info(current_user=Depends(get_current_active_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "is_active": current_user.is_active,
        "preferences": current_user.preferences,
    }

@router.put("/preferences")
def update_preferences(req: PreferencesRequest, current_user=Depends(get_current_active_user)):
    from SMA.models.database import SessionLocal
    db = SessionLocal()
    try:
        current_user.preferences = req.preferences
        db.add(current_user)
        db.commit()
        return {"success": True, "preferences": current_user.preferences}
    finally:
        db.close()

@router.post("/deactivate")
def deactivate_user(req: DeactivateRequest, current_user=Depends(get_current_active_user)):
    from SMA.models.database import SessionLocal
    db = SessionLocal()
    try:
        current_user.is_active = False
        db.add(current_user)
        db.commit()
        return {"success": True}
    finally:
        db.close()
