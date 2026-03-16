from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core import models
from . import schemas
from app.core.database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.VaccinationRecord])
def get_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    records = db.query(models.VaccinationRecord).offset(skip).limit(limit).all()
    return records

@router.get("/{record_id}", response_model=schemas.VaccinationRecord)
def get_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(models.VaccinationRecord).filter(models.VaccinationRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Vaccination record not found")
    return record

@router.post("/", response_model=schemas.VaccinationRecord, status_code=status.HTTP_201_CREATED)
def create_record(record: schemas.VaccinationRecordCreate, db: Session = Depends(get_db)):
    db_record = models.VaccinationRecord(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record
