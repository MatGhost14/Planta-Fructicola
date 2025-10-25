# 🚢 Sistema de Inspección de Contenedores Frutícolas

Sistema completo de gestión de inspecciones con autenticación JWT, control de permisos por roles, captura de fotos, firmas digitales y reportes en tiempo real.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.2.0-61DAFB?logo=react)](https://reactjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3.3-3178C6?logo=typescript)](https://www.typescriptlang.org)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql)](https://www.mysql.com)
[![Docker](https://img.shields.io/badge/Docker-4.0+-2496ED?logo=docker)](https://www.docker.com)

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Roles y Permisos](#-roles-y-permisos)
- [Instalación](#-instalación)
- [Inicio Rápido](#-inicio-rápido)
- [Credenciales de Prueba](#-credenciales-de-prueba)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Tecnologías](#-tecnologías)
- [Solución de Problemas](#-solución-de-problemas)
- [Mantenimiento](#-mantenimiento)

---

## ✨ Características

### 🔐 Sistema de Autenticación
- ✅ **Login con JWT**: Tokens con expiración de 8 horas
- ✅ **Contraseñas encriptadas**: bcrypt con 12 rounds
- ✅ **Control de sesiones**: localStorage con interceptores axios
- ✅ **Protección de rutas**: HOC ProtectedRoute por rol
- ✅ **Auditoría**: Registro de login/logout en bitácora

### 👥 Gestión por Roles
- **Inspector**: CRUD de inspecciones propias, subir fotos, firmar
- **Supervisor**: Gestión completa de planta, aprobar/rechazar
- **Admin**: Acceso total, gestión de usuarios y sistema

### 📸 Inspecciones
- ✅ **Modal de detalle**: Galería de fotos con lightbox
- ✅ **Captura múltiple**: Soporte para múltiples fotos
- ✅ **Firma digital**: Canvas HTML5 (mouse y touch)
- ✅ **Estados**: Pending, Approved, Rejected
- ✅ **Filtros avanzados**: Por estado, fecha, planta, contenedor

### 📊 Dashboard
- ✅ **KPIs en tiempo real**: Contadores por estado
- ✅ **Gráficos**: Visualización de estadísticas
- ✅ **Reportes**: Filtros personalizados
- ✅ **Notificaciones**: Sistema de mensajes modales centrados

### 🎨 Sistema de Notificaciones
- ✅ **Popups Modales**: Mensajes centrados en pantalla
- ✅ **No Auto-Cierre**: Requieren interacción del usuario
- ✅ **Múltiples Opciones de Cierre**: Botón "Aceptar", clic fuera, o tecla ESC
- ✅ **Sistema de Cola**: Un mensaje a la vez, con indicador de pendientes
- ✅ **Tema Oscuro**: Soporte completo para tema claro/oscuro
- ✅ **4 Tipos**: Éxito (verde), Error (rojo), Advertencia (amarillo), Info (azul)

### 🐳 Docker & Contenedores
- ✅ **Docker Compose**: Orquestación completa de servicios
- ✅ **Base de datos MySQL**: Contenedor con datos de prueba
- ✅ **Backend FastAPI**: Contenedor con dependencias Python
- ✅ **Frontend React**: Contenedor con build optimizado
- ✅ **CORS configurado**: Comunicación entre contenedores
- ✅ **Volúmenes persistentes**: Datos y archivos subidos

---

## 🔑 Roles y Permisos

### Inspector (Nivel 1)
| Módulo | Ver | Crear | Editar | Eliminar |
|--------|-----|-------|--------|----------|
| Mis Inspecciones | ✅ | ✅ | ✅ | ❌ |
| Otras Inspecciones | ❌ | ❌ | ❌ | ❌ |
| Subir Fotos | ✅ | ✅ | ❌ | ❌ |
| Cambiar Estado | ❌ | ❌ | ❌ | ❌ |

### Supervisor (Nivel 2)
| Módulo | Ver | Crear | Editar | Eliminar |
|--------|-----|-------|--------|----------|
| Todas las Inspecciones | ✅ | ✅ | ✅ | ✅ |
| Aprobar/Rechazar | ✅ | ✅ | ✅ | ✅ |
| Catálogos | ✅ | ✅ | ✅ | ✅ |

### Admin (Nivel 3)
- ✅ **Acceso total** sin restricciones

---

## 🚀 Instalación

### Requisitos Previos

**Opción 1: Instalación Tradicional**

| Software | Versión | Descarga |
|----------|---------|----------|
| Python | 3.10+ | [python.org](https://python.org) |
| Node.js | 18.0+ | [nodejs.org](https://nodejs.org) |
| MySQL | 8.0+ | XAMPP recomendado |

**Opción 2: Docker (Recomendado para Colaboradores)**

| Software | Versión | Descarga |
|----------|---------|----------|
| Docker Desktop | 4.0+ | [docker.com](https://www.docker.com/products/docker-desktop/) |

### Instalación Automática

**Opción 1: Docker (Recomendado)**
```cmd
# 1. Navegar al directorio del proyecto
cd "C:\Users\HP\Desktop\Planta-Fruticola"

# 2. Ejecutar con Docker
.\start-docker.bat
```

**Opción 2: Docker Compose Manual**
```cmd
# 1. Navegar al directorio del proyecto
cd "C:\Users\HP\Desktop\Planta-Fruticola"

# 2. Iniciar todos los servicios
docker-compose up -d

# 3. Ver logs en tiempo real
docker-compose logs -f
```

**Docker automáticamente:**
- ✅ Instala todas las dependencias
- ✅ Configura MySQL en contenedor
- ✅ Inicia backend (FastAPI) en puerto 8000
- ✅ Inicia frontend (React) en puerto 5173
- ✅ Configura CORS correctamente
- ✅ Sin problemas de dependencias

---

## ⚡ Inicio Rápido

### 1. Iniciar Servicios

**Opción A: Docker (Recomendado)**
```cmd
# Desde el directorio raíz del proyecto
.\start-docker.bat
```

**Opción B: Docker Compose Manual**
```cmd
# Desde el directorio raíz del proyecto
docker-compose up -d
```

### 2. Acceder a la Aplicación

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **Frontend** | http://localhost:5173 | Interfaz de usuario |
| **API** | http://localhost:8000 | Backend FastAPI |
| **API Docs** | http://localhost:8000/docs | Documentación interactiva |

### 3. Login

```
Inspector:
📧 juan.diaz@empresa.com
🔑 123456

Supervisor:
📧 maria.lopez@empresa.com
🔑 123456

Admin:
📧 carlos.ruiz@empresa.com
🔑 123456
```

---

## 🎯 Credenciales de Prueba

| Rol | Email | Password |
|-----|-------|----------|
| **Inspector** | juan.diaz@empresa.com | 123456 |
| **Supervisor** | maria.lopez@empresa.com | 123456 |
| **Admin** | carlos.ruiz@empresa.com | 123456 |

> ⚠️ **IMPORTANTE**: Cambia estas contraseñas en producción

---

## 📁 Estructura del Proyecto

```
Planta-Fruticola/
├── backend/                    # Backend FastAPI
│   ├── app/
│   │   ├── core/              # Configuración central
│   │   ├── routers/           # Endpoints con permisos
│   │   ├── models/            # Modelos SQLAlchemy
│   │   ├── schemas/           # Schemas Pydantic
│   │   ├── services/          # Lógica de negocio
│   │   ├── repositories/      # Acceso a datos
│   │   ├── middleware/        # Middleware personalizado
│   │   ├── utils/             # Utilidades
│   │   └── main.py
│   ├── alembic/               # Migraciones de BD
│   ├── scripts/               # Scripts de administración
│   ├── tests/                 # Tests unitarios
│   ├── Dockerfile
│   ├── requirements.txt
│   └── wait_for_db.py
│
├── frontend/                   # Frontend React
│   ├── src/
│   │   ├── api/               # Servicios API
│   │   ├── components/        # Componentes reutilizables
│   │   ├── contexts/          # Contextos React
│   │   ├── pages/             # Páginas principales
│   │   ├── store/             # Estado global (Zustand)
│   │   ├── types/             # Definiciones TypeScript
│   │   └── utils/             # Utilidades
│   ├── Dockerfile
│   └── package.json
│
├── capturas/                   # Archivos subidos
│   ├── inspecciones/          # Fotos de inspecciones
│   └── firmas/                # Firmas digitales
├── database/
│   └── inspeccioncontenedor.sql # Schema de BD
├── docker-compose.yml          # Orquestación Docker
├── start-docker.bat           # Script de inicio Docker
├── stop-docker.bat            # Script de parada Docker
├── docker-logs.bat            # Script para ver logs
└── README.md
```

---

## 🛠️ Tecnologías

### Backend
- **FastAPI** - Framework web
- **SQLAlchemy** - ORM
- **python-jose** - JWT
- **bcrypt** - Encriptación

### Frontend
- **React 18** - UI library
- **TypeScript** - Tipado
- **TailwindCSS** - Estilos
- **Axios** - HTTP client
- **Lucide React** - Iconos
- **Zustand** - State management
- **React Router** - Navegación

---

## 📚 API Endpoints

### Autenticación
```http
POST   /api/auth/login           # Login
GET    /api/auth/me              # Info sesión
POST   /api/auth/logout          # Logout
POST   /api/auth/change-password # Cambiar password
```

### Inspecciones (Autenticado)
```http
GET    /api/inspecciones         # Listar (filtrado por rol)
GET    /api/inspecciones/{id}    # Detalle
POST   /api/inspecciones         # Crear
PUT    /api/inspecciones/{id}    # Actualizar
DELETE /api/inspecciones/{id}    # Eliminar
POST   /api/inspecciones/{id}/fotos  # Subir fotos
```

**Documentación interactiva**: http://localhost:8000/docs

---

## 🔒 Seguridad

- ✅ JWT Tokens (HS256, 8h expiración)
- ✅ Passwords bcrypt (12 rounds)
- ✅ CORS configurado
- ✅ Validación Pydantic
- ✅ Auditoría de acciones
- ✅ Protección SQL Injection
- ✅ Verificación de usuario activo

---

## 🔧 Solución de Problemas

### "Error al cargar catálogos" / CORS Policy Blocking
```cmd
# Verificar que los contenedores estén corriendo
docker ps

# Reiniciar el backend para aplicar configuración CORS
docker restart planta_backend

# Verificar logs del backend
docker logs planta_backend
```

### "No se pudo validar las credenciales"
Token expirado. Cierra sesión y vuelve a ingresar.

### "500 Internal Server Error" en /api/plantas
```cmd
# Verificar datos en la base de datos
docker exec planta-mysql mysql -u planta_user -pplanta_password inspeccioncontenedor -e "SELECT * FROM plantas;"

# Si hay registros con código vacío, corregirlos
docker exec planta-mysql mysql -u planta_user -pplanta_password inspeccioncontenedor -e "UPDATE plantas SET codigo = 'centro' WHERE codigo = '';"
```

### "Sin respuesta del servidor"
```cmd
# Verificar que todos los servicios estén corriendo
docker-compose ps

# Reiniciar todos los servicios
docker-compose restart

# Ver logs en tiempo real
docker-compose logs -f
```

### "Module not found" en desarrollo local
```powershell
# Backend
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm install
npm run dev -- --port 5173
```

---

## 📝 Archivos Principales

| Archivo | Descripción |
|---------|-------------|
| `start-docker.bat` | **Script principal Docker** - Inicio automático |
| `stop-docker.bat` | Script para detener servicios |
| `docker-logs.bat` | Script para ver logs en tiempo real |
| `docker-compose.yml` | Configuración de contenedores Docker |
| `README.md` | Documentación completa del proyecto |
| `backend/Dockerfile` | Configuración Docker para backend |
| `frontend/Dockerfile` | Configuración Docker para frontend |
| `database/inspeccioncontenedor.sql` | Schema de la base de datos |

---

## 🛠️ Mantenimiento

### Comandos Docker Útiles

```cmd
# Ver estado de contenedores
docker ps

# Ver logs de un servicio específico
docker logs planta_backend
docker logs planta_frontend
docker logs planta-mysql

# Reiniciar un servicio
docker restart planta_backend

# Detener todos los servicios
docker-compose down

# Limpiar contenedores no utilizados
docker system prune -f

# Ver logs en tiempo real
docker-compose logs -f
```

### Backup de Base de Datos

```cmd
# Crear backup
docker exec planta-mysql mysqldump -u planta_user -pplanta_password inspeccioncontenedor > backup.sql

# Restaurar backup
docker exec -i planta-mysql mysql -u planta_user -pplanta_password inspeccioncontenedor < backup.sql
```

---

**Desarrollado con ❤️ usando FastAPI + React + Docker**

**Última actualización:** 25 de octubre de 2025
