"""Router para plantas"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..core import get_db
from ..models import Usuario
from ..schemas import Planta, PlantaCreate, PlantaUpdate, Message
from ..repositories import planta_repository
from ..utils.auth import get_current_user, require_supervisor

router = APIRouter(prefix="/plantas", tags=["Plantas"])


@router.get("/test")
def listar_plantas_test():
    """
    Endpoint de prueba sin autenticación
    """
    return {"mensaje": "Endpoint de prueba funcionando", "plantas": 5}


@router.get("", response_model=List[Planta])
def listar_plantas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtener todas las plantas
    
    **Accesible para todos los usuarios autenticados**
    """
    return planta_repository.get_all(db)


@router.post("", response_model=Planta, status_code=status.HTTP_201_CREATED)
def crear_planta(
    planta_data: PlantaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_supervisor)
):
    """
    Crear nueva planta
    
    **Requiere rol: Supervisor o Admin**
    """
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
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_supervisor)
):
    """
    Actualizar planta existente
    
    **Requiere rol: Supervisor o Admin**
    """
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
def eliminar_planta(
    id_planta: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_supervisor)
):
    """
    Eliminar planta
    
    **Requiere rol: Supervisor o Admin**
    """
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
