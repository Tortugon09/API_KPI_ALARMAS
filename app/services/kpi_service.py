from sqlalchemy.orm import Session
from models.models import KPI, RegionKPI, MercadoKPI, Alarma, AlarmaMercado, Region, Mercado, ConteoDeAlarmas
from datetime import datetime, timedelta
from datetime import date
from typing import List, Union

def get_all_kpis_with_details(db: Session):
    kpis = db.query(KPI).all()
    kpi_with_details = []
    for kpi in kpis:
        region_kpis = db.query(RegionKPI).filter(RegionKPI.kpi_id == kpi.id).all()
        for rkpi in region_kpis:
            region = db.query(Region).filter(Region.id == rkpi.region_id).first()
            alarms = db.query(Alarma).filter(Alarma.region_kpi == rkpi.id).all()
            kpi_with_details.append({
                "nombre_kpi": kpi.nombre_kpi,
                "related_name": region.nombre_de_region,
                "fecha": rkpi.fecha,
                "alarms": alarms
            })
    return kpi_with_details


def get_kpis_by_region_with_details(db: Session, region_id: int):
    region_kpis = db.query(RegionKPI).filter(RegionKPI.region_id == region_id).all()
    kpi_with_details = []
    for rkpi in region_kpis:
        kpi = db.query(KPI).filter(KPI.id == rkpi.kpi_id).first()
        alarms = db.query(Alarma).filter(Alarma.region_kpi == rkpi.id).all()
        kpi_with_details.append({
            "nombre_kpi": kpi.nombre_kpi,
            "related_name": kpi.nombre_kpi,
            "fecha": rkpi.fecha,
            "alarms": alarms
        })
    return kpi_with_details

def get_kpis_by_market_with_details(db: Session, mercado_id: int):
    mercado_kpis = db.query(MercadoKPI).filter(MercadoKPI.mercado_id == mercado_id).all()
    kpi_with_details = []
    for mkpi in mercado_kpis:
        kpi = db.query(KPI).filter(KPI.id == mkpi.kpi_id).first()
        alarms = db.query(AlarmaMercado).filter(AlarmaMercado.mercado_kpi_id == mkpi.id).all()
        kpi_with_details.append({
            "nombre_kpi": kpi.nombre_kpi,
            "related_name": kpi.nombre_kpi,
            "fecha": mkpi.fecha,
            "alarms": alarms
        })
    return kpi_with_details

def get_alarms_by_market_and_date(db: Session, mercado_id: int, start_date: str, end_date: str):

    conteo_dias = db.query(ConteoDeAlarmas).filter(ConteoDeAlarmas.id.in_([1, 2, 3])).all()
    conteo_dias_dict = {c.id: c.conteo_dias for c in conteo_dias}

    kpis_with_alarms = {}
    mercado_kpis = db.query(MercadoKPI).filter(
        MercadoKPI.mercado_id == mercado_id,
        MercadoKPI.fecha >= start_date,
        MercadoKPI.fecha <= end_date
    ).all()


    all_alarms = db.query(AlarmaMercado).join(MercadoKPI).filter(
        MercadoKPI.mercado_id == mercado_id
    ).all()


    all_alarm_dates = sorted(set(alarm.fecha for alarm in all_alarms))


    max_consecutive_days = 0
    consecutive_days = 1

    if all_alarm_dates:
        previous_date = all_alarm_dates[0]
        for current_date in all_alarm_dates[1:]:
            if (current_date - previous_date).days == 1:
                consecutive_days += 1
            else:
                max_consecutive_days = max(max_consecutive_days, consecutive_days)
                consecutive_days = 1
            previous_date = current_date

        max_consecutive_days = max(max_consecutive_days, consecutive_days)

    if max_consecutive_days >= conteo_dias_dict.get(3, 0):
        severity = "Crítico"
    elif max_consecutive_days >= conteo_dias_dict.get(2, 0):
        severity = "Intermedio"
    elif max_consecutive_days >= conteo_dias_dict.get(1, 0):
        severity = "Alarmado"
    else:
        severity = "Normal"

    for mkpi in mercado_kpis:
        kpi = db.query(KPI).filter(KPI.id == mkpi.kpi_id).first()

        if kpi.nombre_kpi not in kpis_with_alarms:
            kpis_with_alarms[kpi.nombre_kpi] = {
                "consecutive_days_with_alarms": max_consecutive_days,
                "severity": severity,
                "details": []
            }

        alarms_for_date = [
            {"alarm_id": alarm.alarma_id, "fecha": alarm.fecha}
            for alarm in all_alarms if alarm.mercado_kpi_id == mkpi.id
        ]

        kpis_with_alarms[kpi.nombre_kpi]["details"].append({
            "pivot_fecha": mkpi.fecha,
            "resultados": mkpi.resultados,
            "alarms": alarms_for_date,
        })

    return kpis_with_alarms

