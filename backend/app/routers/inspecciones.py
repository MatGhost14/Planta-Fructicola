"""Router para inspecciones"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import io
import csv
from datetime import datetime

from ..core import get_db
from ..models import Usuario
from ..schemas import (
    Inspeccion,
    InspeccionDetalle,
    InspeccionCreate,
    InspeccionUpdate,
    InspeccionEstadoUpdate,
    InspeccionCreated,
    FotoInspeccion,
    PaginatedResponse,
    Message
)
from ..services import inspeccion_service
from ..repositories.plantas import planta_repository
from ..repositories.navieras import naviera_repository
from ..repositories.usuarios import usuario_repository
from ..utils.auth import get_current_user
from ..core.settings import settings

router = APIRouter(prefix="/inspecciones", tags=["Inspecciones"])


@router.get("", response_model=PaginatedResponse)
def listar_inspecciones(
    page: int = 1,
    page_size: int = 20,
    q: Optional[str] = None,
    planta: Optional[int] = None,
    naviera: Optional[int] = None,
    estado: Optional[str] = None,
    fecha_desde: Optional[str] = None,
    fecha_hasta: Optional[str] = None,
    inspector: Optional[int] = None,
    order_by: str = "inspeccionado_en",
    order_dir: str = "desc",
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Listar inspecciones con filtros y paginación
    
    - **Inspector**: Solo ve sus propias inspecciones
    - **Supervisor**: Ve todas las inspecciones de sus plantas asignadas
    - **Admin**: Ve todas las inspecciones
    
    - **q**: Búsqueda por número de contenedor o código
    - **planta**: Filtrar por ID de planta
    - **naviera**: Filtrar por ID de naviera
    - **estado**: Filtrar por estado (pending/approved/rejected)
    - **fecha_desde**: Fecha desde (YYYY-MM-DD)
    - **fecha_hasta**: Fecha hasta (YYYY-MM-DD)
    - **inspector**: Filtrar por ID de inspector (solo Admin/Supervisor)
    - **order_by**: Campo para ordenar (inspeccionado_en, numero_contenedor, estado)
    - **order_dir**: Dirección (asc/desc)
    """
    
    # Aplicar filtros según rol
    id_inspector = None
    if current_user.rol == 'inspector':
        # Inspector solo ve sus propias inspecciones
        id_inspector = current_user.id_usuario
    elif current_user.rol == 'supervisor':
        # Supervisor ve todas las inspecciones de sus plantas
        # TODO: Implementar lógica de plantas asignadas al supervisor
        # Por ahora, si especifica planta, solo ve esa planta
        # Permitir filtrar por inspector si se envía explícitamente
        if inspector:
            id_inspector = inspector
    else:
        # Admin: si se especifica inspector, aplicar filtro
        if inspector:
            id_inspector = inspector
    # Admin ve todo sin restricciones
    
    items, total, total_pages = inspeccion_service.listar_inspecciones(
        db=db,
        page=page,
        page_size=page_size,
        q=q,
        id_planta=planta,
        id_navieras=naviera,
        estado=estado,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        order_by=order_by,
        order_dir=order_dir,
        id_inspector=id_inspector
    )
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }


