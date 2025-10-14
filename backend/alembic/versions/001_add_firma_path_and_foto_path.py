"""add_firma_path_and_foto_path

Revision ID: 001
Revises: 
Create Date: 2024-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Modificar tabla inspecciones
    # Eliminar firma_blob si existe
    op.execute("""
        ALTER TABLE inspecciones 
        DROP COLUMN IF EXISTS firma_blob
    """)
    
    # Agregar columna firma_path si no existe
    op.execute("""
        ALTER TABLE inspecciones 
        ADD COLUMN IF NOT EXISTS firma_path VARCHAR(255) NULL 
        AFTER observaciones
    """)
    
    # 2. Modificar tabla fotos_inspeccion
    # Eliminar foto_blob si existe
    op.execute("""
        ALTER TABLE fotos_inspeccion 
        DROP COLUMN IF EXISTS foto_blob
    """)
    
    # Agregar foto_path si no existe
    op.execute("""
        ALTER TABLE fotos_inspeccion 
        ADD COLUMN IF NOT EXISTS foto_path VARCHAR(255) NOT NULL 
        AFTER id_inspeccion
    """)


def downgrade() -> None:
    # Revertir cambios
    op.execute("""
        ALTER TABLE inspecciones 
        DROP COLUMN IF EXISTS firma_path
    """)
    
    # Nota: Agregamos firma_blob de vuelta como LONGBLOB
    op.execute("""
        ALTER TABLE inspecciones 
        ADD COLUMN IF NOT EXISTS firma_blob LONGBLOB NULL 
        AFTER observaciones
    """)
    
    op.execute("""
        ALTER TABLE fotos_inspeccion 
        DROP COLUMN IF EXISTS foto_path
    """)
    
    # Nota: Agregamos foto_blob de vuelta como LONGBLOB
    op.execute("""
        ALTER TABLE fotos_inspeccion 
        ADD COLUMN IF NOT EXISTS foto_blob LONGBLOB NOT NULL 
        AFTER id_inspeccion
    """)
