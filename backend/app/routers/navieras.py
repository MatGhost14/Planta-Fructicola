"""Router para navieras"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..core import get_db
from ..models import Usuario
from ..schemas import Naviera, NavieraCreate, NavieraUpdate, Message
from ..repositories import naviera_repository
from ..utils.auth import get_current_user, require_supervisor

router = APIRouter(prefix="/navieras", tags=["Navieras"])


@router.get("", response_model=List[Naviera])
def listar_navieras(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtener todas las navieras
    
    **Accesible para todos los usuarios autenticados**
    """
    return naviera_repository.get_all(db)


@router.post("", response_model=Naviera, status_code=status.HTTP_201_CREATED)
def crear_naviera(
    naviera_data: NavieraCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_supervisor)
):
    """
    Crear nueva naviera
    
    **Requiere rol: Supervisor o Admin**
    """
    # Verificar código único
    existing = naviera_repository.get_by_codigo(db, naviera_data.codigo)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe una naviera con código '{naviera_data.codigo}'"
        )
    
    return naviera_repository.create(db, naviera_data)


@router.put("/{id_navieras}", response_model=Naviera)
def actualizar_naviera(
    id_navieras: int,
    naviera_data: NavieraUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_supervisor)
):
    """
    Actualizar naviera existente
    
    **Requiere rol: Supervisor o Admin**
    """
    naviera = naviera_repository.get_by_id(db, id_navieras)
    if not naviera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Naviera {id_navieras} no encontrada"
        )
    
    # Verificar código único si se está actualizando
    if naviera_data.codigo and naviera_data.codigo != naviera.codigo:
        existing = naviera_repository.get_by_codigo(db, naviera_data.codigo)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe una naviera con código '{naviera_data.codigo}'"
            )
    
    return naviera_repository.update(db, naviera, naviera_data)


@router.delete("/{id_navieras}", response_model=Message)
def eliminar_naviera(
    id_navieras: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_supervisor)
):
    """
    Eliminar naviera
    
    **Requiere rol: Supervisor o Admin**
    """
    naviera = naviera_repository.get_by_id(db, id_navieras)
    if not naviera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Naviera {id_navieras} no encontrada"
        )
    
    try:
        naviera_repository.delete(db, naviera)
        return {"mensaje": f"Naviera '{naviera.nombre}' eliminada exitosamente"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar la naviera porque tiene inspecciones asociadas"
        )
