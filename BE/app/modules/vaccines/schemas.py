from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from enum import Enum

class VaccineStatus(str, Enum):
    available = "available"
    out_of_stock = "out_of_stock"
    discontinued = "discontinued"

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
