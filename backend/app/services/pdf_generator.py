"""Servicio para generación de PDFs de inspecciones"""
import os
import uuid
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional
from io import BytesIO

import qrcode
from sqlalchemy.orm import Session
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib import colors
from PIL import Image as PILImage

from ..models import Inspeccion, FotoInspeccion, Reporte
from ..repositories.inspecciones import inspeccion_repository, foto_repository
from ..repositories.reportes import reporte_repository


class PDFGeneratorService:
    """Servicio para generar PDFs de inspecciones"""
    
    def __init__(self):
        # Construir ruta absoluta: subir desde pdf_generator.py -> services -> app -> backend -> proyecto raíz
        # Path(__file__) = .../backend/app/services/pdf_generator.py
        # .parent.parent.parent.parent = .../Planta-Fructicola (raíz del proyecto)
        proyecto_root = Path(__file__).resolve().parent.parent.parent.parent
        self.capturas_base = proyecto_root / "capturas"
        self.pdf_storage_path = self.capturas_base / "reportes"
        self.pdf_storage_path.mkdir(parents=True, exist_ok=True)
    
    def validar_inspeccion_para_pdf(self, db: Session, id_inspeccion: int) -> tuple[bool, str]:
        """
        Valida que la inspección tenga los datos necesarios para generar PDF
        
        Returns:
            tuple: (es_valida, mensaje_error)
        """
        inspeccion = inspeccion_repository.get_by_id(db, id_inspeccion)
        
        if not inspeccion:
            return False, "Inspección no encontrada"
        
        # Validar campos obligatorios
        if not inspeccion.numero_contenedor:
            return False, "Número de contenedor es obligatorio"
        
        if not inspeccion.id_planta or not inspeccion.planta:
            return False, "Planta es obligatoria"
        
        if not inspeccion.id_navieras or not inspeccion.naviera:
            return False, "Naviera es obligatoria"
        
        if not inspeccion.inspeccionado_en:
            return False, "Fecha de inspección es obligatoria"
        
        if not inspeccion.id_inspector or not inspeccion.inspector:
            return False, "Inspector es obligatorio"
        
        # Validar que tenga al menos 1 evidencia
        fotos = foto_repository.get_by_inspeccion(db, id_inspeccion)
        if not fotos or len(fotos) == 0:
            return False, "La inspección debe tener al menos 1 evidencia fotográfica"
        
        return True, ""
    
    def generar_pdf(self, db: Session, id_inspeccion: int) -> Reporte:
        """
        Genera un PDF estándar para una inspección
        
        Args:
            db: Sesión de base de datos
            id_inspeccion: ID de la inspección
            
        Returns:
            Reporte: Objeto reporte creado con la ruta del PDF
            
        Raises:
            ValueError: Si la inspección no es válida para generar PDF
        """
        # Validar inspección
        es_valida, mensaje = self.validar_inspeccion_para_pdf(db, id_inspeccion)
        if not es_valida:
            raise ValueError(mensaje)
        
        # Antes de continuar, asegurar que la tabla "reportes" exista.
        # Esto evita errores en entornos donde la migración aún no fue aplicada.
        try:
            bind = db.get_bind()
            # Crear tabla si no existe (no afecta si ya existe)
            Reporte.__table__.create(bind=bind, checkfirst=True)
        except Exception:
            # En caso de fallo, continuamos y permitimos que el error sea manejado por la inserción
            pass

        # Obtener datos completos
        inspeccion = inspeccion_repository.get_by_id(db, id_inspeccion)
        fotos = foto_repository.get_by_inspeccion(db, id_inspeccion)
        
        # Generar UUID para el reporte
        uuid_reporte = str(uuid.uuid4())
        uuid_corto = uuid_reporte.split('-')[0]
        
        # Crear nombre de archivo
        fecha_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"reporte_{inspeccion.codigo}_{fecha_str}.pdf"
        pdf_path = self.pdf_storage_path / pdf_filename
        
        # Generar PDF (pasamos el uuid_reporte para el QR; el hash aún no está disponible)
        self._crear_pdf(inspeccion, fotos, pdf_path, uuid_corto, uuid_reporte=uuid_reporte)
        
        # Calcular hash del PDF
        hash_global = self._calcular_hash_pdf(pdf_path)
        
        # Guardar en BD
        reporte_data = {
            "uuid_reporte": uuid_reporte,
            "id_inspeccion": id_inspeccion,
            "pdf_ruta": str(pdf_path),
            "hash_global": hash_global
        }
        
        reporte = reporte_repository.create(db, reporte_data)
        
        return reporte
    
    def _crear_pdf(
        self,
        inspeccion: Inspeccion,
        fotos: list[FotoInspeccion],
        pdf_path: Path,
        uuid_corto: str,
        uuid_reporte: Optional[str] = None,
        hash_global: Optional[str] = None
    ) -> None:
        """Crea el archivo PDF con la estructura definida"""
        
        # Crear documento
        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Contenido
        story = []
        styles = getSampleStyleSheet()
        
        # Estilos personalizados
        titulo_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a5490'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        subtitulo_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=20
        )
        
        # === PORTADA ===
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph("REPORTE DE INSPECCIÓN", titulo_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Información del reporte
        info_reporte = [
            ["Reporte #:", uuid_corto],
            ["Inspección #:", inspeccion.codigo],
            ["Contenedor:", inspeccion.numero_contenedor],
            ["Planta:", inspeccion.planta.nombre if inspeccion.planta else "N/A"],
            ["Naviera:", inspeccion.naviera.nombre if inspeccion.naviera else "N/A"],
            ["Fecha Inspección:", inspeccion.inspeccionado_en.strftime("%d/%m/%Y %H:%M")],
            ["Inspector:", inspeccion.inspector.nombre if inspeccion.inspector else "N/A"],
            ["Estado:", inspeccion.estado.upper()]
        ]
        
        tabla_info = Table(info_reporte, colWidths=[2*inch, 4*inch])
        tabla_info.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4f8')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(tabla_info)
        story.append(Spacer(1, 0.3*inch))
        
        # === RESUMEN CHECKLIST ===
        story.append(Paragraph("Resumen de Inspección", subtitulo_style))
        
        # Determinar resultado del checklist
        if inspeccion.temperatura_c is not None:
            temp_text = f"{inspeccion.temperatura_c}°C"
            temp_status = "OK" if -25 <= inspeccion.temperatura_c <= 5 else "OBSERVACIÓN"
        else:
            temp_text = "NO MEDIDA"
            temp_status = "NO APLICA"
        
        checklist_data = [
            ["Item", "Estado", "Detalle"],
            ["Contenedor", "OK", inspeccion.numero_contenedor],
            ["Temperatura", temp_status, temp_text],
            ["Evidencias", "OK", f"{len(fotos)} fotos registradas"],
            ["Observaciones", "OK" if not inspeccion.observaciones else "CON NOTAS",
             inspeccion.observaciones[:50] + "..." if inspeccion.observaciones and len(inspeccion.observaciones) > 50 else inspeccion.observaciones or "Ninguna"]
        ]
        
        tabla_checklist = Table(checklist_data, colWidths=[2*inch, 1.5*inch, 3*inch])
        tabla_checklist.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
        ]))
        
        story.append(tabla_checklist)
        
        # Observaciones completas si existen
        if inspeccion.observaciones:
            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph("<b>Observaciones Completas:</b>", styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
            obs_style = ParagraphStyle(
                'Observaciones',
                parent=styles['Normal'],
                fontSize=10,
                leftIndent=20,
                spaceBefore=6,
                spaceAfter=6
            )
            story.append(Paragraph(inspeccion.observaciones, obs_style))
        
        story.append(PageBreak())
        
        # === EVIDENCIAS FOTOGRÁFICAS ===
        story.append(Paragraph("Evidencias Fotográficas", subtitulo_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Organizar fotos en cuadrícula (2x3 = 6 por página)
        thumbnails_per_page = 6
        cols = 2
        thumbnail_size = 2.5 * inch
        
        for i in range(0, len(fotos), thumbnails_per_page):
            batch = fotos[i:i+thumbnails_per_page]
            foto_rows = []
            
            for j in range(0, len(batch), cols):
                row = []
                for k in range(cols):
                    if j + k < len(batch):
                        foto = batch[j + k]
                        cell_content = self._crear_celda_foto(foto, thumbnail_size)
                        row.append(cell_content)
                    else:
                        row.append("")  # Celda vacía
                
                foto_rows.append(row)
            
            if foto_rows:
                tabla_fotos = Table(foto_rows, colWidths=[3.25*inch, 3.25*inch])
                tabla_fotos.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 10),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                    ('TOPPADDING', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ]))
                
                story.append(tabla_fotos)
                story.append(Spacer(1, 0.2*inch))
            
            # Nueva página si hay más fotos
            if i + thumbnails_per_page < len(fotos):
                story.append(PageBreak())
        
        # === INTEGRIDAD ===
        story.append(PageBreak())
        story.append(Paragraph("Integridad del Documento", subtitulo_style))
        story.append(Spacer(1, 0.1*inch))
        
        # Texto informativo
        info_text = """
        Este reporte ha sido generado automáticamente por el sistema de inspección.
        La integridad del documento está garantizada mediante:
        <br/><br/>
        <b>1. Hash Criptográfico SHA-256:</b> Huella digital única del documento.
        <br/>
        <b>2. Código QR:</b> Permite verificación rápida mediante dispositivos móviles.
        """
        story.append(Paragraph(info_text, styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Mostrar QR si hay uuid disponible; mostrar hash si está disponible
        if uuid_reporte:
            integridad_data = []
            integridad_data.append([
                Paragraph("<b>Hash SHA-256</b>", styles['Normal']),
                Paragraph("<b>Código QR de Verificación</b>", styles['Normal'])
            ])
            
            # Hash (si está disponible) o placeholder
            if hash_global:
                hash_formateado = '<br/>'.join([hash_global[i:i+32] for i in range(0, len(hash_global), 32)])
                hash_paragraph = Paragraph(
                    f'<font name="Courier" size="8">{hash_formateado}</font>',
                    styles['Normal']
                )
            else:
                hash_paragraph = Paragraph(
                    '<i>Se registrará al finalizar la generación.</i>',
                    styles['Normal']
                )
            
            # QR con el UUID
            qr_data = f"REPORTE:{uuid_reporte}"
            qr_image = self._generar_qr(qr_data, size=2)
            integridad_data.append([hash_paragraph, qr_image])
            
            tabla_integridad = Table(integridad_data, colWidths=[4*inch, 2.5*inch])
            tabla_integridad.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('ALIGN', (0, 1), (0, 1), 'LEFT'),
                ('ALIGN', (1, 1), (1, 1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ]))
            story.append(tabla_integridad)
            story.append(Spacer(1, 0.2*inch))
            
            nota_verificacion = Paragraph(
                '<b>Nota:</b> Escanee el código QR para verificar la autenticidad del documento. '
                'El hash oficial se valida contra el registro en el sistema.',
                ParagraphStyle('Nota', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor('#7f8c8d'))
            )
            story.append(nota_verificacion)
        else:
            mensaje_alt = Paragraph(
                '<i>Los datos de integridad (hash y QR) se generarán al finalizar el documento.</i>',
                styles['Normal']
            )
            story.append(mensaje_alt)
        
        # Generar PDF
        doc.build(story)
    
    def _crear_celda_foto(self, foto: FotoInspeccion, size: float) -> list:
        """Crea una celda con la foto y sus metadatos"""
        elementos = []
        styles = getSampleStyleSheet()
        
        # Construir ruta completa de la imagen
        # Las rutas en BD son relativas (ej: inspecciones/28-10-2025/8/foto_1.jpg)
        # Necesitamos construir ruta absoluta: self.capturas_base / foto.foto_path
        foto_path = self.capturas_base / foto.foto_path if not Path(foto.foto_path).is_absolute() else Path(foto.foto_path)
        
        if foto_path.exists():
            try:
                # Abrir con PIL para redimensionar manteniendo aspecto
                img_pil = PILImage.open(foto_path)
                
                # Obtener dimensiones originales
                original_width, original_height = img_pil.size
                
                # Calcular nuevo tamaño manteniendo aspecto
                aspect_ratio = original_width / original_height
                if aspect_ratio > 1:  # Imagen horizontal
                    new_width = int(size)
                    new_height = int(size / aspect_ratio)
                else:  # Imagen vertical o cuadrada
                    new_height = int(size)
                    new_width = int(size * aspect_ratio)
                
                # Redimensionar
                img_pil = img_pil.resize((new_width, new_height), PILImage.Resampling.LANCZOS)
                
                # Crear imagen temporal en memoria
                img_buffer = BytesIO()
                img_pil.save(img_buffer, format='JPEG', quality=85)
                img_buffer.seek(0)
                
                # Crear imagen para ReportLab
                img = Image(img_buffer, width=new_width, height=new_height)
                elementos.append(img)
                
            except Exception as e:
                # Si falla, mostrar placeholder con el error
                elementos.append(Paragraph(f"[Imagen no disponible: {str(e)}]", styles['Normal']))
        else:
            elementos.append(Paragraph(f"[Imagen no encontrada: {foto_path}]", styles['Normal']))
        
        # Metadatos
        meta_style = ParagraphStyle(
            'Meta',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#555555')
        )
        
        fecha_str = foto.tomada_en.strftime("%d/%m/%Y %H:%M") if foto.tomada_en else "N/A"
        meta_text = f"<b>ID:</b> {foto.id_foto} | <b>Fecha:</b> {fecha_str}"
        elementos.append(Spacer(1, 0.05*inch))
        elementos.append(Paragraph(meta_text, meta_style))
        
        return elementos
    
    def _calcular_hash_pdf(self, pdf_path: Path) -> str:
        """Calcula el hash SHA-256 del archivo PDF"""
        sha256 = hashlib.sha256()
        
        with open(pdf_path, 'rb') as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        
        return sha256.hexdigest()

    def _generar_qr(self, data: str, size: float = 2) -> Image:
            """
            Genera un código QR como imagen para ReportLab
        
            Args:
                data: Datos a codificar en el QR
                size: Tamaño del QR en pulgadas
            
            Returns:
                Image: Objeto Image de ReportLab con el QR
            """
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=2,
            )
            qr.add_data(data)
            qr.make(fit=True)
        
            qr_img = qr.make_image(fill_color="black", back_color="white")
        
            # Guardar en buffer
            img_buffer = BytesIO()
            qr_img.save(img_buffer, format='PNG')
            img_buffer.seek(0)
        
            # Convertir a ReportLab Image
            return Image(img_buffer, width=size*inch, height=size*inch)
    
    def obtener_reporte(self, db: Session, id_reporte: int) -> Optional[Reporte]:
        """Obtiene un reporte por ID"""
        return reporte_repository.get_by_id(db, id_reporte)
    
    def obtener_reporte_por_uuid(self, db: Session, uuid_reporte: str) -> Optional[Reporte]:
        """Obtiene un reporte por UUID"""
        return reporte_repository.get_by_uuid(db, uuid_reporte)
    
    def listar_reportes_inspeccion(self, db: Session, id_inspeccion: int) -> list[Reporte]:
        """Lista todos los reportes de una inspección"""
        return reporte_repository.get_by_inspeccion(db, id_inspeccion)


pdf_generator_service = PDFGeneratorService()
