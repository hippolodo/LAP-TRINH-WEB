from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core import models
from . import schemas
from app.core.database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Inventory])
def get_inventory(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # The response_model schemas.Inventory includes vaccine and location
    # SQLAlchemy relationships will handle the loading
    inventory_items = db.query(models.Inventory).offset(skip).limit(limit).all()
    return inventory_items

@router.get("/{inventory_id}", response_model=schemas.Inventory)
def get_inventory_item(inventory_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Inventory).filter(models.Inventory.id == inventory_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return item

@router.post("/", response_model=schemas.Inventory, status_code=status.HTTP_201_CREATED)
def create_inventory_item(item: schemas.InventoryCreate, db: Session = Depends(get_db)):
    db_item = models.Inventory(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
