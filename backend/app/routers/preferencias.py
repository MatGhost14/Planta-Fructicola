"""Router para preferencias de usuario"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core import get_db
from ..schemas import PreferenciaUsuario, PreferenciaUsuarioUpdate
from ..repositories import preferencia_repository, usuario_repository

router = APIRouter(prefix="/preferencias", tags=["Preferencias"])


@router.get("/{id_usuario}", response_model=PreferenciaUsuario)
def obtener_preferencias(id_usuario: int, db: Session = Depends(get_db)):
    """Obtener preferencias de un usuario"""
    # Verificar que el usuario existe
    usuario = usuario_repository.get_by_id(db, id_usuario)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario {id_usuario} no encontrado"
        )
    
    preferencia = preferencia_repository.get_by_usuario(db, id_usuario)
    if not preferencia:
        # Crear preferencias por defecto si no existen
        preferencia = preferencia_repository.create(db, id_usuario)
    
    return preferencia


@router.put("/{id_usuario}", response_model=PreferenciaUsuario)
def actualizar_preferencias(
    id_usuario: int,
    preferencia_data: PreferenciaUsuarioUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar preferencias de un usuario"""
    # Verificar que el usuario existe
    usuario = usuario_repository.get_by_id(db, id_usuario)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario {id_usuario} no encontrado"
        )
    
    preferencia = preferencia_repository.get_by_usuario(db, id_usuario)
    if not preferencia:
        # Crear si no existe
        preferencia = preferencia_repository.create(
            db,
            id_usuario,
            **preferencia_data.model_dump()
        )
    else:
        # Actualizar existente
        preferencia = preferencia_repository.update(
            db,
            preferencia,
            preferencia_data.model_dump()
        )
    
    return preferencia
