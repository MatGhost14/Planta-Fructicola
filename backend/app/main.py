"""Aplicación principal FastAPI"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import os

from .core import settings
from .utils import ensure_dir
from .routers import (
    plantas_router,
    navieras_router,
    usuarios_router,
    inspecciones_router,
    reportes_router,
    preferencias_router,
    auth_router
)
from .schemas import HealthResponse

# Crear directorios necesarios
ensure_dir(settings.CAPTURAS_DIR)
ensure_dir(os.path.join(settings.CAPTURAS_DIR, "inspecciones"))
ensure_dir(os.path.join(settings.CAPTURAS_DIR, "firmas"))

# Inicializar aplicación
app = FastAPI(
    title="Sistema de Inspección de Contenedores",
    description="API REST para gestión de inspecciones de contenedores frutícolas",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

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
