"""Router para usuarios"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..core import get_db
from ..models import Usuario as UsuarioModel
from ..schemas import Usuario, UsuarioCreate, UsuarioUpdate, UsuarioEstado, Message
from ..repositories import usuario_repository
from ..utils.auth import get_current_user, require_admin

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("", response_model=List[Usuario])
def listar_usuarios(
    include_inactive: bool = False,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(require_admin)
):
    """
    Obtener todos los usuarios
    
    **Requiere rol: Admin**
    """
    return usuario_repository.get_all(db, include_inactive=include_inactive)


@router.post("", response_model=Usuario, status_code=status.HTTP_201_CREATED)
def crear_usuario(
    usuario_data: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(require_admin)
):
    """
    Crear nuevo usuario
    
    **Requiere rol: Admin**
    """
    # Verificar correo único
    existing = usuario_repository.get_by_correo(db, usuario_data.correo)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un usuario con correo '{usuario_data.correo}'"
        )
    
    return usuario_repository.create(db, usuario_data)


@router.put("/{id_usuario}", response_model=Usuario)
def actualizar_usuario(
    id_usuario: int,
    usuario_data: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(require_admin)
):
    """
    Actualizar usuario existente
    
    **Requiere rol: Admin**
    """
    usuario = usuario_repository.get_by_id(db, id_usuario)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario {id_usuario} no encontrado"
        )
    
    # Verificar correo único si se está actualizando
    if usuario_data.correo and usuario_data.correo != usuario.correo:
        existing = usuario_repository.get_by_correo(db, usuario_data.correo)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un usuario con correo '{usuario_data.correo}'"
            )
    
    return usuario_repository.update(db, usuario, usuario_data)


@router.patch("/{id_usuario}/estado", response_model=Usuario)
def cambiar_estado_usuario(
    id_usuario: int,
    estado_data: UsuarioEstado,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(require_admin)
):
    """
    Cambiar estado de usuario (active/inactive)
    
    **Requiere rol: Admin**
    """
    usuario = usuario_repository.get_by_id(db, id_usuario)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario {id_usuario} no encontrado"
        )
    
    return usuario_repository.update_estado(db, usuario, estado_data.estado)


@router.delete("/{id_usuario}", response_model=Message)
def eliminar_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(require_admin)
):
    """
    Eliminar usuario
    
    **Requiere rol: Admin**
    """
    usuario = usuario_repository.get_by_id(db, id_usuario)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario {id_usuario} no encontrado"
        )
    
    try:
        usuario_repository.delete(db, usuario)
        return {"mensaje": f"Usuario '{usuario.nombre}' eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar el usuario porque tiene inspecciones asociadas"
        )
