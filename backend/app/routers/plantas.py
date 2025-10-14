"""Router para plantas"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..core import get_db
from ..schemas import Planta, PlantaCreate, PlantaUpdate, Message
from ..repositories import planta_repository

router = APIRouter(prefix="/plantas", tags=["Plantas"])


@router.get("", response_model=List[Planta])
def listar_plantas(db: Session = Depends(get_db)):
    """Obtener todas las plantas"""
    return planta_repository.get_all(db)


@router.post("", response_model=Planta, status_code=status.HTTP_201_CREATED)
def crear_planta(planta_data: PlantaCreate, db: Session = Depends(get_db)):
    """Crear nueva planta"""
    # Verificar código único
    existing = planta_repository.get_by_codigo(db, planta_data.codigo)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe una planta con código '{planta_data.codigo}'"
        )
    
    return planta_repository.create(db, planta_data)


@router.put("/{id_planta}", response_model=Planta)
def actualizar_planta(
    id_planta: int,
    planta_data: PlantaUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar planta existente"""
    planta = planta_repository.get_by_id(db, id_planta)
    if not planta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Planta {id_planta} no encontrada"
        )
    
    # Verificar código único si se está actualizando
    if planta_data.codigo and planta_data.codigo != planta.codigo:
        existing = planta_repository.get_by_codigo(db, planta_data.codigo)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe una planta con código '{planta_data.codigo}'"
            )
    
    return planta_repository.update(db, planta, planta_data)


@router.delete("/{id_planta}", response_model=Message)
def eliminar_planta(id_planta: int, db: Session = Depends(get_db)):
    """Eliminar planta"""
    planta = planta_repository.get_by_id(db, id_planta)
    if not planta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Planta {id_planta} no encontrada"
        )
    
    try:
        planta_repository.delete(db, planta)
        return {"mensaje": f"Planta '{planta.nombre}' eliminada exitosamente"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar la planta porque tiene inspecciones asociadas"
        )
