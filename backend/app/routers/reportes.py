"""Router para reportes"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional, List

from ..core import get_db
from ..schemas import ConteoEstado, ResumenReporte
from ..services import reporte_service

router = APIRouter(prefix="/reportes", tags=["Reportes"])


@router.get("/conteo-estado", response_model=List[ConteoEstado])
def obtener_conteo_por_estado(db: Session = Depends(get_db)):
    """
    Obtener conteo de inspecciones por estado
    
    Retorna la cantidad de inspecciones en cada estado: pending, approved, rejected
    """
    conteo = reporte_service.obtener_conteo_por_estado(db)
    
    return [
        {"estado": estado, "total": total}
        for estado, total in conteo.items()
    ]


@router.get("/resumen", response_model=ResumenReporte)
def obtener_resumen(
    desde: Optional[str] = None,
    hasta: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Obtener resumen de inspecciones
    
    - **desde**: Fecha desde (YYYY-MM-DD) - opcional
    - **hasta**: Fecha hasta (YYYY-MM-DD) - opcional
    
    Retorna estadísticas generales: total, aprobadas, pendientes, rechazadas y tasa de aprobación
    """
    return reporte_service.obtener_resumen(db, fecha_desde=desde, fecha_hasta=hasta)
