"""
Router para exportación de reportes en PDF y Excel
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date
from typing import Optional
import io

# Importaciones para PDF
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# Importaciones para Excel
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

from ..core.database import get_db
from ..models import Inspeccion, Planta, Naviera, Usuario
from ..utils.auth import get_current_active_user

router = APIRouter(tags=["Reportes Export"])


def crear_pdf_inspecciones(inspecciones: list, filtros: dict) -> io.BytesIO:
    """
    Genera un PDF con el reporte de inspecciones
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elementos = []
    
    # Estilos
    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1e3a8a'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    subtitulo_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.grey,
        alignment=TA_CENTER,
        spaceAfter=20
    )
    
    # Título
    elementos.append(Paragraph("Reporte de Inspecciones de Contenedores", titulo_style))
    
    # Información del reporte
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
    info_texto = f"Generado el: {fecha_actual}"
    
    if filtros.get('fecha_desde') and filtros.get('fecha_hasta'):
        info_texto += f"<br/>Período: {filtros['fecha_desde']} al {filtros['fecha_hasta']}"
    
    elementos.append(Paragraph(info_texto, subtitulo_style))
    elementos.append(Spacer(1, 0.3*inch))
    
    # Estadísticas resumen
    total = len(inspecciones)
    aprobadas = sum(1 for i in inspecciones if i.estado == 'approved')
    rechazadas = sum(1 for i in inspecciones if i.estado == 'rejected')
    pendientes = sum(1 for i in inspecciones if i.estado == 'pending')
    
    resumen_data = [
        ['RESUMEN GENERAL', '', '', ''],
        ['Total Inspecciones', 'Aprobadas', 'Rechazadas', 'Pendientes'],
        [str(total), str(aprobadas), str(rechazadas), str(pendientes)]
    ]
    
    resumen_table = Table(resumen_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    resumen_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#e5e7eb')),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 2), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
    ]))
    
    elementos.append(resumen_table)
    elementos.append(Spacer(1, 0.4*inch))
    
    # Tabla de inspecciones
    if inspecciones:
        elementos.append(Paragraph("DETALLE DE INSPECCIONES", titulo_style))
        elementos.append(Spacer(1, 0.2*inch))
        
        # Encabezados
        data = [['Código', 'Contenedor', 'Planta', 'Fecha', 'Estado', 'Inspector']]
        
        # Datos
        for insp in inspecciones[:100]:  # Limitar a 100 registros por página
            estado_texto = {
                'pending': 'Pendiente',
                'approved': 'Aprobado',
                'rejected': 'Rechazado'
            }.get(insp.estado, insp.estado)
            
            fecha = insp.inspeccionado_en.strftime("%d/%m/%Y") if insp.inspeccionado_en else 'N/A'
            planta_nombre = insp.planta.nombre if insp.planta else 'N/A'
            inspector_nombre = insp.inspector.nombre_completo if insp.inspector else 'N/A'
            
            data.append([
                insp.codigo[:15] if insp.codigo else 'N/A',
                insp.numero_contenedor[:12] if insp.numero_contenedor else 'N/A',
                planta_nombre[:20],
                fecha,
                estado_texto,
                inspector_nombre[:20]
            ])
        
        # Crear tabla
        col_widths = [1.2*inch, 1.2*inch, 1.5*inch, 0.9*inch, 0.9*inch, 1.5*inch]
        tabla = Table(data, colWidths=col_widths)
        
        # Estilo de la tabla
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elementos.append(tabla)
    
    # Construir PDF
    doc.build(elementos)
    buffer.seek(0)
    return buffer


