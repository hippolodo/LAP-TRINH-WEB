from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from ..vaccines.schemas import Vaccine
from ..locations.schemas import Location
from ..schedules.schemas import SessionType

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
    patient_name: str
    patient_age: int
    patient_gender: PatientGender
    vaccine_id: int
    location_id: int
    schedule_id: int
    appointment_date: date
    session: SessionType
    total_price: Decimal

class AppointmentCreate(AppointmentBase):
    user_id: Optional[int] = None

class Appointment(AppointmentBase):
    id: int
    user_id: int
    status: AppointmentStatus
    created_at: datetime
    vaccine: Optional[Vaccine] = None
    location: Optional[Location] = None

    class Config:
        from_attributes = True
