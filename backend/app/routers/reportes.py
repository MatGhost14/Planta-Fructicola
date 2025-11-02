"""Router para reportes"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional, List
import os

from ..core import get_db
from ..schemas import ConteoEstado, ResumenReporte, Reporte, ReporteCreated, ReporteCreate
from ..services import reporte_service
from ..services.pdf_generator import pdf_generator_service
from ..utils.auth import get_current_user, require_roles
from ..models import Usuario

router = APIRouter(prefix="/reportes", tags=["Reportes"])


@router.get("/conteo-estado", response_model=List[ConteoEstado])
def obtener_conteo_por_estado(db: Session = Depends(get_db)):
    """
    Obtener conteo de inspecciones por estado
    
    Retorna la cantidad de inspecciones en cada estado: pending, approved, rejected
    """
    conteo = reporte_service.obtener_conteo_por_estado(db)
    
    return [
        {"estado": estado, "total": total}
        for estado, total in conteo.items()
    ]


@router.get("/resumen", response_model=ResumenReporte)
def obtener_resumen(
    desde: Optional[str] = None,
    hasta: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Obtener resumen de inspecciones
    
    - **desde**: Fecha desde (YYYY-MM-DD) - opcional
    - **hasta**: Fecha hasta (YYYY-MM-DD) - opcional
    
    Retorna estadísticas generales: total, aprobadas, pendientes, rechazadas y tasa de aprobación
    """
    return reporte_service.obtener_resumen(db, fecha_desde=desde, fecha_hasta=hasta)


# ===== GENERACIÓN DE PDF =====

@router.post("/pdf/generar", response_model=ReporteCreated, status_code=status.HTTP_201_CREATED)
def generar_pdf_inspeccion(
    data: ReporteCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Genera un PDF estándar para una inspección
    
    Validaciones:
    - Inspección debe tener al menos 1 evidencia
    - Campos obligatorios completos
    - Solo ADMIN puede generar PDFs
    """
    require_roles(current_user, ["admin"])
    
    try:
        # Generar el PDF utilizando el servicio
        # Nota: el método del servicio se llama 'generar_pdf'
        reporte = pdf_generator_service.generar_pdf(db, data.id_inspeccion)
        
        return ReporteCreated(
            id_reporte=reporte.id,
            uuid_reporte=reporte.uuid_reporte,
            pdf_ruta=reporte.pdf_ruta,
            mensaje="Reporte PDF generado exitosamente"
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al generar PDF: {str(e)}")


@router.get("/pdf/{reporte_id}/descargar")
def descargar_pdf(
    reporte_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Descarga el archivo PDF de un reporte"""
    from ..repositories import reporte_repository
    
    reporte = reporte_repository.get_by_id(db, reporte_id)
    if not reporte:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reporte no encontrado")
    
    if not os.path.exists(reporte.pdf_ruta):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Archivo PDF no encontrado")
    
    filename = os.path.basename(reporte.pdf_ruta)
    return FileResponse(path=reporte.pdf_ruta, media_type="application/pdf", filename=filename)


