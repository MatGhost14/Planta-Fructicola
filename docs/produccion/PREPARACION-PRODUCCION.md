# 🚀 Checklist de Preparación para Producción

## Fecha: 14 de octubre de 2025
## Sistema: Inspección de Contenedores Frutícolas v2.1.0

---

## 📊 Estado Actual: 70% Completado

```
Funcionalidades Core:     ████████████████████░░░░░░ 85%
Seguridad:               ███████████████░░░░░░░░░░░░ 60%
Configuración:           ███████████░░░░░░░░░░░░░░░░ 45%
Testing:                 ████████████████░░░░░░░░░░░ 65%
Documentación:           ████████████████████░░░░░░░ 80%
Optimización:            ██████████░░░░░░░░░░░░░░░░░ 40%

TOTAL:                   ██████████████░░░░░░░░░░░░░ 62.5%
```

---

## 🔴 CRÍTICO - Debe hacerse antes de producción

### 1. Seguridad 🔒

#### ❌ Secret Key en Código
**Problema**: 
```python
# backend/app/utils/auth.py
SECRET_KEY = "tu-clave-secreta-super-segura-cambiar-en-produccion"
```
**Solución**:
```python
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY no está configurada")
```

**Archivos a modificar**:
- [ ] `backend/app/utils/auth.py`
- [ ] Crear `backend/.env.example`
- [ ] Agregar `.env` a `.gitignore`

#### ❌ Credenciales de Base de Datos en Código
**Problema**:
```python
# backend/app/core/database.py
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root@localhost/impeccioncontenedor"
```
**Solución**:
```python
DATABASE_URL = os.getenv("DATABASE_URL")
SQLALCHEMY_DATABASE_URL = DATABASE_URL
```

**Archivos a modificar**:
- [ ] `backend/app/core/database.py`
- [ ] `backend/app/core/settings.py`

#### ❌ CORS Abierto para Todos
**Problema**:
```python
# backend/app/main.py
allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"]
```
**Solución**:
```python
allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
allow_origins=allowed_origins
```

**Archivos a modificar**:
- [ ] `backend/app/main.py`

---

### 2. Variables de Entorno 🌍

#### ❌ No hay archivo .env
**Crear**: `backend/.env.example`
```env
# Aplicación
APP_NAME=Sistema de Inspección de Contenedores
APP_VERSION=2.1.0
DEBUG=False
ENVIRONMENT=production

# Seguridad
SECRET_KEY=CAMBIAR_POR_CLAVE_SEGURA_LARGA_Y_ALEATORIA_64_CARACTERES_MINIMO
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480

# Base de Datos
DATABASE_URL=mysql+pymysql://usuario:password@host:3306/nombre_bd
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20

# CORS
ALLOWED_ORIGINS=https://tudominio.com,https://app.tudominio.com

# Archivos
CAPTURAS_DIR=/var/www/capturas
MAX_FILE_SIZE=10485760

# Email (para notificaciones futuras)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
SMTP_FROM=noreply@tuempresa.com

# Logs
LOG_LEVEL=INFO
LOG_FILE=/var/log/inspeccion/app.log
```

**Archivos a crear**:
- [ ] `backend/.env.example`
- [ ] `backend/.env` (con valores reales, no commitear)
- [ ] `frontend/.env.example`
- [ ] `frontend/.env.production`

---

### 3. Gestión de Contraseñas 🔑

#### ❌ Contraseñas por Defecto en Usuarios de Prueba
**Problema**: Usuarios con `password123`

**Solución**:
- [ ] Eliminar usuarios de prueba antes de producción
- [ ] Crear script para generar primer admin con contraseña segura
- [ ] Implementar política de contraseñas:
  - Mínimo 8 caracteres
  - Al menos 1 mayúscula, 1 minúscula, 1 número, 1 símbolo
  - No puede ser igual a contraseñas anteriores

**Archivos a crear**:
- [ ] `backend/scripts/create_admin.py`
- [ ] `backend/app/utils/password_policy.py`

---

### 4. HTTPS y SSL 🔐

