"""Aplicación principal FastAPI"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import os
import logging
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from .core.settings import settings
from .core.logging import setup_logging
from .middleware import LoggingMiddleware
from .utils import ensure_dir
from .routers import (
    plantas_router,
    navieras_router,
    usuarios_router,
    inspecciones_router,
    reportes_router,
    preferencias_router,
    auth_router,
    estadisticas_router,
    reportes_export_router
)
from .schemas import HealthResponse

# Configurar logging
setup_logging()
logger = logging.getLogger(__name__)

logger.info(f"🚀 Iniciando {settings.APP_NAME} v{settings.APP_VERSION}")
logger.info(f"Entorno: {settings.ENVIRONMENT}")
logger.info(f"Debug mode: {settings.DEBUG}")

# Crear directorios necesarios
ensure_dir(settings.CAPTURAS_DIR)
ensure_dir(os.path.join(settings.CAPTURAS_DIR, "inspecciones"))
ensure_dir(os.path.join(settings.CAPTURAS_DIR, "firmas"))

# Inicializar aplicación
app = FastAPI(
    title=settings.APP_NAME,
    description="API REST para gestión de inspecciones de contenedores frutícolas",
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.DEBUG else None,  # Deshabilitar docs en producción
    redoc_url="/redoc" if settings.DEBUG else None
)

# Middleware de logging (debe ir PRIMERO)
app.add_middleware(LoggingMiddleware)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

logger.info(f"CORS configurado: {', '.join(settings.cors_origins)}")

# Montar archivos estáticos
app.mount(
    "/capturas",
    StaticFiles(directory=settings.CAPTURAS_DIR),
    name="capturas"
)

# Health check
@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    """Endpoint de salud de la aplicación"""
    return {
        "status": "ok",
        "timestamp": datetime.now()
    }

# Registrar routers con prefijo /api
app.include_router(auth_router, prefix="/api")
app.include_router(plantas_router, prefix="/api")
app.include_router(navieras_router, prefix="/api")
app.include_router(usuarios_router, prefix="/api")
app.include_router(inspecciones_router, prefix="/api")
app.include_router(reportes_router, prefix="/api")
app.include_router(preferencias_router, prefix="/api")
app.include_router(estadisticas_router, prefix="/api")
app.include_router(reportes_export_router, prefix="/api/reportes/export")

logger.info("✅ Todos los routers registrados")


# Root endpoint
@app.get("/", tags=["Root"])
def root():
    """Endpoint raíz"""
    return {
        "mensaje": "Sistema de Inspección de Contenedores - API REST",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.BACKEND_PORT,
        reload=True
    )
