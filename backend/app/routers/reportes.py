"""Router para reportes"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional, List
import os
import json
from datetime import datetime

from ..core import get_db
from ..schemas import ConteoEstado, ResumenReporte, Reporte, ReporteCreated, ReporteCreate
from ..services import reporte_service
from ..services.pdf_generator import pdf_generator_service
from ..utils.auth import get_current_user, require_roles
from ..models import Usuario
from ..core.settings import settings
from ..utils.files import ensure_dir
from ..repositories import reporte_repository as _reporte_repo
from ..repositories.inspecciones import inspeccion_repository

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
    id_planta: Optional[int] = None,
    id_navieras: Optional[int] = None,
    id_inspector: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Obtener resumen de inspecciones
    
    - **desde**: Fecha desde (YYYY-MM-DD) - opcional
    - **hasta**: Fecha hasta (YYYY-MM-DD) - opcional
    - **id_planta**: Filtrar por planta - opcional
    - **id_navieras**: Filtrar por naviera - opcional
    - **id_inspector**: Filtrar por inspector - opcional
    
    Retorna estadísticas generales: total, aprobadas, pendientes, rechazadas y tasa de aprobación
    """
    return reporte_service.obtener_resumen(
        db, 
        fecha_desde=desde, 
        fecha_hasta=hasta,
        id_planta=id_planta,
        id_navieras=id_navieras,
        id_inspector=id_inspector
    )


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


@router.post("/pdf/{reporte_id}/firmar")
async def firmar_reporte(
    reporte_id: int,
    archivo: UploadFile = File(...),
    regenerar_pdf: bool = True,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Firma digitalmente un reporte aprobado (revisión por admin/supervisor) y opcionalmente regenera el PDF
    incorporando la firma.

    - Requiere rol: admin o supervisor
    - Solo se permite firmar reportes cuya inspección esté en estado 'approved'
    - Guarda la imagen de la firma y metadatos del revisor
    - Si regenerar_pdf=True, reconstruye el PDF con la firma y actualiza el hash
    """
    require_roles(current_user, ["admin", "supervisor"])

    # Validar reporte e inspección
    reporte = _reporte_repo.get_by_id(db, reporte_id)
    if not reporte:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reporte no encontrado")

    inspeccion = inspeccion_repository.get_by_id(db, reporte.id_inspeccion)
    if not inspeccion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inspección asociada no encontrada")

    if inspeccion.estado != 'approved':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Solo se puede firmar inspecciones aprobadas")

    # Validar tipo
    if archivo.content_type not in {"image/png", "image/jpeg", "image/jpg"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Formato de firma no válido. Use PNG o JPG")

    # Guardar firma en capturas/firmas/revisiones
    firmas_dir = os.path.abspath(os.path.join(settings.CAPTURAS_DIR, "firmas", "revisiones"))
    ensure_dir(firmas_dir)
    ext = ".png" if archivo.content_type == "image/png" else ".jpg"
    firma_path = os.path.join(firmas_dir, f"inspeccion_{inspeccion.id_inspeccion}{ext}")

    contenido = await archivo.read()
    try:
        with open(firma_path, "wb") as f:
            f.write(contenido)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"No se pudo guardar la firma: {e}")

    # Guardar metadatos
    meta = {
        "id_usuario": current_user.id_usuario,
        "nombre": current_user.nombre,
        "rol": current_user.rol,
        "firmado_en": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    meta_path = os.path.join(firmas_dir, f"inspeccion_{inspeccion.id_inspeccion}_revisor.json")
    try:
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
    except Exception as e:
        # No es crítico para el flujo, solo registrar el problema
        print(f"Advertencia: no se pudo guardar metadatos de firma: {e}")

    # Regenerar PDF si se solicita
    if regenerar_pdf:
        try:
            reporte_actualizado = pdf_generator_service.regenerar_pdf_con_firma(db, reporte_id)
            return {
                "mensaje": "Reporte firmado y PDF actualizado exitosamente",
                "id_reporte": reporte_actualizado.id,
                "pdf_ruta": reporte_actualizado.pdf_ruta
            }
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Firma guardada pero error al regenerar PDF: {e}")

    return {"mensaje": "Firma guardada exitosamente"}


