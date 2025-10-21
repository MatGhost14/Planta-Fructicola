"""
Módulo de Configuración Central de la Aplicación
================================================
Este módulo maneja todas las variables de entorno y configuraciones globales
del sistema usando Pydantic Settings para validación automática.

Uso:
    from app.core.settings import settings
    
    database_url = settings.database_url
    origins = settings.cors_origins

Autor: Sistema de Inspección de Contenedores
Versión: 2.1.0
"""
import os
from typing import List
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Clase de configuración que carga variables desde .env
    
    Todas las propiedades se cargan automáticamente desde el archivo .env
    Si una variable no existe, se usa el valor por defecto.
    
    Attributes:
        APP_NAME: Nombre de la aplicación
        APP_VERSION: Versión actual del sistema
        DEBUG: Modo debug (True en desarrollo, False en producción)
        SECRET_KEY: Clave secreta para JWT (DEBE ser única en producción)
        DATABASE_URL: URL de conexión MySQL generada automáticamente
        ALLOWED_ORIGINS: Orígenes permitidos para CORS (separados por coma)
    """
    
    # ==========================================
    # INFORMACIÓN DE LA APLICACIÓN
    # ==========================================
    APP_NAME: str = "Sistema de Inspección de Contenedores"
    APP_VERSION: str = "2.1.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"  # development, staging, production
    
    # ==========================================
    # SEGURIDAD Y AUTENTICACIÓN JWT
    # ==========================================
    SECRET_KEY: str  # ⚠️ OBLIGATORIO - Generar una clave aleatoria segura
    ALGORITHM: str = "HS256"  # Algoritmo de encriptación JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480  # Duración del token (8 horas)
    
    # ==========================================
    # CONFIGURACIÓN DE BASE DE DATOS
    # ==========================================
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "inspeccioncontenedor"
    
    # Pool de conexiones para mejor rendimiento
    DB_POOL_SIZE: int = 10  # Conexiones simultáneas en el pool
    DB_MAX_OVERFLOW: int = 20  # Conexiones extra permitidas bajo carga
    
    # ==========================================
    # CORS (Cross-Origin Resource Sharing)
    # ==========================================
    ALLOWED_ORIGINS: str = "http://localhost:5173"  # Separar múltiples con coma
    
    # ==========================================
    # GESTIÓN DE ARCHIVOS
    # ==========================================
    CAPTURAS_DIR: str = "../capturas"  # Directorio de imágenes de inspecciones
    MAX_FILE_SIZE: int = 10485760  # Tamaño máximo de archivo: 10MB
    
    # ==========================================
    # CONFIGURACIÓN DEL SERVIDOR
    # ==========================================
    BACKEND_HOST: str = "0.0.0.0"  # 0.0.0.0 permite conexiones externas
    BACKEND_PORT: int = 8000
    
    # ==========================================
    # LOGGING
    # ==========================================
    LOG_LEVEL: str = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_FILE: str = "app.log"
    
    @property
    def database_url(self) -> str:
        """
        Genera la URL de conexión a MySQL
        
        Returns:
            str: URL en formato mysql+pymysql://user:pass@host:port/db
            
        Example:
            mysql+pymysql://root:password@localhost:3306/inspeccioncontenedor
        """
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def cors_origins(self) -> List[str]:
        """
        Convierte la cadena ALLOWED_ORIGINS en una lista
        
        Returns:
            List[str]: Lista de orígenes permitidos
            
        Example:
            Input: "http://localhost:5173,http://example.com"
            Output: ["http://localhost:5173", "http://example.com"]
        """
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    class Config:
        """Configuración de Pydantic Settings"""
        env_file = ".env"  # Archivo de variables de entorno
        env_file_encoding = "utf-8"  # Encoding del archivo
        case_sensitive = True  # Las variables son case-sensitive
        extra = "ignore"  # Ignorar variables extra no definidas


@lru_cache()
def get_settings() -> Settings:
    """
    Obtiene la instancia singleton de configuración
    
    Usa @lru_cache para que la configuración se cargue solo una vez
    en memoria, mejorando el rendimiento.
    
    Returns:
        Settings: Instancia única de configuración
        
    Example:
        from app.core.settings import get_settings
        
        settings = get_settings()
        print(settings.APP_VERSION)  # "2.1.0"
    """
    return Settings()


# ==========================================
# INSTANCIA GLOBAL DE CONFIGURACIÓN
# ==========================================
# Usar esta instancia en toda la aplicación
settings = get_settings()
