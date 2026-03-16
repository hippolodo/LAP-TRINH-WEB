from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core import models
from . import schemas
from app.core.database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Vaccine])
def get_vaccines(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    vaccines = db.query(models.Vaccine).offset(skip).limit(limit).all()
    return vaccines

@router.get("/{vaccine_id}", response_model=schemas.Vaccine)
def get_vaccine(vaccine_id: int, db: Session = Depends(get_db)):
    vaccine = db.query(models.Vaccine).filter(models.Vaccine.id == vaccine_id).first()
    if not vaccine:
        raise HTTPException(status_code=404, detail="Vaccine not found")
    return vaccine

@router.post("/", response_model=schemas.Vaccine, status_code=status.HTTP_201_CREATED)
def create_vaccine(vaccine: schemas.VaccineCreate, db: Session = Depends(get_db)):
    db_vaccine = models.Vaccine(**vaccine.dict())
    db.add(db_vaccine)
    db.commit()
    db.refresh(db_vaccine)
    return db_vaccine
