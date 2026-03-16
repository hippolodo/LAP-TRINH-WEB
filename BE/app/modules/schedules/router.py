from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core import models
from . import schemas
from app.core.database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Schedule])
def get_schedules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    schedules = db.query(models.Schedule).offset(skip).limit(limit).all()
    return schedules

@router.get("/{schedule_id}", response_model=schemas.Schedule)
def get_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule

@router.post("/", response_model=schemas.Schedule, status_code=status.HTTP_201_CREATED)
def create_schedule(schedule: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    db_schedule = models.Schedule(**schedule.dict())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule
