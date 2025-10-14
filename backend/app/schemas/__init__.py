"""Schemas Pydantic para validación y serialización"""
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional, List, Literal
from datetime import datetime


# ===== USUARIOS =====

class UsuarioBase(BaseModel):
    """Esquema base de usuario"""
    nombre: str = Field(..., min_length=1, max_length=120)
    correo: EmailStr
    rol: Literal['inspector', 'supervisor', 'admin'] = 'inspector'


class UsuarioCreate(UsuarioBase):
    """Esquema para crear usuario"""
    password: Optional[str] = Field(None, min_length=6)


class UsuarioUpdate(BaseModel):
    """Esquema para actualizar usuario"""
    nombre: Optional[str] = Field(None, min_length=1, max_length=120)
    correo: Optional[EmailStr] = None
    rol: Optional[Literal['inspector', 'supervisor', 'admin']] = None
    password: Optional[str] = Field(None, min_length=6)


class UsuarioEstado(BaseModel):
    """Esquema para cambiar estado"""
    estado: Literal['active', 'inactive']


class Usuario(UsuarioBase):
    """Esquema completo de usuario (respuesta)"""
    id_usuario: int
    estado: Literal['active', 'inactive']
    ultimo_acceso: Optional[datetime] = None
    creado_en: datetime
    actualizado_en: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ===== PLANTAS =====

class PlantaBase(BaseModel):
    """Esquema base de planta"""
    codigo: str = Field(..., min_length=1, max_length=50)
    nombre: str = Field(..., min_length=1, max_length=120)
    ubicacion: Optional[str] = Field(None, max_length=191)


class PlantaCreate(PlantaBase):
    """Esquema para crear planta"""
    pass


class PlantaUpdate(BaseModel):
    """Esquema para actualizar planta"""
    codigo: Optional[str] = Field(None, min_length=1, max_length=50)
    nombre: Optional[str] = Field(None, min_length=1, max_length=120)
    ubicacion: Optional[str] = Field(None, max_length=191)


class Planta(PlantaBase):
    """Esquema completo de planta (respuesta)"""
    id_planta: int
    creado_en: datetime
    actualizado_en: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ===== NAVIERAS =====

class NavieraBase(BaseModel):
    """Esquema base de naviera"""
    codigo: str = Field(..., min_length=1, max_length=50)
    nombre: str = Field(..., min_length=1, max_length=120)


class NavieraCreate(NavieraBase):
    """Esquema para crear naviera"""
    pass


class NavieraUpdate(BaseModel):
    """Esquema para actualizar naviera"""
    codigo: Optional[str] = Field(None, min_length=1, max_length=50)
    nombre: Optional[str] = Field(None, min_length=1, max_length=120)


class Naviera(NavieraBase):
    """Esquema completo de naviera (respuesta)"""
    id_navieras: int
    creado_en: datetime
    actualizado_en: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ===== FOTOS =====

class FotoInspeccionBase(BaseModel):
    """Esquema base de foto"""
    foto_path: str
    mime_type: str = 'image/jpeg'
    hash_hex: Optional[str] = None
    orden: int = 0
    tomada_en: Optional[datetime] = None


class FotoInspeccion(FotoInspeccionBase):
    """Esquema completo de foto (respuesta)"""
    id_foto: int
    id_inspeccion: int
    creado_en: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ===== INSPECCIONES =====

class InspeccionBase(BaseModel):
    """Esquema base de inspección"""
    numero_contenedor: str = Field(..., min_length=1, max_length=30)
    id_planta: int = Field(..., gt=0)
    id_navieras: int = Field(..., gt=0)
    temperatura_c: Optional[float] = Field(None, ge=-50, le=50)
    observaciones: Optional[str] = None


class InspeccionCreate(InspeccionBase):
    """Esquema para crear inspección"""
    id_inspector: int = Field(..., gt=0)
    inspeccionado_en: Optional[datetime] = None


class InspeccionUpdate(BaseModel):
    """Esquema para actualizar inspección"""
    numero_contenedor: Optional[str] = Field(None, min_length=1, max_length=30)
    id_planta: Optional[int] = Field(None, gt=0)
    id_navieras: Optional[int] = Field(None, gt=0)
    temperatura_c: Optional[float] = Field(None, ge=-50, le=50)
    observaciones: Optional[str] = None
    estado: Optional[Literal['pending', 'approved', 'rejected']] = None


class InspeccionEstadoUpdate(BaseModel):
    """Esquema para cambiar estado de inspección"""
    estado: Literal['approved', 'rejected']
    comentario: Optional[str] = Field(None, max_length=500)


class Inspeccion(InspeccionBase):
    """Esquema completo de inspección (respuesta)"""
    id_inspeccion: int
    codigo: str
    firma_path: Optional[str] = None
    id_inspector: int
    estado: Literal['pending', 'approved', 'rejected']
    inspeccionado_en: datetime
    creado_en: datetime
    actualizado_en: datetime
    
    model_config = ConfigDict(from_attributes=True)


class InspeccionDetalle(Inspeccion):
    """Esquema detallado con relaciones"""
    planta: Planta
    naviera: Naviera
    inspector: Usuario
    fotos: List[FotoInspeccion] = []
    
    model_config = ConfigDict(from_attributes=True)


class InspeccionCreated(BaseModel):
    """Respuesta al crear inspección"""
    id_inspeccion: int
    codigo: str
    mensaje: str = "Inspección creada exitosamente"


# ===== PREFERENCIAS =====

class PreferenciaUsuarioBase(BaseModel):
    """Esquema base de preferencias"""
    auto_sync: bool = True
    notificaciones: bool = True
    geolocalizacion: bool = False


class PreferenciaUsuarioUpdate(PreferenciaUsuarioBase):
    """Esquema para actualizar preferencias"""
    pass


class PreferenciaUsuario(PreferenciaUsuarioBase):
    """Esquema completo de preferencias (respuesta)"""
    id_usuario: int
    actualizado_en: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ===== REPORTES =====

class ConteoEstado(BaseModel):
    """Esquema para conteo por estado"""
    estado: Literal['pending', 'approved', 'rejected']
    total: int


class ResumenReporte(BaseModel):
    """Esquema para resumen de reporte"""
    total_inspecciones: int
    aprobadas: int
    pendientes: int
    rechazadas: int
    tasa_aprobacion: float
    periodo_desde: Optional[str] = None
    periodo_hasta: Optional[str] = None


# ===== PAGINACIÓN =====

class PaginatedResponse(BaseModel):
    """Respuesta paginada genérica"""
    items: List[Inspeccion]
    total: int
    page: int
    page_size: int
    total_pages: int


# ===== MENSAJES =====

class Message(BaseModel):
    """Mensaje genérico"""
    mensaje: str


class HealthResponse(BaseModel):
    """Respuesta de health check"""
    status: str = "ok"
    timestamp: datetime
