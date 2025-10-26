"""
Router de Autenticación - Gestión de sesiones y seguridad
==========================================================
Maneja el inicio de sesión, cierre de sesión, renovación de tokens
y cambio de contraseñas con rate limiting y logging de seguridad.

Endpoints:
- POST /auth/login: Iniciar sesión (5 intentos/minuto)
- GET /auth/me: Obtener información de sesión actual
- POST /auth/logout: Cerrar sesión
- POST /auth/change-password: Cambiar contraseña
- POST /auth/refresh: Renovar token de acceso

Seguridad:
- Rate limiting en login (5 intentos/minuto)
- Logging de eventos de seguridad
- Verificación de usuario activo
- Registro en bitácora de auditoría

Autor: Sistema de Inspección de Contenedores
Versión: 2.1.0
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import timedelta
import logging
from slowapi import Limiter
from slowapi.util import get_remote_address

from ..core.database import get_db
from ..core.settings import settings
from ..middleware import security_event_logger
from ..models import Usuario, BitacoraAuditoria
from ..schemas.auth import LoginRequest, LoginResponse, TokenData, SessionInfo, PasswordChange
from ..utils.auth import (
    verify_password, 
    get_password_hash, 
    create_access_token,
    get_current_active_user,
    get_user_permissions
)


# ==========================================
# CONFIGURACIÓN DEL ROUTER
# ==========================================
router = APIRouter(prefix="/auth", tags=["Autenticación"])
logger = logging.getLogger(__name__)

# Configurar rate limiter para prevenir ataques de fuerza bruta
limiter = Limiter(key_func=get_remote_address)


# ==========================================
# ENDPOINT: LOGIN
# ==========================================
@router.post("/login", response_model=LoginResponse)
@limiter.limit("5/minute")  # Rate limiting: Máximo 5 intentos por minuto por IP
async def login(request: Request, credentials: LoginRequest, db: Session = Depends(get_db)):
    """
    Iniciar sesión y obtener token JWT
    
    Este endpoint maneja el proceso completo de autenticación:
    1. Busca el usuario por correo electrónico
    2. Verifica la contraseña hasheada
    3. Valida que el usuario esté activo
    4. Genera token JWT con duración configurable
    5. Registra el evento en bitácora de auditoría
    6. Retorna token de acceso y datos del usuario
    
    Seguridad:
    - Rate limiting: 5 intentos/minuto por IP (previene fuerza bruta)
    - Logging de todos los intentos fallidos y exitosos
    - Mensajes de error genéricos (no revela si usuario existe)
    - Verificación de estado activo del usuario
    
    Args:
        request: Objeto Request de FastAPI (para obtener IP del cliente)
        credentials: Credenciales del usuario (correo + password)
        db: Sesión de base de datos (inyectada automáticamente)
        
    Returns:
        LoginResponse: Token JWT, datos del usuario y tiempo de expiración
        
    Raises:
        HTTPException 401: Credenciales incorrectas
        HTTPException 403: Usuario inactivo
        HTTPException 429: Demasiados intentos (rate limit)
        
    Example:
        POST /auth/login
        {
            "correo": "admin@planta.com",
            "password": "Password123!"
        }
        
        Response:
        {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "usuario": {
                "id_usuario": 1,
                "correo": "admin@planta.com",
                "rol": "admin",
                "nombre": "Administrador"
            },
            "expires_in": 28800
        }
    """
    # Obtener IP del cliente para logging de seguridad
    client_ip = request.client.host if request.client else "unknown"
    
    # ===== PASO 1: BUSCAR USUARIO POR CORREO =====
    usuario = db.query(Usuario).filter(Usuario.correo == credentials.correo).first()
    
    if not usuario:
        # Seguridad: No revelar si el usuario existe
        security_event_logger.log_login_failure(credentials.correo, client_ip, "Usuario no existe")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos"  # Mensaje genérico
        )
    
    # ===== PASO 2: VERIFICAR CONTRASEÑA =====
    # Compara password en texto plano con hash almacenado usando bcrypt
    if not usuario.password_hash or not verify_password(credentials.password, usuario.password_hash):
        security_event_logger.log_login_failure(credentials.correo, client_ip, "Contraseña incorrecta")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos"  # Mismo mensaje genérico
        )
    
    # ===== PASO 3: VERIFICAR ESTADO ACTIVO =====
    # Solo usuarios con estado 'active' pueden iniciar sesión
    if usuario.estado != 'active':
        security_event_logger.log_login_failure(credentials.correo, client_ip, "Usuario inactivo")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo. Contacte al administrador."
        )
    
    # ===== PASO 4: LOGIN EXITOSO - LOG DE SEGURIDAD =====
    # ===== PASO 4: LOGIN EXITOSO - LOG DE SEGURIDAD =====
    security_event_logger.log_login_success(usuario.correo, client_ip)
    
    # ===== PASO 5: CREAR TOKEN JWT =====
    # Token incluye: id_usuario, correo, rol, nombre
    # Expira según configuración (default: 8 horas)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": str(usuario.id_usuario),  # "sub" = subject (estándar JWT)
            "correo": usuario.correo,
            "rol": usuario.rol,
            "nombre": usuario.nombre
        },
        expires_delta=access_token_expires
    )
    
    # ===== PASO 6: REGISTRAR EN BITÁCORA DE AUDITORÍA =====
    # Permite rastrear todos los logins en el sistema
    bitacora = BitacoraAuditoria(
        id_usuario=usuario.id_usuario,
        accion="LOGIN",
        detalles=f"Login exitoso desde {client_ip}"
    )
    db.add(bitacora)
    db.commit()
    
    # Log informativo en archivo app.log
    logger.info(f"Usuario {usuario.correo} inició sesión correctamente")
    
    # ===== PASO 7: RETORNAR RESPUESTA =====
    return LoginResponse(
        access_token=access_token,  # Token JWT para autenticación
        usuario=TokenData(  # Datos del usuario
            id_usuario=usuario.id_usuario,
            correo=usuario.correo,
            rol=usuario.rol,
            nombre=usuario.nombre
        ),
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60  # Segundos hasta expiración
    )


# ==========================================
# ENDPOINT: OBTENER INFORMACIÓN DE SESIÓN
# ==========================================
@router.get("/me", response_model=SessionInfo)
async def get_session_info(current_user: Usuario = Depends(get_current_active_user)):
    """
    Obtener información completa de la sesión actual
    
    Retorna los datos del usuario autenticado y sus permisos según su rol.
    Requiere token JWT válido en el header Authorization.
    
    Args:
        current_user: Usuario autenticado (inyectado automáticamente por Depends)
        
    Returns:
        SessionInfo: Datos del usuario y lista de permisos
        
    Example:
        GET /auth/me
        Headers: Authorization: Bearer <token>
        
        Response:
        {
            "id_usuario": 1,
            "nombre": "Admin Planta",
            "correo": "admin@planta.com",
            "rol": "admin",
            "estado": "active",
            "ultimo_acceso": "2025-10-14T23:45:12",
            "permisos": ["crear_usuarios", "editar_usuarios", ...]
        }
    """
    return SessionInfo(
        id_usuario=current_user.id_usuario,
        nombre=current_user.nombre,
        correo=current_user.correo,
        rol=current_user.rol,
        estado=current_user.estado,
        ultimo_acceso=current_user.ultimo_acceso,
        permisos=get_user_permissions(current_user.rol)  # Permisos según rol
    )


# ==========================================
# ENDPOINT: CERRAR SESIÓN
# ==========================================
@router.post("/logout")
async def logout(current_user: Usuario = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """
    Cerrar sesión del usuario
    
    Registra el logout en la bitácora de auditoría.
    Nota: El token JWT sigue siendo válido hasta su expiración,
    pero el frontend debe descartarlo.
    
    Args:
        current_user: Usuario autenticado
        db: Sesión de base de datos
        
    Returns:
        dict: Mensaje de confirmación
        
    Example:
        POST /auth/logout
        Headers: Authorization: Bearer <token>
        
        Response:
        {
            "mensaje": "Sesión cerrada exitosamente"
        }
    """
    # Registrar logout en bitácora de auditoría
    bitacora = BitacoraAuditoria(
        id_usuario=current_user.id_usuario,
        accion="LOGOUT",
        detalles="Logout desde aplicación web"
    )
    db.add(bitacora)
    db.commit()
    
    return {"mensaje": "Sesión cerrada exitosamente"}


# ==========================================
# ENDPOINT: CAMBIAR CONTRASEÑA
# ==========================================
@router.post("/change-password")
async def change_password(
    data: PasswordChange,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Cambiar la contraseña del usuario autenticado
    
    Requiere la contraseña actual para verificar identidad.
    La nueva contraseña debe cumplir con los requisitos de seguridad.
    
    Args:
        data: Contraseña actual y nueva contraseña
        current_user: Usuario autenticado
        db: Sesión de base de datos
        
    Returns:
        dict: Mensaje de confirmación
        
    Raises:
        HTTPException 400: Contraseña actual incorrecta
        
    Example:
        POST /auth/change-password
        Headers: Authorization: Bearer <token>
        {
            "password_actual": "OldPassword123!",
            "password_nueva": "NewPassword456!"
        }
        
        Response:
        {
            "mensaje": "Contraseña actualizada exitosamente"
        }
    """
    # ===== VERIFICAR CONTRASEÑA ACTUAL =====
    # Por seguridad, el usuario debe proporcionar su contraseña actual
    if not current_user.password_hash or not verify_password(data.password_actual, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contraseña actual incorrecta"
        )
    
    # ===== ACTUALIZAR A NUEVA CONTRASEÑA =====
    # Hashear nueva contraseña antes de guardarla
    current_user.password_hash = get_password_hash(data.password_nueva)
    
    # ===== REGISTRAR EN BITÁCORA =====
    # Importante para auditoría de seguridad
    bitacora = BitacoraAuditoria(
        id_usuario=current_user.id_usuario,
        accion="CAMBIO_PASSWORD",
        detalles="Cambio de contraseña exitoso"
    )
    db.add(bitacora)
    db.commit()
    
    return {"mensaje": "Contraseña actualizada exitosamente"}


# ==========================================
# ENDPOINT: RENOVAR TOKEN
# ==========================================
@router.post("/refresh")
async def refresh_token(current_user: Usuario = Depends(get_current_active_user)):
    """
    Renovar el token de acceso antes de que expire
    
    Permite obtener un nuevo token JWT sin necesidad de volver a ingresar
    credenciales. Útil para mantener sesiones activas.
    
    Args:
        current_user: Usuario autenticado (token actual debe ser válido)
        
    Returns:
        LoginResponse: Nuevo token JWT con nueva fecha de expiración
        
    Example:
        POST /auth/refresh
        Headers: Authorization: Bearer <token_viejo>
        
        Response:
        {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",  (NUEVO TOKEN)
            "usuario": {...},
            "expires_in": 28800
        }
    """
    # Crear nuevo token con misma información pero nueva fecha de expiración
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": current_user.id_usuario,
            "correo": current_user.correo,
            "rol": current_user.rol,
            "nombre": current_user.nombre
        },
        expires_delta=access_token_expires
    )
    
    return LoginResponse(
        access_token=access_token,
        usuario=TokenData(
            id_usuario=current_user.id_usuario,
            correo=current_user.correo,
            rol=current_user.rol,
            nombre=current_user.nombre
        ),
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
