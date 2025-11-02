"""Script de prueba para generación de PDF

Este script prueba la funcionalidad de generación de PDF sin necesidad del servidor web.
Útil para desarrollo y depuración.
"""
import sys
from pathlib import Path

# Agregar el directorio backend al path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.core.settings import settings
from app.services.pdf_generator import pdf_generator_service
from app.repositories.inspecciones import inspeccion_repository


def main():
    """Función principal de prueba"""
    
    # Crear engine
    engine = create_engine(settings.DATABASE_URL)
    
    with Session(engine) as db:
        # Listar inspecciones disponibles
        print("=" * 60)
        print("INSPECCIONES DISPONIBLES PARA GENERAR PDF")
        print("=" * 60)
        
        inspecciones, total = inspeccion_repository.get_all(db, skip=0, limit=10)
        
        if total == 0:
            print("No hay inspecciones en la base de datos.")
            return
        
        for insp in inspecciones:
            print(f"\nID: {insp.id_inspeccion}")
            print(f"Código: {insp.codigo}")
            print(f"Contenedor: {insp.numero_contenedor}")
            print(f"Planta: {insp.planta.nombre if insp.planta else 'N/A'}")
            print(f"Naviera: {insp.naviera.nombre if insp.naviera else 'N/A'}")
            print(f"Inspector: {insp.inspector.nombre if insp.inspector else 'N/A'}")
            print(f"Fotos: {len(insp.fotos)}")
            
            # Validar
            es_valida, mensaje = pdf_generator_service.validar_inspeccion_para_pdf(db, insp.id_inspeccion)
            if es_valida:
                print("✅ VÁLIDA para generar PDF")
            else:
                print(f"❌ NO VÁLIDA: {mensaje}")
        
        # Pedir ID para generar
        print("\n" + "=" * 60)
        id_inspeccion = input("\nIngrese ID de inspección para generar PDF (0 para salir): ")
        
        try:
            id_inspeccion = int(id_inspeccion)
            if id_inspeccion == 0:
                print("Saliendo...")
                return
        except ValueError:
            print("ID inválido")
            return
        
        # Validar antes de generar
        es_valida, mensaje = pdf_generator_service.validar_inspeccion_para_pdf(db, id_inspeccion)
        if not es_valida:
            print(f"\n❌ ERROR: {mensaje}")
            print("No se puede generar el PDF.")
            return
        
        # Generar PDF
        print(f"\n🔄 Generando PDF para inspección {id_inspeccion}...")
        
        try:
            reporte = pdf_generator_service.generar_pdf(db, id_inspeccion)
            
            print("\n✅ PDF GENERADO EXITOSAMENTE")
            print("=" * 60)
            print(f"ID Reporte: {reporte.id_reporte}")
            print(f"UUID: {reporte.uuid_reporte}")
            print(f"Ruta PDF: {reporte.pdf_ruta}")
            print(f"Hash: {reporte.hash_global}")
            print(f"Creado: {reporte.creado_en}")
            print("=" * 60)
            
            # Verificar que el archivo existe
            if Path(reporte.pdf_ruta).exists():
                size = Path(reporte.pdf_ruta).stat().st_size
                print(f"\n📄 Archivo creado: {size} bytes")
                print(f"Ubicación: {Path(reporte.pdf_ruta).absolute()}")
            else:
                print("\n⚠️ Advertencia: El archivo no se encontró en disco")
        
        except Exception as e:
            print(f"\n❌ ERROR al generar PDF: {str(e)}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
