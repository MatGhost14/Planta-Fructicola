"""Repositorio para navieras"""
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import Naviera
from ..schemas import NavieraCreate, NavieraUpdate


class NavieraRepository:
    """Repositorio para operaciones CRUD de navieras"""
    
    def get_all(self, db: Session) -> List[Naviera]:
        """Obtener todas las navieras"""
        return db.query(Naviera).order_by(Naviera.nombre).all()
    
    def get_by_id(self, db: Session, id_navieras: int) -> Optional[Naviera]:
        """Obtener naviera por ID"""
        return db.query(Naviera).filter(Naviera.id_navieras == id_navieras).first()
    
    def get_by_codigo(self, db: Session, codigo: str) -> Optional[Naviera]:
        """Obtener naviera por código"""
        return db.query(Naviera).filter(Naviera.codigo == codigo).first()
    
    def create(self, db: Session, naviera_data: NavieraCreate) -> Naviera:
        """Crear nueva naviera"""
        naviera = Naviera(**naviera_data.model_dump())
        db.add(naviera)
        db.commit()
        db.refresh(naviera)
        return naviera
    
    def update(self, db: Session, naviera: Naviera, naviera_data: NavieraUpdate) -> Naviera:
        """Actualizar naviera existente"""
        update_data = naviera_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(naviera, key, value)
        db.commit()
        db.refresh(naviera)
        return naviera
    
    def delete(self, db: Session, naviera: Naviera) -> None:
        """Eliminar naviera"""
        db.delete(naviera)
        db.commit()


naviera_repository = NavieraRepository()
