"""Repositorio para plantas"""
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import Planta
from ..schemas import PlantaCreate, PlantaUpdate


class PlantaRepository:
    """Repositorio para operaciones CRUD de plantas"""
    
    def get_all(self, db: Session) -> List[Planta]:
        """Obtener todas las plantas"""
        return db.query(Planta).order_by(Planta.nombre).all()
    
    def get_by_id(self, db: Session, id_planta: int) -> Optional[Planta]:
        """Obtener planta por ID"""
        return db.query(Planta).filter(Planta.id_planta == id_planta).first()
    
    def get_by_codigo(self, db: Session, codigo: str) -> Optional[Planta]:
        """Obtener planta por código"""
        return db.query(Planta).filter(Planta.codigo == codigo).first()
    
    def create(self, db: Session, planta_data: PlantaCreate) -> Planta:
        """Crear nueva planta"""
        planta = Planta(**planta_data.model_dump())
        db.add(planta)
        db.commit()
        db.refresh(planta)
        return planta
    
    def update(self, db: Session, planta: Planta, planta_data: PlantaUpdate) -> Planta:
        """Actualizar planta existente"""
        update_data = planta_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(planta, key, value)
        db.commit()
        db.refresh(planta)
        return planta
    
    def delete(self, db: Session, planta: Planta) -> None:
        """Eliminar planta"""
        db.delete(planta)
        db.commit()


planta_repository = PlantaRepository()