def crear_excel_inspecciones(inspecciones: list, filtros: dict) -> io.BytesIO:
    """
    Genera un archivo Excel con el reporte de inspecciones
    """
    buffer = io.BytesIO()
    wb = Workbook()
    
    # Hoja de Resumen
    ws_resumen = wb.active
    ws_resumen.title = "Resumen"
    
    # Título
    ws_resumen['A1'] = 'REPORTE DE INSPECCIONES DE CONTENEDORES'
    ws_resumen['A1'].font = Font(size=16, bold=True, color='1e3a8a')
    ws_resumen['A1'].alignment = Alignment(horizontal='center')
    ws_resumen.merge_cells('A1:F1')
    
    # Información del reporte
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
    ws_resumen['A2'] = f'Generado el: {fecha_actual}'
    ws_resumen['A2'].alignment = Alignment(horizontal='center')
    ws_resumen.merge_cells('A2:F2')
    
    if filtros.get('fecha_desde') and filtros.get('fecha_hasta'):
        ws_resumen['A3'] = f"Período: {filtros['fecha_desde']} al {filtros['fecha_hasta']}"
        ws_resumen['A3'].alignment = Alignment(horizontal='center')
        ws_resumen.merge_cells('A3:F3')
    
    # Estadísticas
    row = 5
    ws_resumen[f'A{row}'] = 'ESTADÍSTICAS GENERALES'
    ws_resumen[f'A{row}'].font = Font(size=12, bold=True)
    ws_resumen.merge_cells(f'A{row}:D{row}')
    
    row += 1
    headers = ['Total Inspecciones', 'Aprobadas', 'Rechazadas', 'Pendientes']
    for col, header in enumerate(headers, 1):
        cell = ws_resumen.cell(row, col, header)
        cell.font = Font(bold=True)
        cell.fill = PatternFill(start_color='e5e7eb', end_color='e5e7eb', fill_type='solid')
        cell.alignment = Alignment(horizontal='center')
        cell.border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
    
    row += 1
    total = len(inspecciones)
    aprobadas = sum(1 for i in inspecciones if i.estado == 'approved')
    rechazadas = sum(1 for i in inspecciones if i.estado == 'rejected')
    pendientes = sum(1 for i in inspecciones if i.estado == 'pending')
    
    valores = [total, aprobadas, rechazadas, pendientes]
    for col, valor in enumerate(valores, 1):
        cell = ws_resumen.cell(row, col, valor)
        cell.alignment = Alignment(horizontal='center')
        cell.border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
    
    # Ajustar anchos de columna
    for col in range(1, 7):
        ws_resumen.column_dimensions[get_column_letter(col)].width = 20
    
    # Hoja de Detalle
    ws_detalle = wb.create_sheet(title="Detalle")
    
    # Encabezados
    encabezados = ['Código', 'N° Contenedor', 'Planta', 'Naviera', 'Fecha Inspección', 'Estado', 'Inspector', 'Observaciones']
    for col, header in enumerate(encabezados, 1):
        cell = ws_detalle.cell(1, col, header)
        cell.font = Font(bold=True, color='FFFFFF')
        cell.fill = PatternFill(start_color='1e3a8a', end_color='1e3a8a', fill_type='solid')
        cell.alignment = Alignment(horizontal='center')
        cell.border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
    
    # Datos
    for row_idx, insp in enumerate(inspecciones, 2):
        estado_texto = {
            'pending': 'Pendiente',
            'approved': 'Aprobado',
            'rejected': 'Rechazado'
        }.get(insp.estado, insp.estado)
        
        fecha = insp.inspeccionado_en.strftime("%d/%m/%Y") if insp.inspeccionado_en else 'N/A'
        planta_nombre = insp.planta.nombre if insp.planta else 'N/A'
        naviera_nombre = insp.naviera.nombre if insp.naviera else 'N/A'
        inspector_nombre = insp.inspector.nombre_completo if insp.inspector else 'N/A'
        
        datos = [
            insp.codigo or 'N/A',
            insp.numero_contenedor or 'N/A',
            planta_nombre,
            naviera_nombre,
            fecha,
            estado_texto,
            inspector_nombre,
            insp.observaciones[:50] if insp.observaciones else ''
        ]
        
        for col_idx, valor in enumerate(datos, 1):
            cell = ws_detalle.cell(row_idx, col_idx, valor)
            cell.alignment = Alignment(horizontal='left' if col_idx in [1, 2, 3, 4, 7, 8] else 'center')
            cell.border = Border(
                left=Side(style='thin'),
                right=Side(style='thin'),
                top=Side(style='thin'),
                bottom=Side(style='thin')
            )
            
            # Color según estado
            if col_idx == 6:  # Columna Estado
                if estado_texto == 'Aprobado':
                    cell.fill = PatternFill(start_color='d1fae5', end_color='d1fae5', fill_type='solid')
                    cell.font = Font(color='065f46', bold=True)
                elif estado_texto == 'Rechazado':
                    cell.fill = PatternFill(start_color='fee2e2', end_color='fee2e2', fill_type='solid')
                    cell.font = Font(color='991b1b', bold=True)
                elif estado_texto == 'Pendiente':
                    cell.fill = PatternFill(start_color='fef3c7', end_color='fef3c7', fill_type='solid')
                    cell.font = Font(color='92400e', bold=True)
    
    # Ajustar anchos de columna
    anchos = [15, 18, 25, 25, 18, 15, 25, 40]
    for col, ancho in enumerate(anchos, 1):
        ws_detalle.column_dimensions[get_column_letter(col)].width = ancho
    
    # Guardar
    wb.save(buffer)
    buffer.seek(0)
    return buffer


