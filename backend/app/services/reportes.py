"""Servicio para reportes"""
from sqlalchemy.orm import Session
from typing import Dict, Optional
from datetime import datetime

from ..repositories import inspeccion_repository


class ReporteService:
    """Servicio para generación de reportes"""
    
    def obtener_conteo_por_estado(self, db: Session) -> Dict[str, int]:
        """Obtiene conteo de inspecciones por estado"""
        resultados = inspeccion_repository.get_conteo_por_estado(db)
        
        conteo = {
            "pending": 0,
            "approved": 0,
            "rejected": 0
        }
        
        for estado, total in resultados:
            conteo[estado] = total
        
        return conteo
    
    def obtener_resumen(
        self,
        db: Session,
        fecha_desde: Optional[str] = None,
        fecha_hasta: Optional[str] = None
    ) -> Dict:
        """Obtiene resumen general de inspecciones"""
        # Convertir fechas
        fecha_desde_dt = None
        fecha_hasta_dt = None
        
        if fecha_desde:
            try:
                fecha_desde_dt = datetime.fromisoformat(fecha_desde)
            except:
                pass
        
        if fecha_hasta:
            try:
                fecha_hasta_dt = datetime.fromisoformat(fecha_hasta)
            except:
                pass
        
        # Obtener inspecciones filtradas
        items, total = inspeccion_repository.get_all(
            db=db,
            skip=0,
            limit=100000,  # Traer todas
            fecha_desde=fecha_desde_dt,
            fecha_hasta=fecha_hasta_dt
        )
        
        # Calcular estadísticas
        aprobadas = sum(1 for i in items if i.estado == 'approved')
        pendientes = sum(1 for i in items if i.estado == 'pending')
        rechazadas = sum(1 for i in items if i.estado == 'rejected')
        
        tasa_aprobacion = (aprobadas / total * 100) if total > 0 else 0
        
        return {
            "total_inspecciones": total,
            "aprobadas": aprobadas,
            "pendientes": pendientes,
            "rechazadas": rechazadas,
            "tasa_aprobacion": round(tasa_aprobacion, 2),
            "periodo_desde": fecha_desde,
            "periodo_hasta": fecha_hasta
        }


reporte_service = ReporteService()