@router.get("/{id_inspeccion}", response_model=InspeccionDetalle)
def obtener_inspeccion(
    id_inspeccion: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener detalle completo de una inspección"""
    inspeccion = inspeccion_service.obtener_inspeccion(db, id_inspeccion)
    
    # Verificar permisos: Inspector solo ve sus propias inspecciones
    if current_user.rol == 'inspector' and inspeccion.id_inspector != current_user.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para ver esta inspección"
        )
    
    return inspeccion


@router.post("", response_model=InspeccionCreated, status_code=status.HTTP_201_CREATED)
def crear_inspeccion(
    inspeccion_data: InspeccionCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Crear nueva inspección (sin fotos)
    
    Retorna el ID y código para luego subir fotos con POST /inspecciones/{id}/fotos
    """
    # Si es inspector, forzar que el id_inspector sea el usuario actual
    if current_user.rol == 'inspector':
        inspeccion_data.id_inspector = current_user.id_usuario
    
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
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Actualizar campos de una inspección existente"""
    # Verificar permisos: Inspector solo actualiza sus propias inspecciones
    inspeccion = inspeccion_service.obtener_inspeccion(db, id_inspeccion)
    
    if current_user.rol == 'inspector':
        if inspeccion.id_inspector != current_user.id_usuario:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para editar esta inspección"
            )
        # Inspector no puede cambiar el estado
        if inspeccion_data.estado and inspeccion_data.estado != inspeccion.estado:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para cambiar el estado"
            )
    
    return inspeccion_service.actualizar_inspeccion(db, id_inspeccion, inspeccion_data)


@router.patch("/{id_inspeccion}/estado", response_model=InspeccionDetalle)
def cambiar_estado_inspeccion(
    id_inspeccion: int,
    estado_data: InspeccionEstadoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Cambiar estado de una inspección (aprobar/rechazar)
    
    Solo supervisor y admin pueden cambiar el estado.
    
    - **estado**: 'approved' o 'rejected'
    - **comentario**: Comentario opcional (requerido para rechazar)
    """
    # Solo supervisor y admin pueden cambiar estado
    if current_user.rol not in ['supervisor', 'admin']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para cambiar el estado de inspecciones"
        )
    
    # Verificar que existe la inspección
    inspeccion = inspeccion_service.obtener_inspeccion(db, id_inspeccion)
    
    # Validar que se proporcione comentario al rechazar
    if estado_data.estado == 'rejected' and not estado_data.comentario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe proporcionar un comentario al rechazar una inspección"
        )
    
    # Actualizar estado
    update_data = InspeccionUpdate(estado=estado_data.estado)
    if estado_data.comentario:
        # Agregar comentario a observaciones
        observaciones_actuales = inspeccion.observaciones or ""
        comentario_estado = f"\n\n--- {estado_data.estado.upper()} por {current_user.nombre} ---\n{estado_data.comentario}"
        update_data.observaciones = observaciones_actuales + comentario_estado
    
    return inspeccion_service.actualizar_inspeccion(db, id_inspeccion, update_data)


@router.delete("/{id_inspeccion}", response_model=Message)
def eliminar_inspeccion(
    id_inspeccion: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Eliminar inspección y todos sus archivos asociados"""
    # Solo admin y supervisor pueden eliminar
    if current_user.rol not in ['admin', 'supervisor']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para eliminar inspecciones"
        )
    
    inspeccion_service.eliminar_inspeccion(db, id_inspeccion)
    return {"mensaje": f"Inspección {id_inspeccion} eliminada exitosamente"}


@router.post("/{id_inspeccion}/fotos", response_model=List[FotoInspeccion])
async def subir_fotos(
    id_inspeccion: int,
    archivos: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Subir múltiples fotos para una inspección
    
    - Soporta múltiples archivos en una sola petición
    - Formatos: JPG, JPEG, PNG
    - Se guardan en capturas/inspecciones/{id_inspeccion}/
    """
    # Verificar permisos
    inspeccion = inspeccion_service.obtener_inspeccion(db, id_inspeccion)
    if current_user.rol == 'inspector' and inspeccion.id_inspector != current_user.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para subir fotos a esta inspección"
        )
    
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


