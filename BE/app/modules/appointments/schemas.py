from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from ..vaccines.schemas import Vaccine
from ..locations.schemas import Location
from ..schedules.schemas import SessionType
from ..auth.schemas import User

class AppointmentStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    completed = "completed"
    cancelled = "cancelled"

class PatientGender(str, Enum):
    Nam = "Nam"
    Nu = "Nữ"
    Khac = "Khác"

class AppointmentBase(BaseModel):
    dependent_id: Optional[int] = None # Mới: Hồ sơ người tiêm
    patient_name: str
    patient_age: int
    patient_gender: PatientGender
    vaccine_id: int
    location_id: int
    schedule_id: Optional[int] = None
    appointment_date: date
    session: SessionType
    total_price: Decimal

class AppointmentCreate(AppointmentBase):
    user_id: Optional[int] = None

class AppointmentUpdate(BaseModel):
    status: Optional[AppointmentStatus] = None
    patient_name: Optional[str] = None
    patient_age: Optional[int] = None
    patient_gender: Optional[PatientGender] = None
    reactions: Optional[str] = None # Thêm trường phản ứng sau tiêm
    provider_name: Optional[str] = None # Tên người xác nhận tiêm

class Appointment(AppointmentBase):
    id: int
    user_id: int
    status: AppointmentStatus
    created_at: datetime
    vaccine: Optional[Vaccine] = None
    location: Optional[Location] = None
    user: Optional[User] = None # Thông tin người đặt lịch (Chủ tài khoản)

    class Config:
        from_attributes = True
