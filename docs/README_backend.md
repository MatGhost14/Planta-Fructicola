# Backend - Sistema de Inspección de Contenedores

## 📋 Descripción

Backend desarrollado en **FastAPI** para el sistema de inspección de contenedores frutícolas. Proporciona una API REST completa con autenticación JWT, gestión de usuarios, inspecciones, reportes y más.

## 🏗️ Arquitectura

```
backend/
├── app/
│   ├── core/           # Configuración central
│   ├── models/         # Modelos de base de datos
│   ├── routers/        # Endpoints de la API
│   ├── schemas/        # Esquemas Pydantic
│   ├── services/       # Lógica de negocio
│   ├── repositories/   # Acceso a datos
│   ├── middleware/     # Middleware personalizado
│   └── utils/          # Utilidades
├── alembic/            # Migraciones de BD
├── tests/              # Pruebas unitarias
└── scripts/            # Scripts de utilidad
```

## 🚀 Tecnologías

- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para Python
- **Alembic** - Migraciones de base de datos
- **Pydantic** - Validación de datos
- **JWT** - Autenticación con tokens
- **MySQL** - Base de datos principal
- **Pytest** - Testing framework

## 📦 Instalación

### Prerrequisitos

- Python 3.8+
- MySQL 5.7+ o MariaDB 10.3+
- XAMPP (recomendado para desarrollo)

### Configuración

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd Planta-/backend
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   ```

3. **Activar entorno virtual**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configurar base de datos**
   ```bash
   # Crear base de datos
   mysql -u root -e "CREATE DATABASE inspeccioncontenedor CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
   
   # Importar esquema
   mysql -u root inspeccioncontenedor < ../database/inspeccioncontenedor.sql
   ```

6. **Configurar variables de entorno**
   ```bash
   # Crear archivo .env
   cp .env.example .env
   # Editar .env con tus configuraciones
   ```

## ⚙️ Configuración

### Variables de Entorno

Crear archivo `.env` en la raíz del backend:

```env
# Base de datos
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=inspeccioncontenedor

# Seguridad
SECRET_KEY=tu-clave-secreta-super-segura-cambiar-en-produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480

# Entorno
DEBUG=True
ENVIRONMENT=development

# CORS
ALLOWED_ORIGINS=http://localhost:5173

# Uploads
CAPTURAS_DIR=../capturas
MAX_FILE_SIZE=10485760

# Servidor
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# Logging
LOG_LEVEL=INFO
LOG_FILE=app.log
```

## 🚀 Ejecución

### Desarrollo

```bash
# Activar entorno virtual
venv\Scripts\activate

# Ejecutar servidor
uvicorn app.main:app --reload --port 8000
```

### Producción

```bash
# Con Gunicorn (recomendado)
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Con Uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📚 API Documentation

Una vez iniciado el servidor, la documentación interactiva está disponible en:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Autenticación

El sistema utiliza **JWT (JSON Web Tokens)** para la autenticación:

### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "correo": "usuario@empresa.com",
  "password": "password123"
}
```

### Respuesta
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "usuario": {
    "id_usuario": 1,
    "correo": "usuario@empresa.com",
    "rol": "inspector",
    "nombre": "Usuario"
  },
  "expires_in": 28800
}
```

### Uso del Token
```http
GET /api/plantas
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## 🗄️ Base de Datos

### Modelos Principales

- **Usuarios**: Gestión de usuarios y autenticación
- **Plantas**: Ubicaciones de inspección
- **Navieras**: Compañías navieras
- **Inspecciones**: Registros de inspecciones
- **Fotos**: Imágenes de inspecciones
- **Bitácora**: Auditoría del sistema

### Migraciones

```bash
# Crear nueva migración
alembic revision --autogenerate -m "descripción del cambio"

# Aplicar migraciones
alembic upgrade head

# Revertir migración
alembic downgrade -1
```

## 🧪 Testing

```bash
# Ejecutar todas las pruebas
pytest

# Con cobertura
pytest --cov=app

# Pruebas específicas
pytest tests/test_inspecciones.py -v
```

## 📊 Endpoints Principales

### Autenticación
- `POST /api/auth/login` - Iniciar sesión
- `POST /api/auth/logout` - Cerrar sesión
- `GET /api/auth/me` - Información del usuario actual

### Catálogos
- `GET /api/plantas` - Listar plantas
- `GET /api/navieras` - Listar navieras

### Inspecciones
- `GET /api/inspecciones` - Listar inspecciones
- `POST /api/inspecciones` - Crear inspección
- `GET /api/inspecciones/{id}` - Obtener inspección
- `PUT /api/inspecciones/{id}` - Actualizar inspección

### Reportes
- `GET /api/reportes/estadisticas` - Estadísticas generales
- `GET /api/reportes/export/pdf` - Exportar PDF

## 🔧 Scripts de Utilidad

### Crear Usuarios
```bash
python scripts/create_users.py
```

### Crear Admin
```bash
python scripts/create_admin.py
```

## 🐛 Debugging

### Logs
Los logs se guardan en `logs/app.log` y incluyen:
- Requests HTTP
- Errores de aplicación
- Operaciones de base de datos

### Variables de Debug
```env
DEBUG=True
LOG_LEVEL=DEBUG
```

## 🚀 Despliegue

### Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Variables de Producción
```env
DEBUG=False
ENVIRONMENT=production
SECRET_KEY=clave-super-segura-de-produccion
DB_PASSWORD=password-seguro
```

## 📝 Notas de Desarrollo

### Estructura de Respuestas
```python
# Éxito
{
  "data": {...},
  "message": "Operación exitosa"
}

# Error
{
  "detail": "Descripción del error",
  "error_code": "ERROR_CODE"
}
```

### Manejo de Errores
- **400**: Bad Request - Datos inválidos
- **401**: Unauthorized - No autenticado
- **403**: Forbidden - Sin permisos
- **404**: Not Found - Recurso no encontrado
- **500**: Internal Server Error - Error del servidor

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

