# 🔧 Backend - Sistema de Inspección de Contenedores

## 📋 Índice

- [Descripción General](#descripción-general)
- [Tecnologías](#tecnologías)
- [Arquitectura](#arquitectura)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Modelos de Datos](#modelos-de-datos)
- [API Endpoints](#api-endpoints)
- [Seguridad y Autenticación](#seguridad-y-autenticación)
- [Base de Datos](#base-de-datos)
- [Instalación y Configuración](#instalación-y-configuración)
- [Testing](#testing)

---

## 📝 Descripción General

El backend del Sistema de Inspección de Contenedores es una **API RESTful** construida con **FastAPI** que gestiona todas las operaciones relacionadas con inspecciones de contenedores frutícolas, incluyendo:

- ✅ Gestión de inspecciones y fotografías
- ✅ Administración de usuarios, plantas y navieras
- ✅ Generación de reportes y estadísticas
- ✅ Autenticación y autorización basada en roles
- ✅ Almacenamiento seguro de archivos multimedia

---

## 🚀 Tecnologías

### Core
- **FastAPI 0.104.1** - Framework web asíncrono de alto rendimiento
- **Python 3.10+** - Lenguaje de programación
- **Uvicorn** - Servidor ASGI de producción

### Base de Datos
- **MySQL 8.0+** - Base de datos relacional
- **SQLAlchemy 2.0** - ORM (Object-Relational Mapping)
- **Alembic** - Migraciones de base de datos

### Seguridad
- **Passlib + Bcrypt** - Hashing de contraseñas
- **JWT (JSON Web Tokens)** - Autenticación sin estado
- **python-jose** - Manejo de tokens JWT

### Validación y Schemas
- **Pydantic v2** - Validación de datos y serialización

### Utilidades
- **python-multipart** - Manejo de archivos multipart/form-data
- **Pillow** - Procesamiento de imágenes
- **python-dotenv** - Variables de entorno

---

## 🏗️ Arquitectura

El backend sigue una **arquitectura en capas (Layered Architecture)** con separación de responsabilidades:

```
┌─────────────────────────────────────┐
│         API Layer (Routers)         │ ← Endpoints HTTP
├─────────────────────────────────────┤
│       Services Layer (Logic)        │ ← Lógica de negocio
├─────────────────────────────────────┤
│   Repository Layer (Data Access)    │ ← Acceso a datos
├─────────────────────────────────────┤
│         Models (ORM Entities)       │ ← Entidades de BD
├─────────────────────────────────────┤
│         Database (MySQL)            │ ← Almacenamiento
└─────────────────────────────────────┘
```

### Patrones de Diseño Implementados

1. **Repository Pattern**: Abstracción del acceso a datos
2. **Dependency Injection**: Inyección de dependencias con FastAPI
3. **DTO Pattern**: Schemas de Pydantic para transferencia de datos
4. **Middleware Pattern**: Interceptores para CORS, logging, errores
5. **Service Layer Pattern**: Lógica de negocio centralizada

---

## 📁 Estructura del Proyecto

```
backend/
├── alembic/                    # Migraciones de base de datos
│   ├── versions/              # Scripts de migración
│   └── env.py                 # Configuración de Alembic
│
├── app/                       # Aplicación principal
│   ├── core/                  # Configuración central
│   │   ├── config.py         # Variables de entorno y settings
│   │   ├── database.py       # Configuración de SQLAlchemy
│   │   └── security.py       # Utilidades de seguridad
│   │
│   ├── middleware/            # Middlewares personalizados
│   │   ├── cors.py           # Configuración CORS
│   │   ├── error_handler.py # Manejo global de errores
│   │   └── logging.py        # Logging de requests
│   │
│   ├── models/                # Modelos ORM (SQLAlchemy)
│   │   ├── __init__.py       # Exporta todos los modelos
│   │   ├── usuario.py        # Modelo Usuario
│   │   ├── planta.py         # Modelo Planta
│   │   ├── naviera.py        # Modelo Naviera
│   │   ├── inspeccion.py     # Modelo Inspección
│   │   ├── foto.py           # Modelo Foto
│   │   ├── firma.py          # Modelo Firma
│   │   └── preferencias.py   # Modelo Preferencias
│   │
│   ├── schemas/               # Schemas Pydantic (DTOs)
│   │   ├── usuario.py        # DTOs de Usuario
│   │   ├── planta.py         # DTOs de Planta
│   │   ├── naviera.py        # DTOs de Naviera
│   │   ├── inspeccion.py     # DTOs de Inspección
│   │   ├── foto.py           # DTOs de Foto
│   │   ├── firma.py          # DTOs de Firma
│   │   └── auth.py           # DTOs de autenticación
│   │
│   ├── repositories/          # Capa de acceso a datos
│   │   ├── __init__.py
│   │   ├── usuarios.py       # CRUD de Usuarios
│   │   ├── plantas.py        # CRUD de Plantas
│   │   ├── navieras.py       # CRUD de Navieras
│   │   ├── inspecciones.py   # CRUD de Inspecciones
│   │   └── preferencias.py   # CRUD de Preferencias
│   │
│   ├── services/              # Lógica de negocio
│   │   ├── auth_service.py   # Lógica de autenticación
│   │   ├── inspeccion_service.py # Lógica de inspecciones
│   │   ├── reporte_service.py    # Generación de reportes
│   │   └── file_service.py       # Manejo de archivos
│   │
│   ├── routers/               # Endpoints de la API
│   │   ├── __init__.py
│   │   ├── auth.py           # POST /auth/login, /auth/register
│   │   ├── usuarios.py       # CRUD /usuarios/*
│   │   ├── plantas.py        # CRUD /plantas/*
│   │   ├── navieras.py       # CRUD /navieras/*
│   │   ├── inspecciones.py   # CRUD /inspecciones/*
│   │   ├── fotos.py          # POST /fotos/upload
│   │   ├── reportes.py       # GET /reportes/*
│   │   └── dashboard.py      # GET /dashboard/stats
│   │
│   ├── utils/                 # Utilidades generales
│   │   ├── auth.py           # Helpers de autenticación
│   │   ├── files.py          # Manejo de archivos
│   │   ├── security.py       # Utilidades de seguridad
│   │   └── validators.py     # Validadores personalizados
│   │
│   ├── main.py                # Punto de entrada de la aplicación
│   └── __init__.py
│
├── scripts/                   # Scripts de utilidad
│   ├── create_admin.py       # Crear usuario administrador
│   └── create_users.py       # Crear usuarios de prueba
│
├── tests/                     # Tests automatizados
│   ├── conftest.py           # Configuración de pytest
│   ├── test_inspecciones.py  # Tests de inspecciones
│   └── test_plantas.py       # Tests de plantas
│
├── uploads/                   # Archivos subidos (gitignored)
│   ├── fotos/                # Fotos de inspecciones
│   └── firmas/               # Firmas digitales
│
├── .env                       # Variables de entorno (gitignored)
├── .env.example              # Plantilla de variables de entorno
├── requirements.txt          # Dependencias de Python
├── alembic.ini              # Configuración de Alembic
└── README.md                # Documentación del backend
```

---

## 🗄️ Modelos de Datos

### Usuario (`models/usuario.py`)

Representa los usuarios del sistema con diferentes roles.

```python
class Usuario(Base):
    __tablename__ = "usuarios"
    
    id_usuario: int          # PK
    nombre: str              # Nombre completo
    correo: str              # Email único
    password_hash: str       # Contraseña hasheada
    rol: str                 # 'inspector', 'supervisor', 'admin'
    activo: bool             # Estado del usuario
    fecha_creacion: datetime
    fecha_actualizacion: datetime
```

**Roles disponibles:**
- `inspector`: Crea y gestiona inspecciones
- `supervisor`: Visualiza y aprueba inspecciones
- `admin`: Acceso total al sistema

### Planta (`models/planta.py`)

Plantas frutícolas donde se realizan las inspecciones.

```python
class Planta(Base):
    __tablename__ = "plantas"
    
    id_planta: int           # PK
    nombre: str              # Nombre de la planta
    ubicacion: str           # Dirección o coordenadas
    codigo: str              # Código único
    activa: bool
    fecha_creacion: datetime
```

### Naviera (`models/naviera.py`)

Compañías navieras asociadas a los contenedores.

```python
class Naviera(Base):
    __tablename__ = "navieras"
    
    id_navieras: int         # PK
    nombre: str              # Nombre de la naviera
    codigo: str              # Código SCAC u otro
    contacto: str            # Información de contacto
    activa: bool
    fecha_creacion: datetime
```

### Inspección (`models/inspeccion.py`)

Registro de inspecciones de contenedores.

```python
class Inspeccion(Base):
    __tablename__ = "inspecciones"
    
    id_inspeccion: int       # PK
    numero_contenedor: str   # Número del contenedor
    id_planta: int           # FK → Planta
    id_naviera: int          # FK → Naviera
    id_usuario: int          # FK → Usuario (inspector)
    temperatura: float       # Temperatura registrada
    observaciones: text      # Notas adicionales
    estado: str              # 'pendiente', 'aprobada', 'rechazada'
    fecha_inspeccion: datetime
    fecha_creacion: datetime
    
    # Relaciones
    planta: Planta
    naviera: Naviera
    usuario: Usuario
    fotos: List[Foto]
    firma: Firma
```

### Foto (`models/foto.py`)

Fotografías asociadas a una inspección.

```python
class Foto(Base):
    __tablename__ = "fotos"
    
    id_foto: int             # PK
    id_inspeccion: int       # FK → Inspección
    ruta_archivo: str        # Path relativo en uploads/
    tipo: str                # 'exterior', 'interior', 'defecto'
    orden: int               # Orden de visualización
    fecha_subida: datetime
```

### Firma (`models/firma.py`)

Firma digital del inspector.

```python
class Firma(Base):
    __tablename__ = "firmas"
    
    id_firma: int            # PK
    id_inspeccion: int       # FK → Inspección (unique)
    ruta_archivo: str        # Path a imagen de firma
    fecha_firma: datetime
```

### Preferencias (`models/preferencias.py`)

Preferencias de usuario (tema, notificaciones, etc.)

```python
class Preferencias(Base):
    __tablename__ = "preferencias"
    
    id_preferencia: int      # PK
    id_usuario: int          # FK → Usuario (unique)
    tema: str                # 'light', 'dark'
    notificaciones: bool
    idioma: str
    configuracion_json: JSON
```

---

## 🌐 API Endpoints

### Autenticación (`/auth`)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/auth/login` | Login de usuario | No |
| POST | `/auth/register` | Registro de nuevo usuario | No |
| GET | `/auth/me` | Información del usuario actual | Sí |
| POST | `/auth/refresh` | Renovar token JWT | Sí |

**Ejemplo de Login:**
```json
POST /auth/login
{
  "correo": "inspector@empresa.com",
  "password": "password123"
}

Response 200:
{
  "access_token": "eyJhbGciOiJIUzI1...",
  "token_type": "bearer",
  "usuario": {
    "id_usuario": 1,
    "nombre": "Juan Pérez",
    "correo": "inspector@empresa.com",
    "rol": "inspector"
  }
}
```

### Usuarios (`/usuarios`)

| Método | Endpoint | Descripción | Permisos |
|--------|----------|-------------|----------|
| GET | `/usuarios` | Listar todos los usuarios | admin |
| GET | `/usuarios/{id}` | Obtener usuario por ID | admin, mismo usuario |
| POST | `/usuarios` | Crear nuevo usuario | admin |
| PUT | `/usuarios/{id}` | Actualizar usuario | admin, mismo usuario |
| DELETE | `/usuarios/{id}` | Eliminar usuario | admin |
| GET | `/usuarios/rol/{rol}` | Usuarios por rol | admin |

### Plantas (`/plantas`)

| Método | Endpoint | Descripción | Permisos |
|--------|----------|-------------|----------|
| GET | `/plantas` | Listar plantas activas | Todos |
| GET | `/plantas/{id}` | Obtener planta por ID | Todos |
| POST | `/plantas` | Crear nueva planta | admin, supervisor |
| PUT | `/plantas/{id}` | Actualizar planta | admin, supervisor |
| DELETE | `/plantas/{id}` | Desactivar planta | admin |

### Navieras (`/navieras`)

| Método | Endpoint | Descripción | Permisos |
|--------|----------|-------------|----------|
| GET | `/navieras` | Listar navieras activas | Todos |
| GET | `/navieras/{id}` | Obtener naviera por ID | Todos |
| POST | `/navieras` | Crear nueva naviera | admin, supervisor |
| PUT | `/navieras/{id}` | Actualizar naviera | admin, supervisor |
| DELETE | `/navieras/{id}` | Desactivar naviera | admin |

### Inspecciones (`/inspecciones`)

| Método | Endpoint | Descripción | Permisos |
|--------|----------|-------------|----------|
| GET | `/inspecciones` | Listar inspecciones | Todos |
| GET | `/inspecciones/{id}` | Detalle de inspección | Todos |
| POST | `/inspecciones` | Crear inspección | inspector+ |
| PUT | `/inspecciones/{id}` | Actualizar inspección | inspector (propias), admin |
| DELETE | `/inspecciones/{id}` | Eliminar inspección | admin |
| GET | `/inspecciones/usuario/{id}` | Inspecciones por usuario | inspector (propias), admin |
| PATCH | `/inspecciones/{id}/estado` | Cambiar estado | supervisor, admin |

**Ejemplo de Creación:**
```json
POST /inspecciones
{
  "numero_contenedor": "ABCD1234567",
  "id_planta": 1,
  "id_naviera": 2,
  "temperatura": -18.5,
  "observaciones": "Contenedor en buen estado",
  "estado": "pendiente"
}

Response 201:
{
  "id_inspeccion": 42,
  "numero_contenedor": "ABCD1234567",
  "planta": {"id_planta": 1, "nombre": "Planta Central"},
  "naviera": {"id_navieras": 2, "nombre": "Maersk"},
  "fecha_inspeccion": "2025-10-15T14:30:00Z",
  "estado": "pendiente"
}
```

### Fotos (`/fotos`)

| Método | Endpoint | Descripción | Permisos |
|--------|----------|-------------|----------|
| POST | `/fotos/upload` | Subir foto de inspección | inspector+ |
| GET | `/fotos/{id}` | Obtener foto por ID | Todos |
| DELETE | `/fotos/{id}` | Eliminar foto | inspector (propias), admin |
| GET | `/fotos/inspeccion/{id}` | Fotos de una inspección | Todos |

**Ejemplo de Upload:**
```
POST /fotos/upload
Content-Type: multipart/form-data

id_inspeccion: 42
tipo: exterior
archivo: [binary image data]

Response 201:
{
  "id_foto": 123,
  "id_inspeccion": 42,
  "ruta_archivo": "uploads/fotos/2025/10/15/abc123.jpg",
  "tipo": "exterior",
  "orden": 1,
  "fecha_subida": "2025-10-15T14:35:00Z"
}
```

### Dashboard (`/dashboard`)

| Método | Endpoint | Descripción | Permisos |
|--------|----------|-------------|----------|
| GET | `/dashboard/stats` | Estadísticas generales | Todos |
| GET | `/dashboard/ultimas-inspecciones` | Últimas 10 inspecciones | Todos |
| GET | `/dashboard/por-estado` | Distribución por estado | supervisor, admin |

**Ejemplo de Stats:**
```json
GET /dashboard/stats?fecha_inicio=2025-10-01&fecha_fin=2025-10-15

Response 200:
{
  "total_inspecciones": 247,
  "pendientes": 12,
  "aprobadas": 220,
  "rechazadas": 15,
  "por_planta": [
    {"nombre": "Planta Central", "count": 120},
    {"nombre": "Planta Norte", "count": 127}
  ],
  "por_naviera": [
    {"nombre": "Maersk", "count": 89},
    {"nombre": "MSC", "count": 158}
  ]
}
```

### Reportes (`/reportes`)

| Método | Endpoint | Descripción | Permisos |
|--------|----------|-------------|----------|
| GET | `/reportes/exportar` | Exportar datos a Excel/PDF | supervisor, admin |
| GET | `/reportes/graficos` | Datos para gráficos | Todos |
| POST | `/reportes/personalizado` | Reporte con filtros custom | supervisor, admin |

---

## 🔐 Seguridad y Autenticación

### Sistema de Autenticación

El sistema utiliza **JWT (JSON Web Tokens)** para autenticación sin estado:

1. **Login**: Usuario envía credenciales → Backend valida → Retorna JWT
2. **Requests**: Cliente incluye JWT en header `Authorization: Bearer <token>`
3. **Validación**: Backend verifica firma y expiración del token
4. **Refresh**: Token puede renovarse antes de expirar

### Hashing de Contraseñas

Las contraseñas se hashean con **Bcrypt** utilizando `passlib`:

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash
hashed = pwd_context.hash("password123")

# Verify
is_valid = pwd_context.verify("password123", hashed)
```

### Roles y Permisos

| Rol | Permisos |
|-----|----------|
| **inspector** | Crear inspecciones, ver propias inspecciones, subir fotos |
| **supervisor** | Todo de inspector + aprobar/rechazar inspecciones, ver reportes |
| **admin** | Acceso total: gestión de usuarios, plantas, navieras |

### CORS (Cross-Origin Resource Sharing)

El backend permite requests desde el frontend:

```python
# app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Variables de Entorno Sensibles

Las credenciales y secrets se almacenan en `.env`:

```env
# Base de datos
DATABASE_URL=mysql+pymysql://user:password@localhost/impeccioncontenedor

# JWT
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Uploads
UPLOAD_DIR=uploads/
MAX_FILE_SIZE=10485760  # 10MB
```

⚠️ **NUNCA** commitear el archivo `.env` al repositorio.

---

## 💾 Base de Datos

### Esquema de Relaciones

```
usuarios
   │
   ├─── inspecciones ──┬─── fotos
   │                   └─── firma
   │
   ├─── preferencias
   
plantas ──┬─── inspecciones
          
navieras ─┴─── inspecciones
```

### Migraciones con Alembic

Alembic maneja cambios en el schema de la BD:

```bash
# Crear migración
alembic revision --autogenerate -m "Descripción del cambio"

# Aplicar migraciones
alembic upgrade head

# Revertir última migración
alembic downgrade -1

# Ver historial
alembic history
```

### Conexión a la Base de Datos

**SQLAlchemy** gestiona la conexión:

```python
# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost/impeccioncontenedor"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Dependency para inyectar session en endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Índices y Optimización

La BD tiene índices en:
- `usuarios.correo` (UNIQUE)
- `inspecciones.numero_contenedor`
- `inspecciones.fecha_inspeccion`
- `inspecciones.estado`
- `fotos.id_inspeccion`

---

## 🛠️ Instalación y Configuración

### 1. Requisitos Previos

- Python 3.10 o superior
- MySQL 8.0 o superior
- pip (gestor de paquetes de Python)

### 2. Clonar Repositorio

```bash
git clone <repo-url>
cd backend
```

### 3. Crear Entorno Virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar Variables de Entorno

Copiar `.env.example` a `.env` y configurar:

```env
DATABASE_URL=mysql+pymysql://root:@localhost/impeccioncontenedor
SECRET_KEY=tu-clave-secreta-super-segura
DEBUG=True
```

### 6. Crear Base de Datos

```sql
CREATE DATABASE impeccioncontenedor CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 7. Aplicar Migraciones

```bash
alembic upgrade head
```

### 8. Crear Usuario Administrador

```bash
python scripts/create_admin.py
```

### 9. Iniciar Servidor de Desarrollo

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en: **http://localhost:8000**

Documentación interactiva: **http://localhost:8000/docs**

---

## 🧪 Testing

### Estructura de Tests

```
tests/
├── conftest.py              # Fixtures y configuración
├── test_inspecciones.py     # Tests de inspecciones
├── test_plantas.py          # Tests de plantas
├── test_usuarios.py         # Tests de usuarios
└── test_auth.py             # Tests de autenticación
```

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Tests específicos
pytest tests/test_inspecciones.py

# Con coverage
pytest --cov=app tests/

# Modo verbose
pytest -v
```

### Ejemplo de Test

```python
def test_crear_inspeccion(client, db_session, test_user_token):
    response = client.post(
        "/inspecciones",
        json={
            "numero_contenedor": "TEST123456",
            "id_planta": 1,
            "id_naviera": 1,
            "temperatura": -18.5,
            "observaciones": "Test",
            "estado": "pendiente"
        },
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["numero_contenedor"] == "TEST123456"
    assert data["estado"] == "pendiente"
```

---

## 📊 Logging y Monitoreo

El sistema registra todas las operaciones importantes:

```python
# app/utils/logging.py
import logging

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

# Ejemplo de uso
logger.info(f"Usuario {usuario.id_usuario} creó inspección {inspeccion.id_inspeccion}")
logger.error(f"Error al subir foto: {str(e)}")
```

Logs se almacenan en:
- Desarrollo: Consola
- Producción: `logs/app.log` (rotación diaria)

---

## 🚀 Despliegue en Producción

Ver el archivo `instruccion_despliegue-produccion.md` en la raíz del proyecto para instrucciones detalladas de despliegue en VPS.

### Checklist Pre-Producción

- [ ] Cambiar `SECRET_KEY` a valor aleatorio seguro
- [ ] Configurar `DEBUG=False`
- [ ] Usar base de datos de producción
- [ ] Configurar HTTPS/SSL
- [ ] Limitar CORS a dominio específico
- [ ] Configurar límites de rate limiting
- [ ] Implementar backups automáticos de BD
- [ ] Configurar monitoreo y alertas
- [ ] Revisar logs de errores
- [ ] Ejecutar todos los tests

---

## 📚 Referencias Adicionales

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

---

## 👥 Mantenimiento y Soporte

Para reportar bugs o solicitar funcionalidades, crear un issue en el repositorio del proyecto.

---

**Última actualización:** Octubre 2025  
**Versión del Backend:** 2.1.0
