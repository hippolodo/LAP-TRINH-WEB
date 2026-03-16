from pydantic import BaseModel
from datetime import date
from enum import Enum

class SessionType(str, Enum):
    morning = "morning"
    afternoon = "afternoon"

class ScheduleStatus(str, Enum):
    active = "active"
    full = "full"
    closed = "closed"

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
