from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core import models
from . import schemas
from app.utils.auth_utils import verify_password

router = APIRouter()

@router.post("")
def login(user_credentials: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=403, detail="Invalid Credentials")
    
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=403, detail="Invalid Credentials")
    
    # Return user info (Simplified, normally you'd return a JWT)
    return {
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role
        },
        "access_token": "fake-jwt-token", # Placeholder
        "token_type": "bearer"
    }
