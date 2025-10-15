"""
Configuración de SQLAlchemy - Conexión a Base de Datos
=======================================================
Configura el motor de base de datos, pool de conexiones y sesiones.

Componentes principales:
- engine: Motor de conexión a MySQL
- SessionLocal: Fábrica de sesiones de BD
- Base: Clase base para modelos ORM
- get_db(): Dependency injection para FastAPI

Uso en routers:
    @router.get("/items")
    def get_items(db: Session = Depends(get_db)):
        items = db.query(Item).all()
        return items

Autor: Sistema de Inspección de Contenedores
Versión: 2.1.0
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from .settings import settings


# ==========================================
# MOTOR DE BASE DE DATOS
# ==========================================
# Crea el motor de conexión a MySQL con configuración optimizada
engine = create_engine(
    settings.database_url,  # mysql+pymysql://user:pass@host:port/db
    
    # ===== CONFIGURACIÓN DE POOL DE CONEXIONES =====
    # Pool: Conjunto de conexiones reutilizables para mejor rendimiento
    
    pool_pre_ping=True,  # Verifica conexión antes de usar (detecta caídas)
    pool_size=settings.DB_POOL_SIZE,  # Conexiones permanentes en el pool (10 por defecto)
    max_overflow=settings.DB_MAX_OVERFLOW,  # Conexiones extra bajo carga (20 por defecto)
    pool_recycle=3600,  # Recicla conexiones cada 1 hora (evita timeouts)
    
    # ===== MODO DEBUG =====
    echo=settings.DEBUG  # Si DEBUG=True, imprime todas las queries SQL
)

# ==========================================
# FÁBRICA DE SESIONES
# ==========================================
# SessionLocal: Clase que crea nuevas sesiones de base de datos
SessionLocal = sessionmaker(
    autocommit=False,  # Las transacciones deben confirmarse explícitamente
    autoflush=False,  # No ejecuta flush automático antes de queries
    bind=engine  # Vincula a nuestro motor de BD
)

# ==========================================
# BASE PARA MODELOS ORM
# ==========================================
# Todos los modelos (Planta, Usuario, Inspeccion, etc.) heredan de esta base
Base = declarative_base()


def get_db():
    """
    Dependency injection para obtener sesión de base de datos
    
    Esta función se usa con FastAPI Depends() para inyectar automáticamente
    una sesión de BD en los endpoints. La sesión se cierra automáticamente
    al finalizar la petición, incluso si hay errores.
    
    Yields:
        Session: Sesión de SQLAlchemy para ejecutar queries
        
    Example:
        from fastapi import Depends
        from sqlalchemy.orm import Session
        
        @router.get("/plantas")
        def listar_plantas(db: Session = Depends(get_db)):
            plantas = db.query(Planta).all()
            return plantas
            
    Flujo:
        1. FastAPI llama get_db() al recibir una petición
        2. Se crea una sesión (db = SessionLocal())
        3. Se "yield" la sesión al endpoint
        4. El endpoint ejecuta sus queries
        5. La sesión se cierra en el bloque finally
        6. La conexión vuelve al pool para reutilizarse
    """
    db = SessionLocal()  # Crear nueva sesión
    try:
        yield db  # Entregar sesión al endpoint
    finally:
        db.close()  # Cerrar sesión (libera conexión al pool)
