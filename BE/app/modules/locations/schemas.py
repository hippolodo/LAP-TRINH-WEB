from pydantic import BaseModel
from typing import Optional
from enum import Enum

class LocationStatus(str, Enum):
    active = "active"
    inactive = "inactive"

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
