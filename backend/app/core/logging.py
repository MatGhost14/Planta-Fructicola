"""
Sistema de Logging Centralizado
================================
Configura el sistema de logs estructurados con rotación automática
para toda la aplicación.

Características:
- Logs en consola (desarrollo) y archivo (producción)
- Rotación automática cada 10MB (mantiene 5 backups)
- Formato estructurado con timestamp, módulo, función y línea
- Loggers especializados: security, audit, database

Uso:
    from app.core.logging import setup_logging, get_logger
    
    setup_logging()  # Llamar al inicio de la app
    logger = get_logger(__name__)
    logger.info("Mensaje de log")

Autor: Sistema de Inspección de Contenedores
Versión: 2.1.0
"""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime
from .settings import settings


def setup_logging():
    """
    Configura el sistema de logging completo de la aplicación
    
    Crea dos handlers:
    1. ConsoleHandler: Imprime logs en terminal (útil en desarrollo)
    2. RotatingFileHandler: Guarda logs en archivo con rotación automática
    
    Rotación de archivos:
    - Cuando app.log alcanza 10MB, se renombra a app.log.1
    - Los archivos antiguos se numeran: app.log.1, app.log.2, ...
    - Se mantienen máximo 5 archivos históricos
    - Los más antiguos se eliminan automáticamente
    
    Formato de log:
        2025-10-14 23:45:12 - app.main - INFO - startup:45 - Aplicación iniciada
        [timestamp] - [módulo] - [nivel] - [función:línea] - [mensaje]
    
    Returns:
        logging.Logger: Logger raíz configurado
        
    Example:
        logger = setup_logging()
        logger.info("Sistema iniciado correctamente")
    """
    
    # ==========================================
    # 1. CREAR DIRECTORIO DE LOGS
    # ==========================================
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)  # Crea si no existe
    
    # ==========================================
    # 2. CONFIGURAR NIVEL DE LOGGING
    # ==========================================
    # Convierte string ("INFO", "DEBUG") a constante de logging
    log_level = getattr(logging, settings.LOG_LEVEL, logging.INFO)
    
    # ==========================================
    # 3. DEFINIR FORMATO DE LOGS
    # ==========================================
    log_format = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # ==========================================
    # 4. CONFIGURAR LOGGER RAÍZ
    # ==========================================
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Limpiar handlers existentes (evita duplicados)
    root_logger.handlers.clear()
    
    # ==========================================
    # 5. HANDLER PARA CONSOLA (STDOUT)
    # ==========================================
    # Imprime logs en la terminal - útil durante desarrollo
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(log_format)
    root_logger.addHandler(console_handler)
    
    # ==========================================
    # 6. HANDLER PARA ARCHIVO CON ROTACIÓN
    # ==========================================
    # Guarda logs en archivo con rotación automática
    file_handler = RotatingFileHandler(
        filename=log_dir / settings.LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10MB - Tamaño máximo antes de rotar
        backupCount=5,  # Mantener 5 archivos históricos
        encoding='utf-8'  # Soporte para caracteres especiales
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(log_format)
    root_logger.addHandler(file_handler)
    
    # ==========================================
    # 7. REDUCIR VERBOSIDAD DE LIBRERÍAS EXTERNAS
    # ==========================================
    # Evita spam de logs de uvicorn y sqlalchemy
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)
    
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Obtiene un logger con nombre específico para un módulo
    
    Permite identificar de qué parte del código proviene cada log.
    
    Args:
        name: Nombre del logger (usar __name__ para obtener el módulo actual)
        
    Returns:
        logging.Logger: Logger configurado
        
    Example:
        # En un archivo app/routers/auth.py
        logger = get_logger(__name__)  # Crea logger "app.routers.auth"
        logger.info("Usuario autenticado")
        
        # Output: 2025-10-14 23:45:12 - app.routers.auth - INFO - ...
    """
    return logging.getLogger(name)


# ==========================================
# LOGGERS ESPECIALIZADOS
# ==========================================
# Estos loggers se usan para categorizar eventos específicos

# Logger para eventos de seguridad (login, accesos no autorizados)
security_logger = logging.getLogger("security")

# Logger para auditoría (cambios importantes, acciones administrativas)
audit_logger = logging.getLogger("audit")

# Logger para operaciones de base de datos (queries lentas, errores DB)
db_logger = logging.getLogger("database")
