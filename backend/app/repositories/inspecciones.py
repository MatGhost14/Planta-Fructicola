"""Repositorio para inspecciones"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, or_
from typing import List, Optional, Tuple
from datetime import datetime
from ..models import Inspeccion, FotoInspeccion


class InspeccionRepository:
    """Repositorio para operaciones CRUD de inspecciones"""
    
    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        q: Optional[str] = None,
        id_planta: Optional[int] = None,
        estado: Optional[str] = None,
        fecha_desde: Optional[datetime] = None,
        fecha_hasta: Optional[datetime] = None,
        order_by: str = "inspeccionado_en",
        order_dir: str = "desc",
        id_inspector: Optional[int] = None
    ) -> Tuple[List[Inspeccion], int]:
        """Obtener inspecciones con filtros y paginación"""
        query = db.query(Inspeccion)
        
        # Filtros
        if q:
            query = query.filter(
                or_(
                    Inspeccion.numero_contenedor.ilike(f"%{q}%"),
                    Inspeccion.codigo.ilike(f"%{q}%")
                )
            )
        
        if id_planta:
            query = query.filter(Inspeccion.id_planta == id_planta)
        
        if estado:
            query = query.filter(Inspeccion.estado == estado)
        
        if fecha_desde:
            query = query.filter(Inspeccion.inspeccionado_en >= fecha_desde)
        
        if fecha_hasta:
            query = query.filter(Inspeccion.inspeccionado_en <= fecha_hasta)
        
        # Filtro por inspector (para role inspector)
        if id_inspector:
            query = query.filter(Inspeccion.id_inspector == id_inspector)
        
        # Contar total
        total = query.count()
        
        # Ordenamiento
        order_column = getattr(Inspeccion, order_by, Inspeccion.inspeccionado_en)
        if order_dir == "desc":
            query = query.order_by(order_column.desc())
        else:
            query = query.order_by(order_column.asc())
        
        # Paginación
        items = query.offset(skip).limit(limit).all()
        
        return items, total
    
    def get_by_id(self, db: Session, id_inspeccion: int) -> Optional[Inspeccion]:
        """Obtener inspección por ID con relaciones cargadas"""
        return (
            db.query(Inspeccion)
            .options(
                joinedload(Inspeccion.planta),
                joinedload(Inspeccion.naviera),
                joinedload(Inspeccion.inspector),
                joinedload(Inspeccion.fotos)
            )
            .filter(Inspeccion.id_inspeccion == id_inspeccion)
            .first()
        )
    
    def get_by_codigo(self, db: Session, codigo: str) -> Optional[Inspeccion]:
        """Obtener inspección por código"""
        return db.query(Inspeccion).filter(Inspeccion.codigo == codigo).first()
    
    def create(self, db: Session, inspeccion_data: dict) -> Inspeccion:
        """Crear nueva inspección"""
        inspeccion = Inspeccion(**inspeccion_data)
        db.add(inspeccion)
        db.commit()
        db.refresh(inspeccion)
        return inspeccion
    
    def update(self, db: Session, inspeccion: Inspeccion, update_data: dict) -> Inspeccion:
        """Actualizar inspección existente"""
        for key, value in update_data.items():
            if value is not None:
                setattr(inspeccion, key, value)
        db.commit()
        db.refresh(inspeccion)
        return inspeccion
    
    def update_firma_path(self, db: Session, inspeccion: Inspeccion, firma_path: str) -> Inspeccion:
        """Actualizar ruta de firma"""
        inspeccion.firma_path = firma_path
        db.commit()
        db.refresh(inspeccion)
        return inspeccion
    
    def delete(self, db: Session, inspeccion: Inspeccion) -> None:
        """Eliminar inspección"""
        db.delete(inspeccion)
        db.commit()
    
    def get_conteo_por_estado(self, db: Session) -> List[Tuple[str, int]]:
        """Obtener conteo de inspecciones por estado"""
        return (
            db.query(Inspeccion.estado, func.count(Inspeccion.id_inspeccion))
            .group_by(Inspeccion.estado)
            .all()
        )


class FotoInspeccionRepository:
    """Repositorio para fotos de inspección"""
    
    def create(self, db: Session, foto_data: dict) -> FotoInspeccion:
        """Crear nueva foto"""
        foto = FotoInspeccion(**foto_data)
        db.add(foto)
        db.commit()
        db.refresh(foto)
        return foto
    
    def get_by_id(self, db: Session, id_foto: int) -> Optional[FotoInspeccion]:
        """Obtener foto por ID"""
        return db.query(FotoInspeccion).filter(FotoInspeccion.id_foto == id_foto).first()
    
    def get_by_inspeccion(self, db: Session, id_inspeccion: int) -> List[FotoInspeccion]:
        """Obtener fotos de una inspección"""
        return (
            db.query(FotoInspeccion)
            .filter(FotoInspeccion.id_inspeccion == id_inspeccion)
            .order_by(FotoInspeccion.orden, FotoInspeccion.tomada_en)
            .all()
        )
    
    def delete(self, db: Session, foto: FotoInspeccion) -> None:
        """Eliminar foto"""
        db.delete(foto)
        db.commit()


inspeccion_repository = InspeccionRepository()
foto_repository = FotoInspeccionRepository()
