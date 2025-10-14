"""Repositorio para preferencias de usuario"""
from sqlalchemy.orm import Session
from typing import Optional
from ..models import PreferenciaUsuario


class PreferenciaRepository:
    """Repositorio para preferencias de usuario"""
    
    def get_by_usuario(self, db: Session, id_usuario: int) -> Optional[PreferenciaUsuario]:
        """Obtener preferencias de un usuario"""
        return db.query(PreferenciaUsuario).filter(
            PreferenciaUsuario.id_usuario == id_usuario
        ).first()
    
    def create(self, db: Session, id_usuario: int, **kwargs) -> PreferenciaUsuario:
        """Crear preferencias para un usuario"""
        preferencia = PreferenciaUsuario(id_usuario=id_usuario, **kwargs)
        db.add(preferencia)
        db.commit()
        db.refresh(preferencia)
        return preferencia
    
    def update(self, db: Session, preferencia: PreferenciaUsuario, update_data: dict) -> PreferenciaUsuario:
        """Actualizar preferencias"""
        for key, value in update_data.items():
            setattr(preferencia, key, value)
        db.commit()
        db.refresh(preferencia)
        return preferencia


preferencia_repository = PreferenciaRepository()
