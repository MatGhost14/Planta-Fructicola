"""
Configuración central de la aplicación
Maneja variables de entorno y configuraciones globales
"""
import os
from typing import List
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuración de la aplicación desde variables de entorno"""
    
    # Información de la aplicación
    APP_NAME: str = "Sistema de Inspección de Contenedores"
    APP_VERSION: str = "2.1.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # Seguridad JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    
    # Base de datos
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "ImpeccionContenedor"
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:5173"
    
    # Archivos
    CAPTURAS_DIR: str = "../capturas"
    MAX_FILE_SIZE: int = 10485760  # 10MB
    
    # Servidor
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "app.log"
    
    @property
    def database_url(self) -> str:
        """Genera la URL de conexión a la base de datos"""
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def cors_origins(self) -> List[str]:
        """Convierte ALLOWED_ORIGINS en lista"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # Ignorar variables extra del .env


@lru_cache()
def get_settings() -> Settings:
    """
    Obtiene la configuración (cached para mejor performance)
    Usa @lru_cache para que solo se cargue una vez
    """
    return Settings()


# Instancia global de settings
settings = get_settings()
