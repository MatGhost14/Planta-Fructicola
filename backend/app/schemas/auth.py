"""Schemas de autenticación"""
from pydantic import BaseModel, EmailStr
from typing import Literal, Optional
from datetime import datetime


class LoginRequest(BaseModel):
    """Request de login"""
    correo: EmailStr
    password: str


class TokenData(BaseModel):
    """Datos del token JWT"""
    id_usuario: int
    correo: str
    rol: Literal['inspector', 'supervisor', 'admin']
    nombre: str


class LoginResponse(BaseModel):
    """Respuesta de login exitoso"""
    access_token: str
    token_type: str = "bearer"
    usuario: TokenData
    expires_in: int  # segundos


class PasswordChange(BaseModel):
    """Cambio de contraseña"""
    password_actual: str
    password_nueva: str


class PasswordReset(BaseModel):
    """Reset de contraseña por admin"""
    password_nueva: str


class SessionInfo(BaseModel):
    """Información de sesión actual"""
    id_usuario: int
    nombre: str
    correo: str
    rol: Literal['inspector', 'supervisor', 'admin']
    estado: Literal['active', 'inactive']
    ultimo_acceso: Optional[datetime] = None
    permisos: dict
