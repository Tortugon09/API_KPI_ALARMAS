from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.schemas import KPIWithDetails, KPICreate, KPIResponse, ObjetivoBase, KPIUpdate
from typing import List, Optional
from services.kpi_service import get_all_kpis_with_details, get_kpis_by_region_with_details, get_kpis_by_market_with_details, get_alarms_by_kpi_last_days, get_alarms_by_kpi_and_date_last_days_REGION
from datetime import datetime
from models.models import KPI, Objetivo

router = APIRouter()

@router.get("/region/{region_id}/kpis", response_model=List[KPIWithDetails])
def get_kpis_by_region(region_id: int, db: Session = Depends(get_db)):
    return get_kpis_by_region_with_details(db, region_id)

@router.get("/mercado/{mercado_id}/kpis", response_model=List[KPIWithDetails])
def get_kpis_by_market(mercado_id: int, db: Session = Depends(get_db)):
    return get_kpis_by_market_with_details(db, mercado_id)

@router.get("/kpi/alarms/mercado/{kpi_id}")
def get_region_alarms_by_date(
    kpi_id: int, 
    db: Session = Depends(get_db)
):
    
    return get_alarms_by_kpi_last_days(db, kpi_id)

@router.get("/kpi/alarms/region/{kpi_id}")
def get_region_alarms_by_date(
    kpi_id: int, 
    db: Session = Depends(get_db)
):
    
    return get_alarms_by_kpi_and_date_last_days_REGION(db, kpi_id)

@router.get("/kpis/", response_model=List[KPIResponse])
def read_kpis(db: Session = Depends(get_db)):
    kpis = db.query(KPI).all()
    response = []
    for kpi in kpis:
        objetivo = db.query(Objetivo).filter(Objetivo.id == kpi.objetivo_id).first()
        if not objetivo:
            raise HTTPException(status_code=404, detail="Objetivo not found")

        response.append(
            KPIResponse(
                id=kpi.id,
                nombre_kpi=kpi.nombre_kpi,
                objetivo=ObjetivoBase(id=objetivo.id, objetivo=objetivo.objetivo)
            )
        )
    return response

@router.get("/kpis/{kpi_id}", response_model=KPIResponse)
def read_kpi(kpi_id: int, db: Session = Depends(get_db)):
    kpi = db.query(KPI).filter(KPI.id == kpi_id).first()
    if not kpi:
        raise HTTPException(status_code=404, detail="KPI not found")

    objetivo = db.query(Objetivo).filter(Objetivo.id == kpi.objetivo_id).first()
    if not objetivo:
        raise HTTPException(status_code=404, detail="Objetivo not found")

    return KPIResponse(id=kpi.id, nombre_kpi=kpi.nombre_kpi, objetivo=objetivo)

@router.put("/kpis/{kpi_id}", response_model=KPIResponse)
def update_kpi(kpi_id: int, kpi_update: KPIUpdate, db: Session = Depends(get_db)):
    # Buscar el KPI existente
    db_kpi = db.query(KPI).filter(KPI.id == kpi_id).first()
    if not db_kpi:
        raise HTTPException(status_code=404, detail="KPI not found")
    
    # Actualizar los campos del KPI
    db_kpi.nombre_kpi = kpi_update.nombre_kpi
    if kpi_update.objetivo:
        # Actualizar el objetivo existente
        objetivo = db.query(Objetivo).filter(Objetivo.id == db_kpi.objetivo_id).first()
        if objetivo:
            objetivo.objetivo = kpi_update.objetivo
            db.commit()
            db.refresh(objetivo)
        else:
            # Crear un nuevo objetivo si no existe
            new_objetivo = Objetivo(objetivo=kpi_update.objetivo)
            db.add(new_objetivo)
            db.commit()
            db.refresh(new_objetivo)
            db_kpi.objetivo_id = new_objetivo.id
            db.commit()
            db.refresh(db_kpi)
    
    # Obtener el objetivo actualizado
    objetivo = db.query(Objetivo).filter(Objetivo.id == db_kpi.objetivo_id).first()
    
    # Retornar la respuesta
    return KPIResponse(
        id=db_kpi.id,
        nombre_kpi=db_kpi.nombre_kpi,
        objetivo=ObjetivoBase(id=objetivo.id, objetivo=objetivo.objetivo)
    )