from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime
from enum import Enum

class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"

class Role(str, Enum):
    customer = "customer"
    staff = "staff"
    admin = "admin"

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

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