#### ❌ No hay configuración SSL
**Solución**:
- [ ] Configurar HTTPS en producción
- [ ] Obtener certificado SSL (Let's Encrypt)
- [ ] Configurar Nginx/Apache como reverse proxy
- [ ] Forzar HTTPS en frontend

**Archivos a crear**:
- [ ] `nginx.conf` (configuración del servidor)
- [ ] Script de renovación automática de certificados

---

## 🟡 IMPORTANTE - Recomendado antes de producción

### 5. Logging y Monitoreo 📊

#### ⚠️ No hay sistema de logs estructurado
**Solución**:
```python
import logging
from logging.handlers import RotatingFileHandler

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('app.log', maxBytes=10485760, backupCount=5),
        logging.StreamHandler()
    ]
)
```

**Archivos a crear**:
- [ ] `backend/app/core/logging.py`
- [ ] `backend/app/middleware/logging_middleware.py`

**Implementar**:
- [ ] Logs de autenticación (login exitoso/fallido)
- [ ] Logs de cambios de estado de inspecciones
- [ ] Logs de operaciones CRUD
- [ ] Logs de errores con stack trace

---

### 6. Manejo de Errores 🚨

#### ⚠️ Errores exponen detalles internos
**Solución**:
```python
# backend/app/main.py
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Error no manejado: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor"}
    )
```

**Archivos a modificar**:
- [ ] `backend/app/main.py` (agregar handlers globales)
- [ ] Todos los routers (mejorar mensajes de error)

---

### 7. Rate Limiting ⏱️

#### ⚠️ No hay límite de peticiones
**Problema**: Vulnerable a ataques DDoS

**Solución**:
```bash
pip install slowapi
```

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/auth/login")
@limiter.limit("5/minute")  # Máximo 5 intentos por minuto
async def login(...):
    ...
```

**Archivos a modificar**:
- [ ] `backend/app/main.py`
- [ ] `backend/app/routers/auth.py`
- [ ] `backend/requirements.txt`

---

### 8. Validación de Archivos 📁

#### ⚠️ Validación básica de archivos subidos
**Mejorar**:
- [ ] Validar extensiones permitidas (whitelist)
- [ ] Verificar magic bytes del archivo (no solo extensión)
- [ ] Escanear con antivirus (ClamAV)
- [ ] Limitar tamaño máximo de archivos
- [ ] Generar nombres aleatorios para evitar colisiones

**Archivos a crear**:
- [ ] `backend/app/utils/file_validator.py`

---

### 9. Base de Datos 💾

#### ⚠️ No hay backups automáticos
**Solución**:
- [ ] Script de backup diario de MySQL
- [ ] Backup de archivos (capturas/)
- [ ] Restauración automática en caso de fallo
- [ ] Almacenamiento en ubicación segura (S3, etc.)

**Archivos a crear**:
- [ ] `scripts/backup_database.sh`
- [ ] `scripts/backup_files.sh`
- [ ] Configurar cron jobs

#### ⚠️ Índices de base de datos
**Optimizar**:
```sql
-- Índices recomendados
CREATE INDEX idx_inspecciones_estado ON inspecciones(estado);
CREATE INDEX idx_inspecciones_fecha ON inspecciones(inspeccionado_en);
CREATE INDEX idx_inspecciones_inspector ON inspecciones(id_inspector);
CREATE INDEX idx_usuarios_correo ON usuarios(correo);
CREATE INDEX idx_usuarios_estado ON usuarios(estado);
```

**Archivos a crear**:
- [ ] `database/migrations/add_indexes.sql`

---

### 10. Caché ⚡

#### ⚠️ No hay sistema de caché
**Solución**: Implementar Redis para:
- Catálogos (plantas, navieras) - cambian poco
- Resultados de búsquedas frecuentes
- Sesiones de usuario

**Archivos a crear**:
- [ ] `backend/app/core/cache.py`
- [ ] Configuración de Redis en docker-compose.yml

---

## 🟢 OPCIONAL - Mejoras recomendadas

### 11. Testing 🧪

#### ✅ Tests Actuales
- [x] Tests manuales de endpoints (16/16 pasaron)
- [x] Guía de pruebas documentada

#### ⚠️ Tests Faltantes
- [ ] Tests unitarios con pytest
- [ ] Tests de integración
- [ ] Tests de carga (locust, k6)
- [ ] Tests de seguridad (OWASP ZAP)
- [ ] Tests E2E con Playwright/Cypress

**Archivos a crear**:
- [ ] `backend/tests/test_auth.py`
- [ ] `backend/tests/test_inspecciones.py`
- [ ] `backend/tests/test_usuarios.py`
- [ ] `frontend/tests/integration/`
- [ ] `frontend/tests/e2e/`

---

### 12. Documentación API 📚

#### ⚠️ Documentación básica con FastAPI
**Mejorar**:
- [ ] Agregar ejemplos de request/response en cada endpoint
- [ ] Documentar códigos de error
- [ ] Agregar schemas de validación
- [ ] Crear Postman Collection

**Archivos a modificar**:
- [ ] Todos los routers (agregar docstrings detallados)
- [ ] `backend/app/main.py` (configurar Swagger UI)

---

### 13. Optimización Frontend ⚡

#### ⚠️ Bundle size
**Optimizar**:
```bash
# Analizar bundle
npm run build
npx vite-bundle-analyzer
```

**Mejoras**:
- [ ] Code splitting por ruta
- [ ] Lazy loading de componentes
- [ ] Optimización de imágenes
- [ ] Minificación y compresión (gzip, brotli)
- [ ] CDN para assets estáticos

**Archivos a modificar**:
- [ ] `frontend/vite.config.ts`

---

### 14. PWA (Progressive Web App) 📱

#### ⚠️ No es PWA
**Agregar**:
- [ ] Service Worker para offline
- [ ] Manifest.json
- [ ] Iconos de diferentes tamaños
- [ ] Instalable en dispositivos móviles

**Archivos a crear**:
- [ ] `frontend/public/manifest.json`
- [ ] `frontend/src/service-worker.ts`

---

### 15. Internacionalización 🌍

#### ⚠️ Solo español
**Agregar** (opcional):
- [ ] Soporte multi-idioma (i18n)
- [ ] Inglés como segundo idioma
- [ ] Detección automática de idioma del navegador

---

### 16. Notificaciones 🔔

#### ⚠️ No hay sistema de notificaciones
**Implementar**:
- [ ] Email cuando inspección es aprobada/rechazada
- [ ] Notificaciones en tiempo real (WebSockets)
- [ ] Push notifications en navegador

---

## 📋 Plan de Implementación Sugerido

### Fase 1: Seguridad Crítica (1-2 días) 🔴
**Prioridad: ALTA**
```
□ Variables de entorno
□ Secret key segura
□ Credenciales BD en .env
□ CORS restrictivo
□ HTTPS obligatorio
□ Eliminar usuarios de prueba
```

### Fase 2: Configuración de Producción (2-3 días) 🟡
**Prioridad: MEDIA-ALTA**
```
□ Sistema de logging
□ Manejo de errores global
□ Rate limiting
□ Validación de archivos mejorada
□ Backups automáticos
□ Índices de BD
```

### Fase 3: Testing y QA (2-3 días) 🟡
**Prioridad: MEDIA**
```
□ Tests unitarios (cobertura 70%+)
□ Tests de integración
□ Tests de carga
□ Tests de seguridad
□ Corrección de bugs encontrados
```

### Fase 4: Optimización (1-2 días) 🟢
**Prioridad: BAJA-MEDIA**
```
□ Caché con Redis
□ Optimización de queries
□ Code splitting frontend
□ Compresión de assets
□ CDN para archivos estáticos
```

### Fase 5: Documentación (1 día) 🟢
**Prioridad: BAJA**
```
□ Documentación API detallada
□ Manual de despliegue
□ Manual de mantenimiento
□ Runbook de incidentes
```

---

## 🚀 Checklist de Despliegue

### Pre-Despliegue
```
□ Código en repositorio actualizado
□ Variables de entorno configuradas
□ Base de datos migrada
□ SSL configurado
□ Backup de datos existentes
□ Plan de rollback documentado
```

### Despliegue
```
□ Servidor configurado (Ubuntu/CentOS)
□ Nginx/Apache configurado
□ Firewall configurado
□ Docker/docker-compose (opcional)
□ Scripts de inicio automático (systemd)
□ Monitoreo configurado
```

### Post-Despliegue
```
□ Smoke tests en producción
□ Verificar logs
□ Monitorear métricas
□ Verificar backups
□ Documentar incidentes
```

---

## 📊 Estimación de Tiempo

| Fase | Días | Prioridad |
|------|------|-----------|
| Seguridad Crítica | 1-2 | 🔴 ALTA |
| Configuración | 2-3 | 🟡 MEDIA-ALTA |
| Testing | 2-3 | 🟡 MEDIA |
| Optimización | 1-2 | 🟢 BAJA-MEDIA |
| Documentación | 1 | 🟢 BAJA |
| **TOTAL** | **7-11 días** | |

---

## 🎯 Mínimo Viable para Producción (MVP)

Si necesitas desplegar **urgentemente**, esto es lo MÍNIMO indispensable:

### ✅ Checklist Mínimo (2-3 días)
```
☑️ Variables de entorno (.env)
☑️ Secret key segura (generada aleatoriamente)
☑️ Credenciales BD seguras
☑️ CORS restrictivo (solo dominio de producción)
☑️ HTTPS obligatorio
☑️ Eliminar usuarios de prueba
☑️ Crear admin de producción con contraseña fuerte
☑️ Logging básico
☑️ Backups manuales configurados
☑️ Tests smoke en producción
```

---

## 🏆 Recomendación Final

**Para un despliegue seguro y confiable:**
- Implementar **Fase 1 y 2** (4-5 días) antes de producción
- Fase 3 en paralelo con producción beta
- Fases 4 y 5 en iteraciones posteriores

**Estado actual**: 
```
🟢 Funcionalidad: EXCELENTE (85%)
🟡 Seguridad: NECESITA TRABAJO (60%)
🟡 Configuración: NECESITA TRABAJO (45%)
```

**Tiempo estimado para producción segura**: **5-7 días laborales**

---

## 📞 Contacto y Soporte

- Documentación: Ver README.md, TUTORIAL.md
- Issues: GitHub Issues del repositorio
- Logs: /var/log/inspeccion/app.log

---

**Última actualización**: 14 de octubre de 2025  
**Versión**: 2.1.0  
**Estado**: 62.5% listo para producción
