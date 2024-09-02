from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.alarm_service import get_all_markets_and_regions_with_alarms, get_markets_and_regions_with_alarms_in_date_range
from datetime import datetime

router = APIRouter()

@router.get("/markets-and-regions-with-alarms")
def get_markets_and_regions_with_alarms(db: Session = Depends(get_db)):
    return get_all_markets_and_regions_with_alarms(db)

@router.get("/regions_and_markets_with_alarms_in_date_range/")
def read_markets_and_regions_with_alarms_in_date_range(
    start_date: str, 
    end_date: str, 
    db: Session = Depends(get_db)
):
    try:
        # Validar formato de fechas
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    
    return get_markets_and_regions_with_alarms_in_date_range(db, start_date, end_date)
