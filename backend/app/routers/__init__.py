from .plantas import router as plantas_router
from .navieras import router as navieras_router
from .usuarios import router as usuarios_router
from .inspecciones import router as inspecciones_router
from .reportes import router as reportes_router
from .preferencias import router as preferencias_router
from .auth import router as auth_router

__all__ = [
    "plantas_router",
    "navieras_router",
    "usuarios_router",
    "inspecciones_router",
    "reportes_router",
    "preferencias_router",
    "auth_router",
]