def get_alarms_by_region_and_date(db: Session, region_id: int, start_date: str, end_date: str):

    conteo_dias = db.query(ConteoDeAlarmas).filter(ConteoDeAlarmas.id.in_([1, 2, 3])).all()
    conteo_dias_dict = {c.id: c.conteo_dias for c in conteo_dias}

    kpis_with_alarms = {}
    region_kpis = db.query(RegionKPI).filter(
        RegionKPI.region_id == region_id,
        RegionKPI.fecha >= start_date,
        RegionKPI.fecha <= end_date
    ).all()

    all_alarms = db.query(Alarma).join(RegionKPI).filter(
        RegionKPI.region_id == region_id
    ).all()

    all_alarm_dates = sorted(set(alarm.fecha for alarm in all_alarms))

    max_consecutive_days = 0
    consecutive_days = 0

    if all_alarm_dates:
        previous_date = all_alarm_dates[0]
        for current_date in all_alarm_dates[1:]:
            if (current_date - previous_date).days == 1:
                consecutive_days += 1
            else:
                max_consecutive_days = max(max_consecutive_days, consecutive_days)
                consecutive_days = 1
            previous_date = current_date

        max_consecutive_days = max(max_consecutive_days, consecutive_days)

    if max_consecutive_days >= conteo_dias_dict.get(3, 0):
        severity = "Crítico"
    elif max_consecutive_days >= conteo_dias_dict.get(2, 0):
        severity = "Intermedio"
    elif max_consecutive_days >= conteo_dias_dict.get(1, 0):
        severity = "Alarmado"
    else:
        severity = "Normal"

    for rkpi in region_kpis:
        kpi = db.query(KPI).filter(KPI.id == rkpi.kpi_id).first()

        if kpi.nombre_kpi not in kpis_with_alarms:
            kpis_with_alarms[kpi.nombre_kpi] = {
                "consecutive_days_with_alarms": max_consecutive_days,
                "severity": severity,
                "details": []
            }

        alarms_for_date = [
            {"alarm_id": alarm.alarma_id, "fecha": alarm.fecha}
            for alarm in all_alarms if alarm.region_kpi == rkpi.id
        ]

        kpis_with_alarms[kpi.nombre_kpi]["details"].append({
            "pivot_fecha": rkpi.fecha,
            "resultado": rkpi.resultado,
            "alarms": alarms_for_date,
        })

    return kpis_with_alarms

def get_markets_by_date_range(db: Session, start_date: str, end_date: str):

    mercados = db.query(Mercado).all()
    mercados_with_alarms = []

    ayer = datetime.now() - timedelta(days=1)
    ayer = ayer.date()

    conteo_dias = db.query(ConteoDeAlarmas).filter(ConteoDeAlarmas.id.in_([1, 2, 3])).all()
    conteo_dias_dict = {c.id: c.conteo_dias for c in conteo_dias}

    for mercado in mercados:
        mercado_kpis = db.query(MercadoKPI).filter(
            MercadoKPI.mercado_id == mercado.id,
            MercadoKPI.fecha >= start_date,
            MercadoKPI.fecha <= end_date
        ).all()

        kpis_with_alarms = {}
        for mkpi in mercado_kpis:
            kpi = db.query(KPI).filter(KPI.id == mkpi.kpi_id).first()

            all_alarms = db.query(AlarmaMercado).join(MercadoKPI).filter(
                MercadoKPI.kpi_id == kpi.id,
                MercadoKPI.mercado_id == mercado.id
            ).all()

            all_alarm_dates = sorted(set(alarm.fecha for alarm in all_alarms))

            max_consecutive_days = 0
            consecutive_days = 0

            if all_alarm_dates:
                previous_date = all_alarm_dates[0]
                for current_date in all_alarm_dates[1:]:
                    if (current_date - previous_date).days == 1:
                        consecutive_days += 1
                    else:
                        max_consecutive_days = max(max_consecutive_days, consecutive_days)
                        consecutive_days = 1
                    previous_date = current_date

                max_consecutive_days = max(max_consecutive_days, consecutive_days)

            if max_consecutive_days >= conteo_dias_dict.get(3, 0):
                severity = "Crítico"
            elif max_consecutive_days >= conteo_dias_dict.get(2, 0):
                severity = "Intermedio"
            elif max_consecutive_days >= conteo_dias_dict.get(1, 0):
                severity = "Alarmado"
            else:
                severity = "Normal"

            if kpi.nombre_kpi not in kpis_with_alarms:
                kpis_with_alarms[kpi.nombre_kpi] = {
                    "consecutive_days_with_alarms": max_consecutive_days,
                    "severity": severity,
                    "details": []
                }

            alarms_for_date = [
                {"alarm_id": alarm.alarma_id, "fecha": alarm.fecha}
                for alarm in all_alarms if alarm.mercado_kpi_id == mkpi.id
            ]

            kpis_with_alarms[kpi.nombre_kpi]["details"].append({
                "pivot_fecha": mkpi.fecha,
                "resultados": mkpi.resultados,
                "alarms": alarms_for_date,
            })

        if kpis_with_alarms:
            mercados_with_alarms.append({
                "nombre_mercado": mercado.nombre_mercado,
                "kpis": kpis_with_alarms
            })

    return mercados_with_alarms

