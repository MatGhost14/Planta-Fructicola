"""Repositorio para reportes PDF"""
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import Reporte


class ReporteRepository:
    """Repositorio para operaciones CRUD de reportes PDF"""
    
    def create(self, db: Session, reporte_data: dict) -> Reporte:
        """Crear nuevo reporte"""
        reporte = Reporte(**reporte_data)
        db.add(reporte)
        db.commit()
        db.refresh(reporte)
        return reporte
    
    def get_by_id(self, db: Session, id_reporte: int) -> Optional[Reporte]:
        """Obtener reporte por ID"""
        return (
            db.query(Reporte)
            .filter(Reporte.id == id_reporte)
            .first()
        )
    
    def get_by_uuid(self, db: Session, uuid_reporte: str) -> Optional[Reporte]:
        """Obtener reporte por UUID"""
        return (
            db.query(Reporte)
            .filter(Reporte.uuid_reporte == uuid_reporte)
            .first()
        )
    
    def get_by_inspeccion(self, db: Session, id_inspeccion: int) -> List[Reporte]:
        """Obtener todos los reportes de una inspección"""
        return (
            db.query(Reporte)
            .filter(Reporte.id_inspeccion == id_inspeccion)
            .order_by(Reporte.creado_en.desc())
            .all()
        )
    
    def delete(self, db: Session, reporte: Reporte) -> None:
        """Eliminar reporte"""
        db.delete(reporte)
        db.commit()


reporte_repository = ReporteRepository()
