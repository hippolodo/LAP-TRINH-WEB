from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal
from enum import Enum

# Enums
class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"

class Role(str, Enum):
    customer = "customer"
    staff = "staff"
    admin = "admin"

class LocationStatus(str, Enum):
    active = "active"
    inactive = "inactive"

class VaccineStatus(str, Enum):
    available = "available"
    out_of_stock = "out_of_stock"
    discontinued = "discontinued"

class SessionType(str, Enum):
    morning = "morning"
    afternoon = "afternoon"

class ScheduleStatus(str, Enum):
    active = "active"
    full = "full"
    closed = "closed"

class AppointmentStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    completed = "completed"
    cancelled = "cancelled"

class PatientGender(str, Enum):
    Nam = "Nam"
    Nu = "Nữ"
    Khac = "Khác"

# Base Schemas
class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    cccd: str
    dob: date
    gender: Gender
    address: str
    role: Optional[Role] = Role.customer
    work_location_id: Optional[int] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Location Schemas
class LocationBase(BaseModel):
    name: str
    address: str
    phone: Optional[str] = None
    status: LocationStatus = LocationStatus.active

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    id: int

    class Config:
        from_attributes = True

# Vaccine Schemas
class VaccineBase(BaseModel):
    name: str
    manufacturer: Optional[str] = None
    price: Decimal
    description: Optional[str] = None
    dose_count: int = 1
    status: VaccineStatus = VaccineStatus.available

class VaccineCreate(VaccineBase):
    pass

class Vaccine(VaccineBase):
    id: int

    class Config:
        from_attributes = True

# Inventory Schemas
class InventoryBase(BaseModel):
    vaccine_id: int
    location_id: int
    batch_number: str
    stock_quantity: int = 0
    expiry_date: date

class InventoryCreate(InventoryBase):
    pass

class Inventory(InventoryBase):
    id: int
    vaccine: Optional[Vaccine] = None
    location: Optional[Location] = None

    class Config:
        from_attributes = True

# Schedule Schemas
class ScheduleBase(BaseModel):
    location_id: int
    work_date: date
    session: SessionType
    max_slots: int = 50
    occupied_slots: int = 0
    status: ScheduleStatus = ScheduleStatus.active

class ScheduleCreate(ScheduleBase):
    pass

class Schedule(ScheduleBase):
    id: int

    class Config:
        from_attributes = True

# Appointment Schemas
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

# Vaccination Record Schemas
class VaccinationRecordBase(BaseModel):
    user_id: int
    appointment_id: Optional[int] = None
    vaccine_id: int
    location_id: int
    batch_number: Optional[str] = None
    dose_number: Optional[str] = None
    provider_name: Optional[str] = None
    reactions: Optional[str] = None
    notes: Optional[str] = None

class VaccinationRecordCreate(VaccinationRecordBase):
    pass

class VaccinationRecord(VaccinationRecordBase):
    id: int
    date_given: datetime
    vaccine: Optional[Vaccine] = None

    class Config:
        from_attributes = True
