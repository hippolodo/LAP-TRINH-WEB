from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core import models
from . import schemas
from app.core.database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Appointment])
def get_appointments(
    user_id: Optional[int] = None,
    location_id: Optional[int] = None,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    query = db.query(models.Appointment)
    
    # Bảo mật: Nếu không có tiêu chí lọc, trả về rỗng
    if not user_id and not location_id:
        return []

    if user_id:
        query = query.filter(models.Appointment.user_id == user_id)
    if location_id:
        query = query.filter(models.Appointment.location_id == location_id)
        
    appointments = query.order_by(models.Appointment.appointment_date.desc()).offset(skip).limit(limit).all()
    return appointments

@router.put("/{appointment_id}", response_model=schemas.Appointment)
def update_appointment(appointment_id: int, apt_update: schemas.AppointmentUpdate, db: Session = Depends(get_db)):
    db_apt = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not db_apt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    old_status = db_apt.status
    update_data = apt_update.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_apt, key, value)
    
    # Logic: Nếu trạng thái chuyển sang 'completed', tự động tạo hoặc cập nhật VaccinationRecord
    if apt_update.status == 'completed' and old_status != 'completed':
        # 1. Trừ kho vaccine tại cơ sở tiêm
        inventory = db.query(models.Inventory).filter(
            models.Inventory.vaccine_id == db_apt.vaccine_id,
            models.Inventory.location_id == db_apt.location_id
        ).first()

        if inventory:
            if inventory.stock_quantity > 0:
                inventory.stock_quantity -= 1
            else:
                # Có thể log cảnh báo hoặc raise lỗi tùy yêu cầu nghiệp vụ
                # Ở đây chúng ta cho phép tiêm dù kho báo hết (có thể do sai lệch số liệu thực tế)
                pass

        # 2. Tạo hoặc cập nhật VaccinationRecord
        existing_record = db.query(models.VaccinationRecord).filter(models.VaccinationRecord.appointment_id == appointment_id).first()
        
        if not existing_record:
            new_record = models.VaccinationRecord(
                user_id=db_apt.user_id,
                dependent_id=db_apt.dependent_id,
                appointment_id=appointment_id,
                vaccine_id=db_apt.vaccine_id,
                location_id=db_apt.location_id,
                batch_number=inventory.batch_number if inventory else "N/A",
                dose_number="1",
                provider_name=apt_update.provider_name or "System Staff",
                reactions=apt_update.reactions, 
                notes=f"Auto-generated from appointment VC-{appointment_id}"
            )
            db.add(new_record)
        else:
            if apt_update.reactions is not None:
                existing_record.reactions = apt_update.reactions

    db.commit()
    db.refresh(db_apt)
    return db_apt

@router.get("/{appointment_id}", response_model=schemas.Appointment)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@router.delete("/{appointment_id}", status_code=status.HTTP_200_OK)
def cancel_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """
    Khách hàng tự hủy lịch hẹn khi vẫn ở trạng thái 'pending'
    """
    db_apt = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    
    if not db_apt:
        raise HTTPException(status_code=404, detail="Không tìm thấy lịch hẹn")
    
    if db_apt.status != 'pending':
        raise HTTPException(
            status_code=400, 
            detail=f"Không thể hủy lịch hẹn đã ở trạng thái: {db_apt.status}. Vui lòng liên hệ trung tâm để được hỗ trợ."
        )
    
    # Cập nhật trạng thái lịch hẹn
    db_apt.status = 'cancelled'
    
    # Hoàn trả slot cho lịch làm việc (Schedule)
    schedule = db.query(models.Schedule).filter(models.Schedule.id == db_apt.schedule_id).first()
    if schedule and schedule.occupied_slots > 0:
        schedule.occupied_slots -= 1
        # Nếu trước đó là 'full', bây giờ có thể nhận khách lại
        if schedule.status == 'full':
            schedule.status = 'active'
            
    db.commit()
    return {"message": "Hủy lịch hẹn thành công", "appointment_id": appointment_id}

@router.post("/", response_model=schemas.Appointment, status_code=status.HTTP_201_CREATED)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    if not appointment.user_id:
        raise HTTPException(status_code=400, detail="user_id is required")
    
    # Kiểm tra trạng thái cơ sở
    db_location = db.query(models.Location).filter(models.Location.id == appointment.location_id).first()
    if not db_location or db_location.status == 'inactive':
        raise HTTPException(status_code=400, detail="Cơ sở này hiện đang tạm nghỉ, vui lòng chọn cơ sở khác")
    
    apt_data = appointment.dict()
    
    # Nếu thiếu schedule_id, tự động tìm dựa trên cơ sở, ngày và ca
    if not appointment.schedule_id:
        schedule = db.query(models.Schedule).filter(
            models.Schedule.location_id == appointment.location_id,
            models.Schedule.work_date == appointment.appointment_date,
            models.Schedule.session == appointment.session
        ).first()
        
        if not schedule:
            # Nếu chưa có ca tiêm này trong DB, tự động tạo mới (dành cho tạo phiếu tay)
            schedule = models.Schedule(
                location_id=appointment.location_id,
                work_date=appointment.appointment_date,
                session=appointment.session,
                max_slots=50,
                occupied_slots=0,
                status='active'
            )
            db.add(schedule)
            db.commit()
            db.refresh(schedule)
        
        apt_data["schedule_id"] = schedule.id

    db_appointment = models.Appointment(**apt_data)
    db.add(db_appointment)
    
    # Cập nhật số lượng slot đã đặt
    schedule_to_update = db.query(models.Schedule).filter(models.Schedule.id == apt_data["schedule_id"]).first()
    if schedule_to_update:
        schedule_to_update.occupied_slots += 1
        if schedule_to_update.occupied_slots >= schedule_to_update.max_slots:
            schedule_to_update.status = 'full'
            
    db.commit()
    db.refresh(db_appointment)
    return db_appointment
