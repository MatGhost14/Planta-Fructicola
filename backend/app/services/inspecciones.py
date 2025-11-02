"""Servicio para inspecciones"""
import os
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
from typing import List, Optional, Tuple

from ..repositories import inspeccion_repository, foto_repository
from .notification_manager import notification_manager
from ..schemas import InspeccionCreate, InspeccionUpdate
from ..models import Inspeccion, FotoInspeccion
from ..utils import save_upload_file, delete_file_safe, get_mime_type
from ..core.settings import settings


class InspeccionService:
    """Servicio de lógica de negocio para inspecciones"""
    
    def generar_codigo(self) -> str:
        """Genera código único para inspección"""
        timestamp = int(datetime.now().timestamp() * 1000)
        return f"INS_{timestamp}"
    
    def crear_inspeccion(
        self,
        db: Session,
        inspeccion_data: InspeccionCreate
    ) -> Inspeccion:
        """Crea una nueva inspección"""
        # Generar código único
        codigo = self.generar_codigo()
        
        # Preparar datos
        data_dict = inspeccion_data.model_dump()
        data_dict["codigo"] = codigo
        
        # Si no se proporciona fecha, usar actual
        if not data_dict.get("inspeccionado_en"):
            data_dict["inspeccionado_en"] = datetime.now()
        
        created = inspeccion_repository.create(db, data_dict)

        # Si la inspección quedó en estado 'pending', emitir notificación a revisores/admins (MVP sin DB)
        try:
            estado = getattr(created, "estado", None)
            if estado == "pending":
                title = "Inspección en revisión"
                message = f"La inspección {created.codigo} ha sido creada y está pendiente de revisión."
                notification_manager.create(
                    recipients=[{"role": "supervisor"}, {"role": "admin"}],
                    title=title,
                    message=message,
                    link=f"/inspecciones/{created.id_inspeccion}",
                    payload={"id_inspeccion": created.id_inspeccion, "codigo": created.codigo},
                    event="INSPECCION_EN_REVISION"
                )
        except Exception:
            import logging
            logging.getLogger("inspecciones").exception("Error emitiendo notificación de nueva inspección")

        return created
    
    def listar_inspecciones(
        self,
        db: Session,
        page: int = 1,
        page_size: int = 20,
        q: Optional[str] = None,
        id_planta: Optional[int] = None,
        estado: Optional[str] = None,
        fecha_desde: Optional[str] = None,
        fecha_hasta: Optional[str] = None,
        order_by: str = "inspeccionado_en",
        order_dir: str = "desc",
        id_inspector: Optional[int] = None
    ) -> Tuple[List[Inspeccion], int, int]:
        """Lista inspecciones con filtros y paginación"""
        skip = (page - 1) * page_size
        
        # Convertir fechas
        fecha_desde_dt = None
        fecha_hasta_dt = None
        if fecha_desde:
            try:
                fecha_desde_dt = datetime.fromisoformat(fecha_desde)
            except:
                pass
        if fecha_hasta:
            try:
                fecha_hasta_dt = datetime.fromisoformat(fecha_hasta)
            except:
                pass
        
        items, total = inspeccion_repository.get_all(
            db=db,
            skip=skip,
            limit=page_size,
            q=q,
            id_planta=id_planta,
            estado=estado,
            fecha_desde=fecha_desde_dt,
            fecha_hasta=fecha_hasta_dt,
            order_by=order_by,
            order_dir=order_dir,
            id_inspector=id_inspector
        )
        
        total_pages = (total + page_size - 1) // page_size
        
        return items, total, total_pages
    
    def obtener_inspeccion(self, db: Session, id_inspeccion: int) -> Inspeccion:
        """Obtiene una inspección por ID"""
        inspeccion = inspeccion_repository.get_by_id(db, id_inspeccion)
        if not inspeccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Inspección {id_inspeccion} no encontrada"
            )
        return inspeccion
    
    def actualizar_inspeccion(
        self,
        db: Session,
        id_inspeccion: int,
        inspeccion_data: InspeccionUpdate
    ) -> Inspeccion:
        """Actualiza una inspección"""
        inspeccion = self.obtener_inspeccion(db, id_inspeccion)
        update_dict = inspeccion_data.model_dump(exclude_unset=True)

        # Detectar cambio de estado para emitir notificaciones (MVP sin DB)
        old_estado = getattr(inspeccion, "estado", None)
        new_estado = update_dict.get("estado", old_estado)

        updated = inspeccion_repository.update(db, inspeccion, update_dict)

        # Normalizar eventos: 'pending' -> INSPECCION_EN_REVISION, 'rejected' -> INSPECCION_RECHAZADA
        try:
            if old_estado != new_estado:
                if new_estado == "pending":
                    # Notificar a supervisores y admins que hay una inspección en revisión
                    title = "Inspección en revisión"
                    message = f"La inspección {updated.codigo} ha sido enviada para revisión."
                    notification_manager.create(
                        recipients=[{"role": "supervisor"}, {"role": "admin"}],
                        title=title,
                        message=message,
                        link=f"/inspecciones/{updated.id_inspeccion}",
                        payload={"id_inspeccion": updated.id_inspeccion, "codigo": updated.codigo},
                        event="INSPECCION_EN_REVISION"
                    )
                elif new_estado == "rejected":
                    # Notificar al inspector que su inspección fue rechazada
                    title = "Inspección rechazada"
                    message = f"La inspección {updated.codigo} ha sido rechazada. Revise las observaciones."
                    notification_manager.create(
                        recipients=[{"user_id": updated.id_inspector}],
                        title=title,
                        message=message,
                        link=f"/inspecciones/{updated.id_inspeccion}",
                        payload={"id_inspeccion": updated.id_inspeccion, "codigo": updated.codigo},
                        event="INSPECCION_RECHAZADA"
                    )
        except Exception:
            # No interrumpir la operación si la notificación falla
            import logging
            logging.getLogger("inspecciones").exception("Error emitiendo notificación de estado")

        return updated
    
    def eliminar_inspeccion(self, db: Session, id_inspeccion: int) -> None:
        """Elimina una inspección y sus archivos asociados"""
        inspeccion = self.obtener_inspeccion(db, id_inspeccion)
        
        # Eliminar fotos físicas
        for foto in inspeccion.fotos:
            # Convertir ruta relativa a absoluta
            foto_path = foto.foto_path.replace("/capturas/", "")
            full_path = os.path.join(settings.CAPTURAS_DIR, foto_path)
            delete_file_safe(full_path)
        
        # Eliminar firma física
        if inspeccion.firma_path:
            firma_path = inspeccion.firma_path.replace("/capturas/", "")
            full_path = os.path.join(settings.CAPTURAS_DIR, firma_path)
            delete_file_safe(full_path)
        
        # Intentar eliminar directorio de la inspección (puede estar en cualquier fecha)
        # La estructura es: capturas/inspecciones/dd-mm-yyyy/id_inspeccion/
        insp_dir_base = os.path.join(settings.CAPTURAS_DIR, "inspecciones")
        try:
            # Buscar en todos los subdirectorios de fecha
            if os.path.exists(insp_dir_base):
                for fecha_dir in os.listdir(insp_dir_base):
                    dir_path = os.path.join(insp_dir_base, fecha_dir, str(id_inspeccion))
                    if os.path.exists(dir_path):
                        # Eliminar archivos dentro del directorio
                        for file in os.listdir(dir_path):
                            file_path = os.path.join(dir_path, file)
                            delete_file_safe(file_path)
                        # Eliminar directorio vacío
                        os.rmdir(dir_path)
        except Exception as e:
            print(f"Error al eliminar directorio de inspección: {e}")
        
        # Eliminar de BD
        inspeccion_repository.delete(db, inspeccion)
    
    async def subir_fotos(
        self,
        db: Session,
        id_inspeccion: int,
        archivos: List[UploadFile]
    ) -> List[FotoInspeccion]:
        """Sube múltiples fotos para una inspección"""
        inspeccion = self.obtener_inspeccion(db, id_inspeccion)
        
        # Validar que la inspección no esté aprobada
        if inspeccion.estado == 'approved':
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="La evidencia es inmutable (inspección aprobada)"
            )
        
        # Obtener fecha actual en formato dd-mm-yyyy
        fecha_carpeta = datetime.now().strftime("%d-%m-%Y")
        
        # Directorio destino organizado por fecha
        dest_dir = os.path.join(
            settings.CAPTURAS_DIR,
            "inspecciones",
            fecha_carpeta,
            str(id_inspeccion)
        )
        
        fotos_creadas = []
        orden_actual = len(inspeccion.fotos)
        
        for idx, archivo in enumerate(archivos):
            # Guardar archivo
            full_path, relative_path, file_hash = await save_upload_file(
                archivo,
                dest_dir
            )
            
            # Crear registro en BD
            foto_data = {
                "id_inspeccion": id_inspeccion,
                "foto_path": relative_path,
                "mime_type": get_mime_type(archivo.filename),
                "hash_hex": file_hash,
                "orden": orden_actual + idx,
                "tomada_en": datetime.now()
            }
            
            foto = foto_repository.create(db, foto_data)
            fotos_creadas.append(foto)
        
        return fotos_creadas
    
    def eliminar_foto(
        self,
        db: Session,
        id_inspeccion: int,
        id_foto: int
    ) -> None:
        """Elimina una foto específica"""
        # Verificar que la inspección existe
        inspeccion = self.obtener_inspeccion(db, id_inspeccion)
        
        # Validar que la inspección no esté aprobada
        if inspeccion.estado == 'approved':
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="La evidencia es inmutable (inspección aprobada)"
            )
        
        # Obtener foto
        foto = foto_repository.get_by_id(db, id_foto)
        if not foto or foto.id_inspeccion != id_inspeccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Foto no encontrada"
            )
        
        # Eliminar archivo físico
        foto_path = foto.foto_path.replace("/capturas/", "")
        full_path = os.path.join(settings.CAPTURAS_DIR, foto_path)
        delete_file_safe(full_path)
        
        # Eliminar de BD
        foto_repository.delete(db, foto)
    
    async def subir_firma(
        self,
        db: Session,
        id_inspeccion: int,
        archivo: UploadFile
    ) -> Inspeccion:
        """Sube firma para una inspección"""
        inspeccion = self.obtener_inspeccion(db, id_inspeccion)
        
        # Si ya existe firma, eliminar anterior
        if inspeccion.firma_path:
            old_firma = inspeccion.firma_path.replace("/capturas/", "")
            old_path = os.path.join(settings.CAPTURAS_DIR, old_firma)
            delete_file_safe(old_path)
        
        # Directorio destino
        dest_dir = os.path.join(settings.CAPTURAS_DIR, "firmas")
        
        # Nombre único para firma
        extension = os.path.splitext(archivo.filename)[1]
        filename = f"{id_inspeccion}_{int(datetime.now().timestamp())}{extension}"
        
        # Guardar archivo
        full_path, relative_path, _ = await save_upload_file(
            archivo,
            dest_dir,
            filename
        )
        
        # Actualizar BD
        return inspeccion_repository.update_firma_path(db, inspeccion, relative_path)


inspeccion_service = InspeccionService()
