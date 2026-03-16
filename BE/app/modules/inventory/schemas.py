from pydantic import BaseModel
from typing import Optional
from datetime import date
from ..vaccines.schemas import Vaccine
from ..locations.schemas import Location

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
