"""Router para navieras"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..core import get_db
from ..schemas import Naviera, NavieraCreate, NavieraUpdate, Message
from ..repositories import naviera_repository

router = APIRouter(prefix="/navieras", tags=["Navieras"])


@router.get("", response_model=List[Naviera])
def listar_navieras(db: Session = Depends(get_db)):
    """Obtener todas las navieras"""
    return naviera_repository.get_all(db)


@router.post("", response_model=Naviera, status_code=status.HTTP_201_CREATED)
def crear_naviera(naviera_data: NavieraCreate, db: Session = Depends(get_db)):
    """Crear nueva naviera"""
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
    db: Session = Depends(get_db)
):
    """Actualizar naviera existente"""
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
def eliminar_naviera(id_navieras: int, db: Session = Depends(get_db)):
    """Eliminar naviera"""
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
