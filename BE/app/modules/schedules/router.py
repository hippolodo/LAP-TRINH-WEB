from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.core import models
from . import schemas
from app.core.database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Schedule])
def get_schedules(
    location_id: Optional[int] = None,
    work_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Lấy danh sách ca tiêm. 
    Nếu truyền location_id và work_date, hệ thống sẽ tự động tạo 2 ca (Sáng/Chiều) 
    với 50 slot mặc định nếu chưa tồn tại.
    """
    if location_id and work_date:
        # Kiểm tra xem đã có đủ 2 ca chưa
        sessions = ['morning', 'afternoon']
        for sess in sessions:
            exists = db.query(models.Schedule).filter(
                models.Schedule.location_id == location_id,
                models.Schedule.work_date == work_date,
                models.Schedule.session == sess
            ).first()
            
            if not exists:
                new_sch = models.Schedule(
                    location_id=location_id,
                    work_date=work_date,
                    session=sess,
                    max_slots=50,
                    occupied_slots=0,
                    status='active'
                )
                db.add(new_sch)
        db.commit()

    query = db.query(models.Schedule)
    if location_id:
        query = query.filter(models.Schedule.location_id == location_id)
    if work_date:
        query = query.filter(models.Schedule.work_date == work_date)
        
    schedules = query.order_by(models.Schedule.session.desc()).all() # Sáng trước, Chiều sau
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

@router.put("/{schedule_id}", response_model=schemas.Schedule)
def update_schedule(schedule_id: int, schedule_update: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    db_schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    for key, value in schedule_update.dict().items():
        setattr(db_schedule, key, value)
    
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

@router.delete("/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    db_schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    # Có thể chọn xóa cứng hoặc đổi trạng thái sang 'closed'
    db_schedule.status = 'closed'
    db.commit()
    return None
