from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional

class AlarmBase(BaseModel):
    alarma_id: int
    fecha: date

    class Config:
        from_attributes = True  # Renombrado de orm_mode en Pydantic v2

class KPIWithDetails(BaseModel):
    nombre_kpi: str
    related_name: str  # Nombre de región o mercado
    fecha: date
    alarms: List[AlarmBase] = []

    class Config:
        from_attributes = True  # Renombrado de orm_mode en Pydantic v2
class MercadoBase(BaseModel):
    nombre_mercado: str
    activo: Optional[bool] = True
    municipio_id: int

class MercadoCreate(MercadoBase):
    pass

class MercadoUpdate(BaseModel):
    nombre_mercado: Optional[str] = None
    activo: Optional[bool] = None
    municipio_id: Optional[int] = None

class Mercado(MercadoBase):
    id: int

    class Config:
        from_attributes = True  # Reemplaza `orm_mode` por `from_attributes` en Pydantic v2

class RegionBase(BaseModel):
    nombre_de_region: str
    activo: bool

class RegionCreate(RegionBase):
    pass

class RegionUpdate(RegionBase):
    pass

class Region(RegionBase):
    id: int

    class Config:
        orm_mode = True

class ObjetivoBase(BaseModel):
    id: Optional[int] = None
    objetivo: float

    class Config:
        orm_mode = True
        
class KPICreate(BaseModel):
    nombre_kpi: str
    objetivo: float

class KPIResponse(BaseModel):
    id: int
    nombre_kpi: str
    objetivo: ObjetivoBase

    class Config:
        orm_mode = True

class KPIUpdate(BaseModel):
    nombre_kpi: Optional[str] = Field(None, example="Nuevo Nombre del KPI")
    objetivo: Optional[str] = Field(None, example="Nuevo Objetivo")