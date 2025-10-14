"""Router para inspecciones"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional

from ..core import get_db
from ..schemas import (
    Inspeccion,
    InspeccionDetalle,
    InspeccionCreate,
    InspeccionUpdate,
    InspeccionCreated,
    FotoInspeccion,
    PaginatedResponse,
    Message
)
from ..services import inspeccion_service

router = APIRouter(prefix="/inspecciones", tags=["Inspecciones"])


@router.get("", response_model=PaginatedResponse)
def listar_inspecciones(
    page: int = 1,
    page_size: int = 20,
    q: Optional[str] = None,
    planta: Optional[int] = None,
    estado: Optional[str] = None,
    fecha_desde: Optional[str] = None,
    fecha_hasta: Optional[str] = None,
    order_by: str = "inspeccionado_en",
    order_dir: str = "desc",
    db: Session = Depends(get_db)
):
    """
    Listar inspecciones con filtros y paginación
    
    - **q**: Búsqueda por número de contenedor o código
    - **planta**: Filtrar por ID de planta
    - **estado**: Filtrar por estado (pending/approved/rejected)
    - **fecha_desde**: Fecha desde (YYYY-MM-DD)
    - **fecha_hasta**: Fecha hasta (YYYY-MM-DD)
    - **order_by**: Campo para ordenar (inspeccionado_en, numero_contenedor, estado)
    - **order_dir**: Dirección (asc/desc)
    """
    items, total, total_pages = inspeccion_service.listar_inspecciones(
        db=db,
        page=page,
        page_size=page_size,
        q=q,
        id_planta=planta,
        estado=estado,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        order_by=order_by,
        order_dir=order_dir
    )
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }


@router.get("/{id_inspeccion}", response_model=InspeccionDetalle)
def obtener_inspeccion(id_inspeccion: int, db: Session = Depends(get_db)):
    """Obtener detalle completo de una inspección"""
    return inspeccion_service.obtener_inspeccion(db, id_inspeccion)


@router.post("", response_model=InspeccionCreated, status_code=status.HTTP_201_CREATED)
def crear_inspeccion(
    inspeccion_data: InspeccionCreate,
    db: Session = Depends(get_db)
):
    """
    Crear nueva inspección (sin fotos)
    
    Retorna el ID y código para luego subir fotos con POST /inspecciones/{id}/fotos
    """
    inspeccion = inspeccion_service.crear_inspeccion(db, inspeccion_data)
    
    return {
        "id_inspeccion": inspeccion.id_inspeccion,
        "codigo": inspeccion.codigo,
        "mensaje": "Inspección creada exitosamente"
    }


@router.put("/{id_inspeccion}", response_model=Inspeccion)
def actualizar_inspeccion(
    id_inspeccion: int,
    inspeccion_data: InspeccionUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar campos de una inspección existente"""
    return inspeccion_service.actualizar_inspeccion(db, id_inspeccion, inspeccion_data)


@router.delete("/{id_inspeccion}", response_model=Message)
def eliminar_inspeccion(id_inspeccion: int, db: Session = Depends(get_db)):
    """Eliminar inspección y todos sus archivos asociados"""
    inspeccion_service.eliminar_inspeccion(db, id_inspeccion)
    return {"mensaje": f"Inspección {id_inspeccion} eliminada exitosamente"}


@router.post("/{id_inspeccion}/fotos", response_model=List[FotoInspeccion])
async def subir_fotos(
    id_inspeccion: int,
    archivos: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """
    Subir múltiples fotos para una inspección
    
    - Soporta múltiples archivos en una sola petición
    - Formatos: JPG, JPEG, PNG
    - Se guardan en capturas/inspecciones/{id_inspeccion}/
    """
    # Validar tipos de archivo
    valid_types = {"image/jpeg", "image/jpg", "image/png"}
    for archivo in archivos:
        if archivo.content_type not in valid_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de archivo no válido: {archivo.content_type}. Solo se permiten JPG y PNG"
            )
    
    return await inspeccion_service.subir_fotos(db, id_inspeccion, archivos)


@router.delete("/{id_inspeccion}/fotos/{id_foto}", response_model=Message)
def eliminar_foto(
    id_inspeccion: int,
    id_foto: int,
    db: Session = Depends(get_db)
):
    """Eliminar una foto específica de una inspección"""
    inspeccion_service.eliminar_foto(db, id_inspeccion, id_foto)
    return {"mensaje": f"Foto {id_foto} eliminada exitosamente"}


@router.post("/{id_inspeccion}/firma", response_model=Inspeccion)
async def subir_firma(
    id_inspeccion: int,
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Subir firma digital para una inspección
    
    - Formato: PNG o JPG
    - Se guarda en capturas/firmas/{id_inspeccion}.ext
    - Reemplaza firma anterior si existe
    """
    # Validar tipo de archivo
    if archivo.content_type not in {"image/jpeg", "image/jpg", "image/png"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de archivo no válido. Solo se permiten PNG y JPG"
        )
    
    return await inspeccion_service.subir_firma(db, id_inspeccion, archivo)


@router.get("/{id_inspeccion}/pdf")
def generar_pdf(id_inspeccion: int, db: Session = Depends(get_db)):
    """
    Endpoint stub para generación de PDF
    
    El PDF se genera en el frontend con jsPDF.
    Este endpoint retorna los metadatos necesarios.
    """
    inspeccion = inspeccion_service.obtener_inspeccion(db, id_inspeccion)
    
    return {
        "id_inspeccion": inspeccion.id_inspeccion,
        "codigo": inspeccion.codigo,
        "numero_contenedor": inspeccion.numero_contenedor,
        "mensaje": "Use el frontend para generar el PDF con jsPDF"
    }
