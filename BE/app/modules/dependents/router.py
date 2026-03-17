from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core import models
from app.core.database import get_db
from . import schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.Dependent])
def get_dependents(user_id: int, db: Session = Depends(get_db)):
    """Lấy danh sách người thân của một user"""
    dependents = db.query(models.Dependent).filter(models.Dependent.user_id == user_id).all()
    return dependents

@router.post("/", response_model=schemas.Dependent, status_code=status.HTTP_201_CREATED)
def create_dependent(dependent: schemas.DependentCreate, db: Session = Depends(get_db)):
    """Thêm một người thân mới"""
    new_dependent = models.Dependent(**dependent.dict())
    db.add(new_dependent)
    db.commit()
    db.refresh(new_dependent)
    return new_dependent

@router.get("/{dependent_id}", response_model=schemas.Dependent)
def get_dependent(dependent_id: int, db: Session = Depends(get_db)):
    """Lấy chi tiết một người thân"""
    dependent = db.query(models.Dependent).filter(models.Dependent.id == dependent_id).first()
    if not dependent:
        raise HTTPException(status_code=404, detail="Dependent not found")
    return dependent

@router.put("/{dependent_id}", response_model=schemas.Dependent)
def update_dependent(dependent_id: int, dependent_update: schemas.DependentUpdate, db: Session = Depends(get_db)):
    """Cập nhật thông tin người thân"""
    db_dependent = db.query(models.Dependent).filter(models.Dependent.id == dependent_id).first()
    if not db_dependent:
        raise HTTPException(status_code=404, detail="Dependent not found")
    
    update_data = dependent_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_dependent, key, value)
    
    db.commit()
    db.refresh(db_dependent)
    return db_dependent

@router.delete("/{dependent_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dependent(dependent_id: int, db: Session = Depends(get_db)):
    """Xóa người thân"""
    db_dependent = db.query(models.Dependent).filter(models.Dependent.id == dependent_id).first()
    if not db_dependent:
        raise HTTPException(status_code=404, detail="Dependent not found")
    
    db.delete(db_dependent)
    db.commit()
    return None
