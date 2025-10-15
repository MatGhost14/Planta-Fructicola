"""
Router de estadísticas y dashboard
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from datetime import datetime, timedelta
from typing import Optional
import logging

from ..core.database import get_db
from ..models import Inspeccion, Usuario, Planta, Naviera
from ..schemas.estadisticas import (
    DashboardData,
    EstadisticasGeneral,
    InspeccionPorEstado,
    InspeccionPorFecha,
    InspeccionPorPlanta,
    InspeccionPorInspector
)
from ..utils.auth import get_current_active_user

router = APIRouter(prefix="/estadisticas", tags=["Estadísticas"])
logger = logging.getLogger(__name__)


@router.get("/dashboard", response_model=DashboardData)
def get_dashboard_data(
    fecha_desde: Optional[str] = None,
    fecha_hasta: Optional[str] = None,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener datos para el dashboard
    - Inspector: Solo sus propias inspecciones
    - Supervisor: Inspecciones de su planta
    - Admin: Todas las inspecciones
    """
    
    # Fechas por defecto: últimos 30 días
    if not fecha_hasta:
        fecha_hasta_dt = datetime.now()
    else:
        fecha_hasta_dt = datetime.strptime(fecha_hasta, "%Y-%m-%d")
    
    if not fecha_desde:
        fecha_desde_dt = fecha_hasta_dt - timedelta(days=30)
    else:
        fecha_desde_dt = datetime.strptime(fecha_desde, "%Y-%m-%d")
    
    # Filtrar por rol
    query = db.query(Inspeccion).filter(
        Inspeccion.inspeccionado_en >= fecha_desde_dt,
        Inspeccion.inspeccionado_en <= fecha_hasta_dt
    )
    
    if current_user.rol == 'inspector':
        # Inspector solo ve sus inspecciones
        query = query.filter(Inspeccion.id_inspector == current_user.id_usuario)
    elif current_user.rol == 'supervisor':
        # Supervisor ve inspecciones de su planta
        # TODO: Agregar campo id_planta a Usuario
        pass  # Por ahora ve todas
    
    # 1. Estadísticas generales
    total_inspecciones = query.count()
    pendientes = query.filter(Inspeccion.estado == 'pending').count()
    aprobadas = query.filter(Inspeccion.estado == 'approved').count()
    rechazadas = query.filter(Inspeccion.estado == 'rejected').count()
    
    estadisticas_generales = EstadisticasGeneral(
        total_inspecciones=total_inspecciones,
        pendientes=pendientes,
        aprobadas=aprobadas,
        rechazadas=rechazadas,
        total_usuarios=db.query(Usuario).count(),
        total_plantas=db.query(Planta).count(),
        total_navieras=db.query(Naviera).count()
    )
    
    # 2. Por estado
    por_estado = []
    for estado in ['pending', 'approved', 'rejected']:
        cantidad = query.filter(Inspeccion.estado == estado).count()
        porcentaje = (cantidad / total_inspecciones * 100) if total_inspecciones > 0 else 0
        por_estado.append(InspeccionPorEstado(
            estado=estado,
            cantidad=cantidad,
            porcentaje=round(porcentaje, 2)
        ))
    
    # 3. Por fecha (últimos 30 días)
    por_fecha_raw = db.query(
        func.date(Inspeccion.inspeccionado_en).label('fecha'),
        func.count(Inspeccion.id_inspeccion).label('cantidad')
    ).filter(
        Inspeccion.inspeccionado_en >= fecha_desde_dt,
        Inspeccion.inspeccionado_en <= fecha_hasta_dt
    ).group_by(
        func.date(Inspeccion.inspeccionado_en)
    ).all()
    
    por_fecha = [
        InspeccionPorFecha(fecha=row.fecha, cantidad=row.cantidad)
        for row in por_fecha_raw
    ]
    
    # 4. Por planta (top 10)
    por_planta_raw = db.query(
        Planta.nombre.label('planta'),
        func.count(Inspeccion.id_inspeccion).label('cantidad')
    ).join(
        Inspeccion, Planta.id_planta == Inspeccion.id_planta
    ).filter(
        Inspeccion.inspeccionado_en >= fecha_desde_dt,
        Inspeccion.inspeccionado_en <= fecha_hasta_dt
    ).group_by(
        Planta.nombre
    ).order_by(
        func.count(Inspeccion.id_inspeccion).desc()
    ).limit(10).all()
    
    por_planta = [
        InspeccionPorPlanta(planta=row.planta, cantidad=row.cantidad)
        for row in por_planta_raw
    ]
    
    # 5. Por inspector
    por_inspector_raw = db.query(
        Usuario.nombre.label('inspector'),
        func.count(Inspeccion.id_inspeccion).label('total'),
        func.sum(case((Inspeccion.estado == 'pending', 1), else_=0)).label('pendientes'),
        func.sum(case((Inspeccion.estado == 'approved', 1), else_=0)).label('aprobadas'),
        func.sum(case((Inspeccion.estado == 'rejected', 1), else_=0)).label('rechazadas')
    ).join(
        Inspeccion, Usuario.id_usuario == Inspeccion.id_inspector
    ).filter(
        Inspeccion.inspeccionado_en >= fecha_desde_dt,
        Inspeccion.inspeccionado_en <= fecha_hasta_dt
    ).group_by(
        Usuario.nombre
    ).all()
    
    por_inspector = [
        InspeccionPorInspector(
            inspector=row.inspector,
            total=row.total,
            pendientes=row.pendientes or 0,
            aprobadas=row.aprobadas or 0,
            rechazadas=row.rechazadas or 0
        )
        for row in por_inspector_raw
    ]
    
    logger.info(f"Dashboard generado para {current_user.correo} ({current_user.rol})")
    
    return DashboardData(
        estadisticas_generales=estadisticas_generales,
        por_estado=por_estado,
        por_fecha=por_fecha,
        por_planta=por_planta,
        por_inspector=por_inspector,
        fecha_desde=fecha_desde_dt.date(),
        fecha_hasta=fecha_hasta_dt.date()
    )
