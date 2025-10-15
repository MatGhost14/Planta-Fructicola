"""Router de autenticación"""
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


router = APIRouter(prefix="/auth", tags=["Autenticación"])
logger = logging.getLogger(__name__)
limiter = Limiter(key_func=get_remote_address)


@router.post("/login", response_model=LoginResponse)
@limiter.limit("5/minute")
async def login(request: Request, credentials: LoginRequest, db: Session = Depends(get_db)):
    """Login de usuario - Rate limit: 5 intentos por minuto"""
    client_ip = request.client.host if request.client else "unknown"
    
    # Buscar usuario por correo
    usuario = db.query(Usuario).filter(Usuario.correo == credentials.correo).first()
    
    if not usuario:
        security_event_logger.log_login_failure(credentials.correo, client_ip, "Usuario no existe")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos"
        )
    
    # Verificar contraseña
    if not usuario.password_hash or not verify_password(credentials.password, usuario.password_hash):
        security_event_logger.log_login_failure(credentials.correo, client_ip, "Contraseña incorrecta")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos"
        )
    
    # Verificar estado activo
    if usuario.estado != 'active':
        security_event_logger.log_login_failure(credentials.correo, client_ip, "Usuario inactivo")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo. Contacte al administrador."
        )
    
    # Login exitoso - log de seguridad
    security_event_logger.log_login_success(usuario.correo, client_ip)
    
    # Crear token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": str(usuario.id_usuario),  # Convertir a string
            "correo": usuario.correo,
            "rol": usuario.rol,
            "nombre": usuario.nombre
        },
        expires_delta=access_token_expires
    )
    
    # Registrar en bitácora
    bitacora = BitacoraAuditoria(
        id_usuario=usuario.id_usuario,
        accion="LOGIN",
        detalles=f"Login exitoso desde {client_ip}"
    )
    db.add(bitacora)
    db.commit()
    
    logger.info(f"Usuario {usuario.correo} inició sesión correctamente")
    
    return LoginResponse(
        access_token=access_token,
        usuario=TokenData(
            id_usuario=usuario.id_usuario,
            correo=usuario.correo,
            rol=usuario.rol,
            nombre=usuario.nombre
        ),
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.get("/me", response_model=SessionInfo)
async def get_session_info(current_user: Usuario = Depends(get_current_active_user)):
    """Obtener información de la sesión actual"""
    return SessionInfo(
        id_usuario=current_user.id_usuario,
        nombre=current_user.nombre,
        correo=current_user.correo,
        rol=current_user.rol,
        estado=current_user.estado,
        ultimo_acceso=current_user.ultimo_acceso,
        permisos=get_user_permissions(current_user.rol)
    )


@router.post("/logout")
async def logout(current_user: Usuario = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Logout de usuario"""
    # Registrar en bitácora
    bitacora = BitacoraAuditoria(
        id_usuario=current_user.id_usuario,
        accion="LOGOUT",
        detalles="Logout desde aplicación web"
    )
    db.add(bitacora)
    db.commit()
    
    return {"mensaje": "Sesión cerrada exitosamente"}


@router.post("/change-password")
async def change_password(
    data: PasswordChange,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Cambiar contraseña del usuario actual"""
    # Verificar contraseña actual
    if not current_user.password_hash or not verify_password(data.password_actual, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contraseña actual incorrecta"
        )
    
    # Actualizar contraseña
    current_user.password_hash = get_password_hash(data.password_nueva)
    
    # Registrar en bitácora
    bitacora = BitacoraAuditoria(
        id_usuario=current_user.id_usuario,
        accion="CAMBIO_PASSWORD",
        detalles="Cambio de contraseña exitoso"
    )
    db.add(bitacora)
    db.commit()
    
    return {"mensaje": "Contraseña actualizada exitosamente"}


@router.post("/refresh")
async def refresh_token(current_user: Usuario = Depends(get_current_active_user)):
    """Renovar token de acceso"""
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
