"""
Sistema de logging centralizado
Configuración de logs estructurados para la aplicación
"""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime
from .settings import settings


def setup_logging():
    """
    Configura el sistema de logging de la aplicación
    - Logs en consola (desarrollo)
    - Logs en archivo con rotación (producción)
    - Formato estructurado con timestamp
    """
    
    # Crear directorio de logs si no existe
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configurar nivel de logging
    log_level = getattr(logging, settings.LOG_LEVEL, logging.INFO)
    
    # Formato de logs
    log_format = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Logger raíz
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Handler para consola (siempre activo)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(log_format)
    root_logger.addHandler(console_handler)
    
    # Handler para archivo con rotación (10MB, 5 backups)
    file_handler = RotatingFileHandler(
        filename=log_dir / settings.LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(log_format)
    root_logger.addHandler(file_handler)
    
    # Reducir verbosidad de librerías externas
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """Obtiene un logger con el nombre especificado"""
    return logging.getLogger(name)


# Logger para eventos de seguridad
security_logger = logging.getLogger("security")

# Logger para auditoría
audit_logger = logging.getLogger("audit")

# Logger para operaciones de base de datos
db_logger = logging.getLogger("database")
