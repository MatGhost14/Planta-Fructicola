# 🚢 Sistema de Inspección de Contenedores Frutícolas

Sistema completo de gestión de inspecciones con autenticación JWT, control de permisos por roles, captura de fotos, firmas digitales y reportes en tiempo real.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.2.0-61DAFB?logo=react)](https://reactjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3.3-3178C6?logo=typescript)](https://www.typescriptlang.org)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql)](https://www.mysql.com)

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Roles y Permisos](#-roles-y-permisos)
- [Instalación](#-instalación)
- [Inicio Rápido](#-inicio-rápido)
- [Credenciales de Prueba](#-credenciales-de-prueba)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Tecnologías](#-tecnologías)

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
- ✅ **Notificaciones**: Sistema de toasts

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

| Software | Versión | Descarga |
|----------|---------|----------|
| Python | 3.10+ | [python.org](https://python.org) |
| Node.js | 18.0+ | [nodejs.org](https://nodejs.org) |
| MySQL | 8.0+ | XAMPP recomendado |

### Instalación Automática

```powershell
# 1. Clonar repositorio
cd "ruta\al\proyecto"

# 2. Instalar dependencias
.\install.ps1

# 3. Configurar base de datos
.\setup-database.ps1

# 4. Iniciar servicios
.\start-dev.ps1
```

---

## ⚡ Inicio Rápido

### 1. Iniciar Servicios

```powershell
.\start-dev.ps1
```

### 2. Acceder a la Aplicación

| Servicio | URL |
|----------|-----|
| **Frontend** | http://localhost:5173 |
| **API** | http://localhost:8000 |
| **API Docs** | http://localhost:8000/docs |

### 3. Login

```
Inspector:
📧 inspector@empresa.com
🔑 password123

Supervisor:
📧 supervisor@empresa.com
🔑 password123

Admin:
📧 admin@empresa.com
🔑 password123
```

---

## 🎯 Credenciales de Prueba

| Rol | Email | Password |
|-----|-------|----------|
| **Inspector** | inspector@empresa.com | password123 |
| **Supervisor** | supervisor@empresa.com | password123 |
| **Admin** | admin@empresa.com | password123 |

> ⚠️ **IMPORTANTE**: Cambia estas contraseñas en producción

---

## 📁 Estructura del Proyecto

```
Planta-Fruticola/
├── backend/                    # Backend FastAPI
│   ├── app/
│   │   ├── routers/           # Endpoints con permisos
│   │   ├── models/            # Modelos SQLAlchemy
│   │   ├── schemas/           # Schemas Pydantic
│   │   ├── services/          # Lógica de negocio
│   │   ├── utils/
│   │   │   └── auth.py        # JWT, bcrypt, decoradores
│   │   └── main.py
│   └── requirements.txt
│
├── frontend/                   # Frontend React
│   ├── src/
│   │   ├── api/
│   │   │   ├── auth.ts        # AuthService
│   │   │   └── axios.ts       # Interceptor
│   │   ├── components/
│   │   │   ├── InspeccionModal.tsx
│   │   │   └── ProtectedRoute.tsx
│   │   ├── contexts/
│   │   │   └── AuthContext.tsx
│   │   └── pages/
│   │       └── Login.tsx
│   └── package.json
│
├── capturas/                   # Archivos subidos
├── impeccioncontenedor.sql     # Schema de BD
├── start-dev.ps1              # Script de inicio
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

## 🐛 Troubleshooting

### "No se pudo validar las credenciales"
Token expirado. Cierra sesión y vuelve a ingresar.

### "CORS policy blocking"
Verifica puertos: Backend 8000, Frontend 5173.

### "Module not found: jose"
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install python-jose[cryptography]==3.3.0
```

---

## 📝 Scripts

| Script | Descripción |
|--------|-------------|
| `install.ps1` | Instalación completa |
| `setup-database.ps1` | Setup BD |
| `start-dev.ps1` | Inicia servicios |

---

**Desarrollado con ❤️ usando FastAPI + React**

**Última actualización:** 14 de octubre de 2025
