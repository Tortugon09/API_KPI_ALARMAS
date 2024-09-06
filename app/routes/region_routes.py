from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.kpi_service import get_alarms_by_region_and_date, get_regions_by_date_range
from models.models import Region
from schemas.schemas import RegionCreate, RegionUpdate, Region as RegionSchema
from typing import List
from datetime import datetime

router = APIRouter()

@router.get("/region/alarms/{region_id}")
def get_region_alarms_by_date(
    region_id: int, 
    start_date: str, 
    end_date: str, 
    db: Session = Depends(get_db)
):
    try:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    
    return get_alarms_by_region_and_date(db, region_id, start_date_obj, end_date_obj)



@router.get("/region/alarms")
def get_regions_within_date_range(
    start_date: str, 
    end_date: str, 
    db: Session = Depends(get_db)
):
    try:
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    
    return get_regions_by_date_range(db, start_date, end_date)

@router.post("/regions/", response_model=RegionSchema)
def create_region(region: RegionCreate, db: Session = Depends(get_db)):
    db_region = Region(**region.dict())
    db.add(db_region)
    db.commit()
    db.refresh(db_region)
    return db_region

@router.get("/regions/{region_id}", response_model=RegionSchema)
def read_region(region_id: int, db: Session = Depends(get_db)):
    db_region = db.query(Region).filter(Region.id == region_id).first()
    if db_region is None:
        raise HTTPException(status_code=404, detail="Region not found")
    return db_region

@router.put("/regions/{region_id}", response_model=RegionSchema)
def update_region(region_id: int, region: RegionUpdate, db: Session = Depends(get_db)):
    db_region = db.query(Region).filter(Region.id == region_id).first()
    if db_region is None:
        raise HTTPException(status_code=404, detail="Region not found")
    for key, value in region.dict().items():
        setattr(db_region, key, value)
    db.commit()
    db.refresh(db_region)
    return db_region

@router.get("/regions/", response_model=List[RegionSchema])
def read_all_regions(db: Session = Depends(get_db)):
    regions = db.query(Region).all()
    return regions

@router.delete("/regions/{region_id}")
def delete_region(region_id: int, db: Session = Depends(get_db)):
    db_region = db.query(Region).filter(Region.id == region_id).first()
    if db_region is None:
        raise HTTPException(status_code=404, detail="Region not found")
    db.delete(db_region)
    db.commit()
    return {"ok": True}