def get_regions_by_date_range(db: Session, start_date: str, end_date: str):

    regions = db.query(Region).all()
    regions_with_alarms = []


    conteo_dias = db.query(ConteoDeAlarmas).filter(ConteoDeAlarmas.id.in_([1, 2, 3])).all()
    conteo_dias_dict = {c.id: c.conteo_dias for c in conteo_dias}

    ayer = datetime.now() - timedelta(days=1)
    ayer = ayer.date() 

    for region in regions:
        region_kpis = db.query(RegionKPI).filter(
            RegionKPI.region_id == region.id,
            RegionKPI.fecha >= start_date,
            RegionKPI.fecha <= end_date
        ).all()

        kpis_with_alarms = {}
        for rkpi in region_kpis:
            kpi = db.query(KPI).filter(KPI.id == rkpi.kpi_id).first()


            all_alarms = db.query(Alarma).join(RegionKPI).filter(
                RegionKPI.kpi_id == kpi.id,
                RegionKPI.region_id == region.id
            ).all()


            all_alarm_dates = sorted(set(alarm.fecha for alarm in all_alarms))


            max_consecutive_days = 0
            consecutive_days = 0

            if all_alarm_dates:
                previous_date = all_alarm_dates[0]
                for current_date in all_alarm_dates[1:]:
                    if (current_date - previous_date).days == 1:
                        consecutive_days += 1
                    else:
                        max_consecutive_days = max(max_consecutive_days, consecutive_days)
                        consecutive_days = 1
                    previous_date = current_date

                max_consecutive_days = max(max_consecutive_days, consecutive_days)


            if max_consecutive_days >= conteo_dias_dict.get(3, 0):
                severity = "Crítico"
            elif max_consecutive_days >= conteo_dias_dict.get(2, 0):
                severity = "Intermedio"
            elif max_consecutive_days >= conteo_dias_dict.get(1, 0):
                severity = "Alarmado"
            else:
                severity = "Normal"

            if kpi.nombre_kpi not in kpis_with_alarms:
                kpis_with_alarms[kpi.nombre_kpi] = {
                    "consecutive_days_with_alarms": max_consecutive_days,
                    "severity": severity,
                    "details": []
                }


            alarms_for_date = [
                {"alarm_id": alarm.alarma_id, "fecha": alarm.fecha}
                for alarm in all_alarms if alarm.region_kpi == rkpi.id
            ]

            kpis_with_alarms[kpi.nombre_kpi]["details"].append({
                "pivot_fecha": rkpi.fecha,
                "resultado": rkpi.resultado,
                "alarms": alarms_for_date,
            })

        if kpis_with_alarms:
            regions_with_alarms.append({
                "nombre_de_region": region.nombre_de_region,
                "kpis": kpis_with_alarms
            })

    return regions_with_alarms

