"""Router de Auditoría: Cadena de Custodia de Inspecciones/Reportes"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from io import BytesIO
from datetime import datetime
from pathlib import Path
import os

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors

from ..core import get_db
from ..core.settings import settings
from ..models import Usuario
from ..repositories.reportes import reporte_repository
from ..repositories.inspecciones import inspeccion_repository, foto_repository
from ..utils.auth import get_current_user, require_roles
from ..utils.files import calculate_file_hash


router = APIRouter(prefix="/auditar", tags=["Auditar"])


@router.get("/cadena-custodia/{reporte_id}")
def descargar_cadena_custodia(
    reporte_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Genera y descarga el Informe de Cadena de Custodia (PDF) para un reporte.

    Requiere rol: admin
    """
    require_roles(current_user, ["admin"])  # Solo admin para MVP

    # Obtener reporte e inspección
    reporte = reporte_repository.get_by_id(db, reporte_id)
    if not reporte:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reporte no encontrado")

    inspeccion = inspeccion_repository.get_by_id(db, reporte.id_inspeccion)
    if not inspeccion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inspección asociada no encontrada")

    fotos = foto_repository.get_by_inspeccion(db, reporte.id_inspeccion)

    # Preparar buffer PDF en memoria
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50,
    )
    styles = getSampleStyleSheet()
    story = []

    # Encabezado
    titulo_style = ParagraphStyle(
        'Titulo', parent=styles['Heading1'], alignment=TA_CENTER, textColor=colors.HexColor('#1a5490')
    )
    story.append(Paragraph("Informe de Cadena de Custodia", titulo_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    story.append(Spacer(1, 18))

    # Identificación
    story.append(Paragraph("Identificación", styles['Heading2']))
    ident_data = [
        ["ID Reporte", str(reporte.id)],
        ["UUID Reporte", reporte.uuid_reporte or ""],
        ["ID Inspección", str(inspeccion.id_inspeccion)],
        ["Código Inspección", inspeccion.codigo],
        ["Contenedor", inspeccion.numero_contenedor],
        ["Planta", inspeccion.planta.nombre if inspeccion.planta else ""],
        ["Naviera", inspeccion.naviera.nombre if inspeccion.naviera else ""],
        ["Fecha Inspección", inspeccion.inspeccionado_en.strftime('%d/%m/%Y %H:%M')],
        ["Fecha Reporte", reporte.creado_en.strftime('%d/%m/%Y %H:%M')],
    ]
    t_ident = Table(ident_data, colWidths=[160, 360])
    t_ident.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#e8f4f8')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
    ]))
    story.append(t_ident)
    story.append(Spacer(1, 14))

    # Integridad
    story.append(Paragraph("Integridad", styles['Heading2']))
    plantilla_ver = "PDF Plantilla v1.0"
    integ_data = [
        ["Hash SHA-256 (reporte)", (reporte.hash_global or '').upper()],
        ["Versión de plantilla", plantilla_ver],
    ]
    t_integ = Table(integ_data, colWidths=[160, 360])
    t_integ.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f5f5f5')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
    ]))
    story.append(t_integ)
    story.append(Spacer(1, 14))

    # Evidencias
    story.append(Paragraph("Evidencias", styles['Heading2']))

    # Tabla de evidencias - encabezado
    ev_rows = [["ID", "Ruta", "SHA-256", "Tamaño", "Fecha", "Creado por"]]

    capturas_base = Path(os.path.abspath(settings.CAPTURAS_DIR))
    for foto in fotos:
        # Resolver path absoluto
        rel = foto.foto_path.replace("\\", "/")
        if rel.startswith("/capturas/"):
            rel_clean = rel[len("/capturas/"):]
            abs_path = capturas_base / rel_clean
        else:
            abs_path = capturas_base / rel
        size_str = ""
        try:
            if abs_path.exists():
                size_str = f"{abs_path.stat().st_size} B"
        except Exception:
            size_str = ""

        # Hash: usar el de BD si existe, si no calcular on-the-fly
        hash_hex = foto.hash_hex or ""
        if not hash_hex:
            try:
                with open(abs_path, 'rb') as f:
                    hash_hex = calculate_file_hash(f.read())
            except Exception:
                hash_hex = ""

        fecha_evi = foto.creado_en.strftime('%d/%m/%Y %H:%M') if foto.creado_en else (foto.tomada_en.strftime('%d/%m/%Y %H:%M') if foto.tomada_en else "")
        creado_por = inspeccion.inspector.nombre if inspeccion.inspector else ""
        ev_rows.append([str(foto.id_foto), rel, hash_hex, size_str, fecha_evi, creado_por])

    t_evi = Table(ev_rows, colWidths=[40, 180, 150, 70, 80, 100])
    t_evi.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_evi)
    story.append(Spacer(1, 14))

    # Eventos (bitácora derivada)
    story.append(Paragraph("Eventos", styles['Heading2']))
    eventos = []
    # Creación de inspección
    eventos.append(["CREACION", inspeccion.creado_en.strftime('%d/%m/%Y %H:%M'), inspeccion.inspector.nombre if inspeccion.inspector else "", "N/D"])
    # Altas de evidencias
    for foto in fotos:
        ts = foto.creado_en or foto.tomada_en
        eventos.append(["EVIDENCIA_ALTA", ts.strftime('%d/%m/%Y %H:%M') if ts else "", inspeccion.inspector.nombre if inspeccion.inspector else "", "N/D"])
    # Estado
    eventos.append([f"ESTADO: {inspeccion.estado.upper()}", inspeccion.actualizado_en.strftime('%d/%m/%Y %H:%M'), "Sistema", "N/D"])
    # Aprobación / Firma revisión (si aplica)
    if inspeccion.estado == 'approved':
        # Leer metadatos de firma de revisor si existen
        firma_meta = None
        firmas_dir = Path(os.path.abspath(settings.CAPTURAS_DIR)) / "firmas" / "revisiones"
        meta_path = firmas_dir / f"inspeccion_{inspeccion.id_inspeccion}_revisor.json"
        if meta_path.exists():
            try:
                import json
                firma_meta = json.loads(meta_path.read_text(encoding='utf-8'))
            except Exception:
                firma_meta = None
        if firma_meta:
            eventos.append(["APROBACION/FIRMA", firma_meta.get('firmado_en', ''), firma_meta.get('nombre', ''), "N/D"])
        else:
            eventos.append(["APROBACION", inspeccion.actualizado_en.strftime('%d/%m/%Y %H:%M'), "Supervisor/Admin", "N/D"])

    ev_rows = [["Evento", "Timestamp", "Usuario", "IP/UA"]] + eventos
    t_evt = Table(ev_rows, colWidths=[150, 120, 150, 100])
    t_evt.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_evt)
    story.append(Spacer(1, 14))

    # Estado/Bloqueo
    bloqueado = "Sí (evidencias bloqueadas)" if inspeccion.estado == 'approved' else "No"
    story.append(Paragraph("Estado", styles['Heading2']))
    t_estado = Table([["Inspección aprobada", "Sí" if inspeccion.estado == 'approved' else "No"], ["Bloqueo de evidencias", bloqueado]], colWidths=[200, 320])
    t_estado.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f5f5f5')),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
    ]))
    story.append(t_estado)

    # Construir PDF
    doc.build(story)
    buffer.seek(0)

    filename = f"cadena_custodia_{reporte.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    return StreamingResponse(buffer, media_type="application/pdf", headers={
        "Content-Disposition": f"attachment; filename={filename}"
    })
