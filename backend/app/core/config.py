"""Configuración de la aplicación"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Configuración desde variables de entorno"""
    
    # Base de datos
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "ImpeccionContenedor"
    
    # Archivos
    CAPTURAS_DIR: str = "../capturas"
    
    # Servidor
    BACKEND_PORT: int = 8000
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:5173"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )
    
    @property
    def database_url(self) -> str:
        """Construye la URL de conexión a MySQL"""
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convierte CORS_ORIGINS en lista"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


# Instancia global de configuración
settings = Settings()