def get_alarms_by_kpi_and_date_last_days_REGION(db: Session, kpi_id: int):

    end_date = datetime.now()
    start_date = end_date - timedelta(days=8)
    
    # Asegúrate de que start_date y end_date sean del tipo datetime
    if isinstance(start_date, datetime):
        pass
    else:
        start_date = datetime.combine(start_date, datetime.min.time())
    
    if isinstance(end_date, datetime):
        pass
    else:
        end_date = datetime.combine(end_date, datetime.min.time())

    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')


    conteo_dias = db.query(ConteoDeAlarmas).filter(ConteoDeAlarmas.id.in_([1, 2, 3])).all()
    conteo_dias_dict = {c.id: c.conteo_dias for c in conteo_dias}


    region_kpis = db.query(RegionKPI).filter(
        RegionKPI.kpi_id == kpi_id,
        RegionKPI.fecha >= start_date_str,
        RegionKPI.fecha <= end_date_str
    ).all()


    all_alarms = db.query(Alarma).join(RegionKPI).filter(
        RegionKPI.kpi_id == kpi_id,
        Alarma.fecha >= start_date_str,
        Alarma.fecha <= end_date_str
    ).all()


    all_alarm_dates = sorted(set(alarm.fecha for alarm in all_alarms))


    max_consecutive_days = 0
    consecutive_days = 0

    if all_alarm_dates:
        previous_date = all_alarm_dates[0]
        for current_date in all_alarm_dates[1:]:
            if (current_date - previous_date).days == 1:
                consecutive_days += 1
            else:
                max_consecutive_days = max(max_consecutive_days, consecutive_days)
                consecutive_days = 1
            previous_date = current_date

        max_consecutive_days = max(max_consecutive_days, consecutive_days)


    if max_consecutive_days >= conteo_dias_dict.get(3, 0):
        severity = "Crítico"
    elif max_consecutive_days >= conteo_dias_dict.get(2, 0):
        severity = "Intermedio"
    elif max_consecutive_days >= conteo_dias_dict.get(1, 0):
        severity = "Alarmado"
    else:
        severity = "Normal"

    regions_with_alarms = {}

    for rkpi in region_kpis:

        region = db.query(Region).filter(Region.id == rkpi.region_id).first()
        if region is None:
            continue
        
        region_name = region.nombre_de_region

        if region_name not in regions_with_alarms:
            regions_with_alarms[region_name] = {
                "consecutive_days_with_alarms": max_consecutive_days,
                "severity": severity,
                "details": []
            }


        alarms_for_date = [
            {"alarm_id": alarm.alarma_id, "fecha": alarm.fecha}
            for alarm in all_alarms if alarm.region_kpi == rkpi.id
        ]


        regions_with_alarms[region_name]["details"].append({
            "pivot_fecha": rkpi.fecha,
            "resultado": rkpi.resultado,
            "alarms": alarms_for_date,
        })

    return regions_with_alarms

def get_alarms_by_kpi_last_days(db: Session, kpi_id: int):

    end_date = datetime.now()
    start_date = end_date - timedelta(days=8)


    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')


    conteo_dias = db.query(ConteoDeAlarmas).filter(ConteoDeAlarmas.id.in_([1, 2, 3])).all()
    conteo_dias_dict = {c.id: c.conteo_dias for c in conteo_dias}

    mercados_with_alarms = {}


    mercados_kpis = db.query(MercadoKPI).filter(
        MercadoKPI.kpi_id == kpi_id,
        MercadoKPI.fecha >= start_date_str,
        MercadoKPI.fecha <= end_date_str
    ).all()

    mercados_ids = {mk.mercado_id for mk in mercados_kpis}


    all_alarms = db.query(AlarmaMercado).join(MercadoKPI).filter(
        MercadoKPI.mercado_id.in_(mercados_ids),
        AlarmaMercado.fecha >= start_date_str,
        AlarmaMercado.fecha <= end_date_str
    ).all()


    all_alarm_dates = sorted(set(alarm.fecha for alarm in all_alarms))


    max_consecutive_days = 0
    consecutive_days = 1

    if all_alarm_dates:
        previous_date = all_alarm_dates[0]
        for current_date in all_alarm_dates[1:]:
            if (current_date - previous_date).days == 1:
                consecutive_days += 1
            else:
                max_consecutive_days = max(max_consecutive_days, consecutive_days)
                consecutive_days = 1
            previous_date = current_date

        max_consecutive_days = max(max_consecutive_days, consecutive_days)


    if max_consecutive_days >= conteo_dias_dict.get(3, 0):
        severity = "Crítico"
    elif max_consecutive_days >= conteo_dias_dict.get(2, 0):
        severity = "Intermedio"
    elif max_consecutive_days >= conteo_dias_dict.get(1, 0):
        severity = "Alarmado"
    else:
        severity = "Normal"

    for mk in mercados_kpis:
        mercado = db.query(Mercado).filter(Mercado.id == mk.mercado_id).first()

        if mercado:
            if mercado.nombre_mercado not in mercados_with_alarms:
                mercados_with_alarms[mercado.nombre_mercado] = {
                    "consecutive_days_with_alarms": max_consecutive_days,
                    "severity": severity,
                    "details": []
                }

            # Filtrar las alarmas para la fecha actual de mk
            alarms_for_date = [
                {"alarm_id": alarm.alarma_id, "fecha": alarm.fecha}
                for alarm in all_alarms if alarm.mercado_kpi_id == mk.id
            ]

            # Agregar los detalles para la fecha `pivot_fecha`
            mercados_with_alarms[mercado.nombre_mercado]["details"].append({
                "pivot_fecha": mk.fecha,
                "resultados": mk.resultados,
                "alarms": alarms_for_date,
            })

    return mercados_with_alarms