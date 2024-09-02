from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from database import Base

class Region(Base):
    __tablename__ = "Region"
    id = Column(Integer, primary_key=True, index=True)
    nombre_de_region = Column(String(255), nullable=False)
    activo = Column(Boolean)
    municipios = relationship("Municipio", back_populates="region")

class Municipio(Base):
    __tablename__ = "Municipio"
    id = Column(Integer, primary_key=True, index=True)
    nombre_municipio = Column(String(255), nullable=False)
    activo = Column(Boolean)
    region_id = Column(Integer, ForeignKey("Region.id"))
    region = relationship("Region", back_populates="municipios")
    mercados = relationship("Mercado", back_populates="municipio")

class Mercado(Base):
    __tablename__ = "Mercados"
    id = Column(Integer, primary_key=True, index=True)
    nombre_mercado = Column(String(255), nullable=False)
    activo = Column(Boolean)
    municipio_id = Column(Integer, ForeignKey("Municipio.id"))
    municipio = relationship("Municipio", back_populates="mercados")

class Objetivo(Base):
    __tablename__ = "Objetivos"
    id = Column(Integer, primary_key=True, index=True)
    objetivo = Column(Float)

class KPI(Base):
    __tablename__ = "KPIs"
    id = Column(Integer, primary_key=True, index=True)
    nombre_kpi = Column(String(255), nullable=False)
    objetivo_id = Column(Integer, ForeignKey("Objetivos.id"))
    objetivo = relationship("Objetivo")

class RegionKPI(Base):
    __tablename__ = "Region_KPI"
    id = Column(Integer, primary_key=True, index=True)
    region_id = Column(Integer, ForeignKey("Region.id"))
    kpi_id = Column(Integer, ForeignKey("KPIs.id"))
    fecha = Column(Date)
    resultado = Column(Date)
    region = relationship("Region")
    kpi = relationship("KPI")

class MercadoKPI(Base):
    __tablename__ = "Mercado_KPI"
    id = Column(Integer, primary_key=True, index=True)
    mercado_id = Column(Integer, ForeignKey("Mercados.id"))
    kpi_id = Column(Integer, ForeignKey("KPIs.id"))
    fecha = Column(Date)
    resultados = Column(Integer)
    mercado = relationship("Mercado")
    kpi = relationship("KPI")

class Alarma(Base):
    __tablename__ = "alarmas"
    alarma_id = Column(Integer, primary_key=True, index=True)
    region_kpi = Column(Integer, ForeignKey("Region_KPI.id"))
    fecha = Column(Date)
    region_kpi_relation = relationship("RegionKPI")

class AlarmaMercado(Base):
    __tablename__ = "alarmas_mercados"
    alarma_id = Column(Integer, primary_key=True, index=True)
    mercado_kpi_id = Column(Integer, ForeignKey("Mercado_KPI.id"))
    fecha = Column(Date)
    mercado_kpi_relation = relationship("MercadoKPI")

class ConteoDeAlarmas(Base):
    __tablename__ = "Conteo_de_alarmas"
    id = Column(Integer, primary_key=True, index=True)
    conteo_dias = Column(Integer)