@router.get("/pdf")
async def exportar_pdf(
    fecha_desde: Optional[str] = Query(None, description="Fecha desde (YYYY-MM-DD)"),
    fecha_hasta: Optional[str] = Query(None, description="Fecha hasta (YYYY-MM-DD)"),
    estado: Optional[str] = Query(None, description="Estado: pending, approved, rejected"),
    id_planta: Optional[int] = Query(None, description="ID de la planta"),
    id_inspector: Optional[int] = Query(None, description="ID del inspector"),
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Genera un reporte en PDF con las inspecciones filtradas
    """
    try:
        # Construir query base (sin JOINs, usaremos las relaciones de SQLAlchemy)
        query = db.query(Inspeccion)
        
        # Filtrar por rol
        if current_user.rol == 'inspector':
            query = query.filter(Inspeccion.id_inspector == current_user.id_usuario)
        
        # Filtros adicionales
        if fecha_desde:
            try:
                fecha_desde_obj = datetime.strptime(fecha_desde, "%Y-%m-%d").date()
                query = query.filter(func.date(Inspeccion.inspeccionado_en) >= fecha_desde_obj)
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de fecha_desde inválido")
        
        if fecha_hasta:
            try:
                fecha_hasta_obj = datetime.strptime(fecha_hasta, "%Y-%m-%d").date()
                query = query.filter(func.date(Inspeccion.inspeccionado_en) <= fecha_hasta_obj)
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de fecha_hasta inválido")
        
        if estado:
            query = query.filter(Inspeccion.estado == estado)
        
        if id_planta:
            query = query.filter(Inspeccion.id_planta == id_planta)
        
        if id_inspector:
            query = query.filter(Inspeccion.id_inspector == id_inspector)
        
        # Ordenar y obtener resultados
        inspecciones = query.order_by(Inspeccion.inspeccionado_en.desc()).limit(1000).all()
        
        if not inspecciones:
            raise HTTPException(status_code=404, detail="No se encontraron inspecciones con los filtros aplicados")
        
        # Generar PDF
        filtros = {
            'fecha_desde': fecha_desde,
            'fecha_hasta': fecha_hasta,
            'estado': estado,
            'id_planta': id_planta,
            'id_inspector': id_inspector
        }
        
        pdf_buffer = crear_pdf_inspecciones(inspecciones, filtros)
        
        # Nombre del archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reporte_inspecciones_{timestamp}.pdf"
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando PDF: {str(e)}")


@router.get("/excel")
async def exportar_excel(
    fecha_desde: Optional[str] = Query(None, description="Fecha desde (YYYY-MM-DD)"),
    fecha_hasta: Optional[str] = Query(None, description="Fecha hasta (YYYY-MM-DD)"),
    estado: Optional[str] = Query(None, description="Estado: pending, approved, rejected"),
    id_planta: Optional[int] = Query(None, description="ID de la planta"),
    id_inspector: Optional[int] = Query(None, description="ID del inspector"),
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Genera un reporte en Excel con las inspecciones filtradas
    """
    try:
        # Construir query base (sin JOINs, usaremos las relaciones de SQLAlchemy)
        query = db.query(Inspeccion)
        
        # Filtrar por rol
        if current_user.rol == 'inspector':
            query = query.filter(Inspeccion.id_inspector == current_user.id_usuario)
        
        # Filtros adicionales
        if fecha_desde:
            try:
                fecha_desde_obj = datetime.strptime(fecha_desde, "%Y-%m-%d").date()
                query = query.filter(func.date(Inspeccion.inspeccionado_en) >= fecha_desde_obj)
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de fecha_desde inválido")
        
        if fecha_hasta:
            try:
                fecha_hasta_obj = datetime.strptime(fecha_hasta, "%Y-%m-%d").date()
                query = query.filter(func.date(Inspeccion.inspeccionado_en) <= fecha_hasta_obj)
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de fecha_hasta inválido")
        
        if estado:
            query = query.filter(Inspeccion.estado == estado)
        
        if id_planta:
            query = query.filter(Inspeccion.id_planta == id_planta)
        
        if id_inspector:
            query = query.filter(Inspeccion.id_inspector == id_inspector)
        
        # Ordenar y obtener resultados
        inspecciones = query.order_by(Inspeccion.inspeccionado_en.desc()).limit(5000).all()
        
        if not inspecciones:
            raise HTTPException(status_code=404, detail="No se encontraron inspecciones con los filtros aplicados")
        
        # Generar Excel
        filtros = {
            'fecha_desde': fecha_desde,
            'fecha_hasta': fecha_hasta,
            'estado': estado,
            'id_planta': id_planta,
            'id_inspector': id_inspector
        }
        
        excel_buffer = crear_excel_inspecciones(inspecciones, filtros)
        
        # Nombre del archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reporte_inspecciones_{timestamp}.xlsx"
        
        return StreamingResponse(
            excel_buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando Excel: {str(e)}")
