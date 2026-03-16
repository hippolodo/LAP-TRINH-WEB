from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core import models
from . import schemas
from app.utils.auth_utils import get_password_hash

router = APIRouter()

@router.post("", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Kiểm tra Email trùng lặp
    db_user_email = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Kiểm tra CCCD trùng lặp
    db_user_cccd = db.query(models.User).filter(models.User.cccd == user.cccd).first()
    if db_user_cccd:
        raise HTTPException(status_code=400, detail="CCCD already registered")
    
    hashed_password = get_password_hash(user.password)
    # Xử lý work_location_id nếu là 0 hoặc không hợp lệ cho customer
    work_id = user.work_location_id if user.work_location_id and user.work_location_id > 0 else None

    new_user = models.User(
        full_name=user.full_name,
        email=user.email,
        password=hashed_password,
        phone=user.phone,
        cccd=user.cccd,
        dob=user.dob,
        gender=user.gender,
        address=user.address,
        role=user.role,
        work_location_id=work_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