@router.get("/export/csv")
def exportar_inspecciones_csv(
    q: Optional[str] = None,
    planta: Optional[int] = None,
    naviera: Optional[int] = None,
    estado: Optional[str] = None,
    fecha_desde: Optional[str] = None,
    fecha_hasta: Optional[str] = None,
    inspector: Optional[int] = None,
    order_by: str = "inspeccionado_en",
    order_dir: str = "desc",
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Exportar inspecciones a CSV con los mismos filtros que el listado
    
    - **Requiere rol**: Admin
    - Incluye: Fecha, Contenedor, Planta, Naviera, Inspector, Estado, ReportePDF
    - Usa los mismos filtros que el endpoint de listado
    """
    try:
        # Solo admin puede exportar
        if current_user.rol != 'admin':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo administradores pueden exportar inspecciones a CSV"
            )
        
        # Aplicar filtros según rol (mismo que listado pero sin paginación)
        id_inspector = None
        if inspector:
            id_inspector = inspector
        
    # Obtener todas las inspecciones sin paginación (límite razonable)
        items, total, _ = inspeccion_service.listar_inspecciones(
            db=db,
            page=1,
            page_size=10000,  # Límite alto para exportación
            q=q,
            id_planta=planta,
            id_navieras=naviera,
            estado=estado,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            order_by=order_by,
            order_dir=order_dir,
            id_inspector=id_inspector
        )
        
        # Crear CSV en memoria
        output = io.StringIO()
        # Escribir BOM para compatibilidad con Excel en Windows
        output.write('\ufeff')
        # Usar separador ';' común en configuraciones ES y CRLF para Excel
        writer = csv.writer(
            output,
            delimiter=';',
            lineterminator='\r\n',
            quoting=csv.QUOTE_ALL
        )

        # Encabezado de reporte (tipo informe)
        writer.writerow(["Reporte de Inspecciones"])
        writer.writerow([f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}"])
        try:
            writer.writerow([f"Usuario: {getattr(current_user, 'nombre', '')} ({getattr(current_user, 'correo', '')})"])
        except Exception:
            writer.writerow(["Usuario:"])

        # Línea de filtros aplicados
        filtros_aplicados = []
        if q:
            filtros_aplicados.append(f"Búsqueda: {q}")
        if planta:
            pl = planta_repository.get_by_id(db, int(planta))
            filtros_aplicados.append(f"Planta: {pl.nombre if pl else planta}")
        if naviera:
            nv = naviera_repository.get_by_id(db, int(naviera))
            filtros_aplicados.append(f"Naviera: {nv.nombre if nv else naviera}")
        if estado:
            estado_map = {
                'pending': 'Pendiente',
                'approved': 'Aprobada',
                'rejected': 'Rechazada'
            }
            filtros_aplicados.append(f"Estado: {estado_map.get(estado, estado)}")
        if fecha_desde:
            filtros_aplicados.append(f"Desde: {fecha_desde}")
        if fecha_hasta:
            filtros_aplicados.append(f"Hasta: {fecha_hasta}")
        if inspector:
            insp = usuario_repository.get_by_id(db, int(inspector))
            filtros_aplicados.append(f"Inspector: {insp.nombre if insp else inspector}")

        writer.writerow(["Filtros: " + (", ".join(filtros_aplicados) if filtros_aplicados else "Ninguno")])
        writer.writerow([])  # Línea en blanco

        # Cabeceras de tabla
        writer.writerow(['Fecha', 'Contenedor', 'Planta', 'Naviera', 'Inspector', 'Estado', 'ReportePDF'])
        
        # Estado en español
        estado_map = {
            'pending': 'Pendiente',
            'approved': 'Aprobada',
            'rejected': 'Rechazada'
        }
        
        # Datos - procesar cada inspección
        total_pend = total_apr = total_rech = 0
        for inspeccion in items:
            try:
                # Obtener detalle con relaciones cargadas
                detalle = inspeccion_service.obtener_inspeccion(db, inspeccion.id_inspeccion)
                
                # Formatear fecha
                fecha = detalle.inspeccionado_en.strftime('%d/%m/%Y %H:%M') if detalle.inspeccionado_en else ''
                
                estado_texto = estado_map.get(detalle.estado, detalle.estado)
                if detalle.estado == 'pending':
                    total_pend += 1
                elif detalle.estado == 'approved':
                    total_apr += 1
                elif detalle.estado == 'rejected':
                    total_rech += 1
                
                # URL del reporte PDF
                reporte_pdf = f"{settings.BACKEND_URL}/api/reportes/pdf/generar?id_inspeccion={detalle.id_inspeccion}"
                
                writer.writerow([
                    fecha,
                    detalle.numero_contenedor or '',
                    detalle.planta.nombre if hasattr(detalle, 'planta') and detalle.planta else '',
                    detalle.naviera.nombre if hasattr(detalle, 'naviera') and detalle.naviera else '',
                    detalle.inspector.nombre if hasattr(detalle, 'inspector') and detalle.inspector else '',
                    estado_texto,
                    reporte_pdf
                ])
            except Exception as e:
                # Si falla una inspección individual, continuar con las demás
                import logging
                logging.error(f"Error procesando inspección {inspeccion.id_inspeccion}: {e}")
                continue
        
        # Línea de totales
        writer.writerow([])
        writer.writerow(["Totales"])
        writer.writerow([f"Pendientes: {total_pend}"])
        writer.writerow([f"Aprobadas: {total_apr}"])
        writer.writerow([f"Rechazadas: {total_rech}"])
        writer.writerow([f"Total: {total}"])

        # Preparar respuesta
        output.seek(0)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"reporte_inspecciones_{timestamp}.csv"
        
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv; charset=utf-8",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error general en exportación CSV: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar el archivo CSV: {str(e)}"
        )
