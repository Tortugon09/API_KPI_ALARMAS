from sqlalchemy.orm import Session
from models.models import KPI, RegionKPI, MercadoKPI, Alarma, AlarmaMercado, Region, Mercado

def get_markets_and_regions_with_alarms_in_date_range(db: Session, start_date: str, end_date: str):
    from datetime import datetime

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    regions = db.query(Region).all()
    regions_with_alarms = []
    
    for region in regions:
        region_kpis = db.query(RegionKPI).filter(
            RegionKPI.region_id == region.id,
            RegionKPI.fecha.between(start_date, end_date)
        ).all()
        kpis_with_alarms = {}
        for rkpi in region_kpis:
            kpi = db.query(KPI).filter(KPI.id == rkpi.kpi_id).first()
            alarms = db.query(Alarma).filter(Alarma.region_kpi == rkpi.id).all()
            if kpi.nombre_kpi not in kpis_with_alarms:
                kpis_with_alarms[kpi.nombre_kpi] = {
                    "pivot_fecha": rkpi.fecha,
                    "resultado": rkpi.resultado,
                    "alarms": []
                }
            for alarm in alarms:
                kpis_with_alarms[kpi.nombre_kpi]["alarms"].append({
                    "alarm_id": alarm.alarma_id,
                    "fecha": alarm.fecha
                })
        
        regions_with_alarms.append({
            "nombre_de_region": region.nombre_de_region,
            "kpis": kpis_with_alarms
        })

    mercados = db.query(Mercado).all()
    mercados_with_alarms = []
    
    for mercado in mercados:
        mercado_kpis = db.query(MercadoKPI).filter(
            MercadoKPI.mercado_id == mercado.id,
            MercadoKPI.fecha.between(start_date, end_date)
        ).all()
        kpis_with_alarms = {}
        for mkpi in mercado_kpis:
            kpi = db.query(KPI).filter(KPI.id == mkpi.kpi_id).first()
            alarms = db.query(AlarmaMercado).filter(AlarmaMercado.mercado_kpi_id == mkpi.id).all()
            if kpi.nombre_kpi not in kpis_with_alarms:
                kpis_with_alarms[kpi.nombre_kpi] = {
                    "pivot_fecha": mkpi.fecha,
                    "resultados": mkpi.resultados,
                    "alarms": []
                }
            for alarm in alarms:
                kpis_with_alarms[kpi.nombre_kpi]["alarms"].append({
                    "alarm_id": alarm.alarma_id,
                    "fecha": alarm.fecha
                })
        
        mercados_with_alarms.append({
            "nombre_mercado": mercado.nombre_mercado,
            "kpis": kpis_with_alarms
        })

    return {
        "regions": regions_with_alarms,
        "markets": mercados_with_alarms
    }

def get_all_markets_and_regions_with_alarms(db: Session):
    regions = db.query(Region).all()
    regions_with_alarms = []
    
    for region in regions:
        region_kpis = db.query(RegionKPI).filter(RegionKPI.region_id == region.id).all()
        kpis_with_alarms = {}
        for rkpi in region_kpis:
            kpi = db.query(KPI).filter(KPI.id == rkpi.kpi_id).first()
            alarms = db.query(Alarma).filter(Alarma.region_kpi == rkpi.id).all()
            if kpi.nombre_kpi not in kpis_with_alarms:
                kpis_with_alarms[kpi.nombre_kpi] = {
                    "pivot_fecha": rkpi.fecha,
                    "resultado": rkpi.resultado,
                    "alarms": []
                }
            for alarm in alarms:
                kpis_with_alarms[kpi.nombre_kpi]["alarms"].append({
                    "alarm_id": alarm.alarma_id,
                    "fecha": alarm.fecha
                })
        
        regions_with_alarms.append({
            "nombre_de_region": region.nombre_de_region,
            "kpis": kpis_with_alarms
        })

    mercados = db.query(Mercado).all()
    mercados_with_alarms = []
    
    for mercado in mercados:
        mercado_kpis = db.query(MercadoKPI).filter(MercadoKPI.mercado_id == mercado.id).all()
        kpis_with_alarms = {}
        for mkpi in mercado_kpis:
            kpi = db.query(KPI).filter(KPI.id == mkpi.kpi_id).first()
            alarms = db.query(AlarmaMercado).filter(AlarmaMercado.mercado_kpi_id == mkpi.id).all()
            if kpi.nombre_kpi not in kpis_with_alarms:
                kpis_with_alarms[kpi.nombre_kpi] = {
                    "pivot_fecha": mkpi.fecha,
                    "resultados": mkpi.resultados,
                    "alarms": []
                }
            for alarm in alarms:
                kpis_with_alarms[kpi.nombre_kpi]["alarms"].append({
                    "alarm_id": alarm.alarma_id,
                    "fecha": alarm.fecha
                })
        
        mercados_with_alarms.append({
            "nombre_mercado": mercado.nombre_mercado,
            "kpis": kpis_with_alarms
        })

    return {
        "regions": regions_with_alarms,
        "markets": mercados_with_alarms
    }