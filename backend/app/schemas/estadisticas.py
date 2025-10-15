"""
Schemas para estadísticas y dashboard
"""
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import date


class EstadisticasGeneral(BaseModel):
    """Estadísticas generales del sistema"""
    total_inspecciones: int
    pendientes: int
    aprobadas: int
    rechazadas: int
    total_usuarios: int
    total_plantas: int
    total_navieras: int


class InspeccionPorEstado(BaseModel):
    """Conteo de inspecciones por estado"""
    estado: str
    cantidad: int
    porcentaje: float


class InspeccionPorFecha(BaseModel):
    """Inspecciones agrupadas por fecha"""
    fecha: date
    cantidad: int


class InspeccionPorPlanta(BaseModel):
    """Inspecciones por planta"""
    planta: str
    cantidad: int


class InspeccionPorInspector(BaseModel):
    """Inspecciones por inspector"""
    inspector: str
    total: int
    pendientes: int
    aprobadas: int
    rechazadas: int


class DashboardData(BaseModel):
    """Datos completos para el dashboard"""
    estadisticas_generales: EstadisticasGeneral
    por_estado: List[InspeccionPorEstado]
    por_fecha: List[InspeccionPorFecha]  # Últimos 30 días
    por_planta: List[InspeccionPorPlanta]
    por_inspector: List[InspeccionPorInspector]
    fecha_desde: date
    fecha_hasta: date
