from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core import models
from . import schemas
from app.core.database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Appointment])
def get_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    appointments = db.query(models.Appointment).offset(skip).limit(limit).all()
    return appointments

@router.get("/{appointment_id}", response_model=schemas.Appointment)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@router.post("/", response_model=schemas.Appointment, status_code=status.HTTP_201_CREATED)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    if not appointment.user_id:
        raise HTTPException(status_code=400, detail="user_id is required")
        
    db_appointment = models.Appointment(**appointment.dict())
    db.add(db_appointment)
    
    # Update occupied_slots in Schedule
    schedule = db.query(models.Schedule).filter(models.Schedule.id == appointment.schedule_id).first()
    if schedule:
        schedule.occupied_slots += 1
        if schedule.occupied_slots >= schedule.max_slots:
            schedule.status = 'full'
            
    db.commit()
    db.refresh(db_appointment)
    return db_appointment
