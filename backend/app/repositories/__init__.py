from .plantas import planta_repository
from .navieras import naviera_repository
from .usuarios import usuario_repository
from .inspecciones import inspeccion_repository, foto_repository
from .preferencias import preferencia_repository
from .reportes import reporte_repository

__all__ = [
    "planta_repository",
    "naviera_repository",
    "usuario_repository",
    "inspeccion_repository",
    "foto_repository",
    "preferencia_repository",
    "reporte_repository",
]
