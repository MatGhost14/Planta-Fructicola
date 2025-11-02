"""002_add_reportes_table

Revision ID: 002_add_reportes_table
Revises: 001_add_firma_path_and_foto_path
Create Date: 2025-11-02

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '002_add_reportes_table'
down_revision = '001_add_firma_path_and_foto_path'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Crear tabla reportes para almacenar PDFs generados"""
    
    op.create_table(
        'reportes',
        sa.Column('id_reporte', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('uuid_reporte', sa.String(36), nullable=False),
        sa.Column('id_inspeccion', sa.BigInteger(), nullable=False),
        sa.Column('pdf_ruta', sa.String(255), nullable=False),
        sa.Column('hash_global', sa.String(64), nullable=True),
        sa.Column('creado_en', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id_reporte'),
        sa.ForeignKeyConstraint(
            ['id_inspeccion'],
            ['inspecciones.id_inspeccion'],
            name='fk_reportes_inspeccion',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci'
    )
    
    # Crear índices
    op.create_index('ix_reportes_uuid', 'reportes', ['uuid_reporte'], unique=True)
    op.create_index('ix_reportes_inspeccion', 'reportes', ['id_inspeccion'], unique=False)


def downgrade() -> None:
    """Eliminar tabla reportes"""
    
    op.drop_index('ix_reportes_inspeccion', table_name='reportes')
    op.drop_index('ix_reportes_uuid', table_name='reportes')
    op.drop_table('reportes')
