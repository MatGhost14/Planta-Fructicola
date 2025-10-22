"""Sistema de autenticación JWT"""
from datetime import datetime, timedelta
from typing import Optional, Literal
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.settings import settings
from ..models import Usuario
from ..schemas.auth import TokenData


# Contexto de encriptación - usando pbkdf2_sha256 que es más confiable
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Security scheme
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar contraseña"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generar hash de contraseña"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crear token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[TokenData]:
    """Decodificar token JWT"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        id_usuario_str: str = payload.get("sub")
        correo: str = payload.get("correo")
        rol: str = payload.get("rol")
        nombre: str = payload.get("nombre")
        
        if id_usuario_str is None or correo is None or rol is None:
            return None
        
        # Convertir id_usuario de string a int
        try:
            id_usuario = int(id_usuario_str)
        except (ValueError, TypeError):
            return None
            
        return TokenData(
            id_usuario=id_usuario,
            correo=correo,
            rol=rol,
            nombre=nombre
        )
    except JWTError:
        return None
    except Exception:
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Usuario:
    """Obtener usuario actual desde token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        token_data = decode_token(token)
        
        if token_data is None:
            raise credentials_exception
        
        usuario = db.query(Usuario).filter(Usuario.id_usuario == token_data.id_usuario).first()
        
        if usuario is None:
            raise credentials_exception
        
        if usuario.estado != 'active':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario inactivo"
            )
        
        # Actualizar último acceso
        usuario.ultimo_acceso = datetime.now()
        db.commit()
        
        return usuario
    except HTTPException:
        raise
    except Exception:
        raise credentials_exception
    
    return usuario


async def get_current_active_user(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """Verificar que el usuario esté activo"""
    if current_user.estado != 'active':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    return current_user


# Decoradores de permisos por rol

def require_role(*roles: Literal['inspector', 'supervisor', 'admin']):
    """Decorador para requerir roles específicos"""
    async def role_checker(current_user: Usuario = Depends(get_current_active_user)) -> Usuario:
        if current_user.rol not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere rol: {', '.join(roles)}"
            )
        return current_user
    return role_checker


# Aliases para facilitar uso
require_inspector = require_role('inspector', 'supervisor', 'admin')
require_supervisor = require_role('supervisor', 'admin')
require_admin = require_role('admin')


def check_inspector_access(current_user: Usuario, id_inspector: int) -> bool:
    """Verificar si el usuario puede acceder a datos de un inspector"""
    # Admin y supervisor pueden ver todo
    if current_user.rol in ['admin', 'supervisor']:
        return True
    # Inspector solo puede ver sus propios datos
    return current_user.id_usuario == id_inspector


def check_planta_access(db: Session, current_user: Usuario, id_planta: int) -> bool:
    """Verificar si el usuario puede acceder a datos de una planta"""
    # Admin puede ver todo
    if current_user.rol == 'admin':
        return True
    
    # Supervisor solo puede ver su planta asignada
    # TODO: Implementar tabla de asignación usuario-planta
    # Por ahora, permitimos acceso a todos los supervisores
    if current_user.rol == 'supervisor':
        return True
    
    # Inspector solo puede ver inspecciones de su planta
    # TODO: Implementar lógica de verificación
    return False


def get_user_permissions(rol: str) -> dict:
    """Obtener permisos según rol"""
    permissions = {
        'inspector': {
            'inspecciones': ['read_own', 'create', 'update_own'],
            'fotos': ['upload', 'view_own'],
            'firmas': ['create'],
            'reportes': ['view_own'],
            'preferencias': ['read', 'update']
        },
        'supervisor': {
            'inspecciones': ['read_all_planta', 'create', 'update', 'approve', 'reject'],
            'fotos': ['view_all_planta'],
            'firmas': ['view_all_planta'],
            'reportes': ['view_planta'],
            'plantas': ['read', 'update'],
            'navieras': ['read', 'create', 'update'],
            'usuarios': ['read_planta'],
            'bitacora': ['read_planta'],
            'preferencias': ['read', 'update']
        },
        'admin': {
            'inspecciones': ['full_access'],
            'fotos': ['full_access'],
            'firmas': ['full_access'],
            'reportes': ['full_access'],
            'plantas': ['full_access'],
            'navieras': ['full_access'],
            'usuarios': ['full_access'],
            'bitacora': ['full_access'],
            'preferencias': ['read', 'update'],
            'configuracion': ['full_access'],
            'tokens_api': ['manage']
        }
    }
    
    return permissions.get(rol, {})
