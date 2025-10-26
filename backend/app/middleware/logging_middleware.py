"""
Middleware de logging para FastAPI
Registra todas las peticiones HTTP
"""
import time
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

logger = logging.getLogger("http")


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware para registrar todas las peticiones HTTP"""
    
    async def dispatch(self, request: Request, call_next):
        # Información de la petición
        start_time = time.time()
        client_ip = request.client.host if request.client else "unknown"
        method = request.method
        path = request.url.path
        
        # Obtener usuario si está autenticado
        user_info = "anonymous"
        if hasattr(request.state, "user"):
            user = request.state.user
            user_info = f"{user.correo} ({user.rol})"
        
        # Log de petición entrante
        logger.info(f"-> {method} {path} from {client_ip} [{user_info}]")
        
        # Procesar petición
        try:
            response: Response = await call_next(request)
            
            # Calcular tiempo de respuesta
            process_time = (time.time() - start_time) * 1000  # en ms
            
            # Log de respuesta
            status_code = response.status_code
            if status_code >= 500:
                logger.error(f"<- {status_code} {method} {path} ({process_time:.2f}ms)")
            elif status_code >= 400:
                logger.warning(f"<- {status_code} {method} {path} ({process_time:.2f}ms)")
            else:
                logger.info(f"<- {status_code} {method} {path} ({process_time:.2f}ms)")
            
            # Agregar header con tiempo de procesamiento
            response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
            
            return response
            
        except Exception as e:
            process_time = (time.time() - start_time) * 1000
            logger.exception(f"X ERROR {method} {path} ({process_time:.2f}ms): {str(e)}")
            raise


class SecurityEventLogger:
    """Logger especializado para eventos de seguridad"""
    
    def __init__(self):
        self.logger = logging.getLogger("security")
    
    def log_login_success(self, usuario: str, ip: str):
        """Registra login exitoso"""
        self.logger.info(f"OK LOGIN exitoso: {usuario} desde {ip}")
    
    def log_login_failure(self, correo: str, ip: str, razon: str):
        """Registra intento de login fallido"""
        self.logger.warning(f"X LOGIN fallido: {correo} desde {ip} - Razón: {razon}")
    
    def log_unauthorized_access(self, usuario: str, recurso: str, ip: str):
        """Registra intento de acceso no autorizado"""
        self.logger.warning(f"! ACCESO DENEGADO: {usuario} intentó acceder a {recurso} desde {ip}")
    
    def log_password_change(self, usuario: str, ip: str):
        """Registra cambio de contraseña"""
        self.logger.info(f"KEY CAMBIO DE CONTRASEÑA: {usuario} desde {ip}")
    
    def log_token_invalid(self, token_prefix: str, ip: str):
        """Registra token inválido"""
        self.logger.warning(f"! TOKEN INVÁLIDO: {token_prefix}... desde {ip}")


# Instancia global del logger de seguridad
security_event_logger = SecurityEventLogger()
