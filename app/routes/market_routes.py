from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.kpi_service import get_alarms_by_market_and_date, get_markets_by_date_range
from datetime import datetime
from schemas.schemas import Mercado , MercadoCreate, MercadoUpdate
from models.models import Mercado as MercadoModel
from typing import List

router = APIRouter()

@router.get("/market/alarms/{mercado_id}")
def get_market_alarms_by_date(
    mercado_id: int, 
    start_date: str, 
    end_date: str, 
    db: Session = Depends(get_db)
):
    try:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    
    return get_alarms_by_market_and_date(db, mercado_id, start_date_obj, end_date_obj)

@router.get("/market/alarms")
def get_markets_within_date_range(
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
    
    return get_markets_by_date_range(db, start_date, end_date)

@router.get("/markets", response_model=List[Mercado])
def get_markets(db: Session = Depends(get_db)):
    mercados = db.query(MercadoModel).all()
    return mercados


# Endpoint para modificar el estado de activo de un mercado
@router.put("/markets/{market_id}", response_model=Mercado)
def update_market(market_id: int, market_data: MercadoUpdate, db: Session = Depends(get_db)):
    market = db.query(MercadoModel).filter(MercadoModel.id == market_id).first()
    if not market:
        raise HTTPException(status_code=404, detail="Market not found")
    market.activo = market_data.activo
    db.commit()
    db.refresh(market)
    return market

@router.post("/markets", response_model=Mercado)
def create_market(market: MercadoCreate, db: Session = Depends(get_db)):
    new_market = MercadoModel(**market.dict())
    db.add(new_market)
    db.commit()
    db.refresh(new_market)
    return new_market

# Endpoint para eliminar un mercado
@router.delete("/markets/{market_id}", response_model=dict)
def delete_market(market_id: int, db: Session = Depends(get_db)):
    market = db.query(MercadoModel).filter(MercadoModel.id == market_id).first()
    if not market:
        raise HTTPException(status_code=404, detail="Market not found")
    db.delete(market)
    db.commit()
    return {"message": "Market deleted successfully"}
