from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from enum import Enum

class GenderEnum(str, Enum):
    nam = "Nam"
    nu = "Nữ"
    khac = "Khác"

class DependentBase(BaseModel):
    full_name: str
    dob: date
    gender: GenderEnum
    relation_type: str # 'Bản thân', 'Con', 'Vợ/Chồng', 'Bố/Mẹ'...
    cccd: Optional[str] = None

class DependentCreate(DependentBase):
    user_id: int

class DependentUpdate(BaseModel):
    full_name: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[GenderEnum] = None
    relation_type: Optional[str] = None
    cccd: Optional[str] = None

class Dependent(DependentBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
