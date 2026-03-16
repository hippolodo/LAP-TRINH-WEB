from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from ..vaccines.schemas import Vaccine

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
