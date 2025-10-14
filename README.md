# 🚢 Sistema de Inspección de Contenedores

Sistema completo de gestión de inspecciones de contenedores frutícolas con captura de fotos, firmas digitales y reportes en tiempo real.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.2.0-61DAFB?logo=react)](https://reactjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3.3-3178C6?logo=typescript)](https://www.typescriptlang.org)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql)](https://www.mysql.com)

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Requisitos](#-requisitos)
- [Instalación Rápida](#-instalación-rápida)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Uso](#-uso)
- [API Endpoints](#-api-endpoints)
- [Tecnologías](#-tecnologías)

---

## ✨ Características

### 🎯 Funcionalidades Principales

- ✅ **Gestión de Inspecciones**: Crear, editar, aprobar y rechazar inspecciones
- 📸 **Captura de Fotos**: Captura múltiple de imágenes con cámara del dispositivo
- ✍️ **Firma Digital**: Canvas HTML5 para captura de firmas (mouse y touch)
- 📊 **Dashboard en Tiempo Real**: KPIs y estadísticas actualizadas automáticamente
- 🔍 **Búsqueda y Filtros**: Filtrado por estado, fecha y número de contenedor
- 📈 **Reportes**: Estadísticas con gráficos y exportación a CSV
- 👥 **Gestión de Usuarios**: Roles (Inspector, Supervisor, Admin)
- 🏭 **Catálogos**: Administración de Plantas y Navieras
- 🔔 **Notificaciones**: Sistema de toasts para feedback visual
- 🗄️ **Almacenamiento**: Archivos en filesystem (no en base de datos)

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React + Vite)                   │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │ Dashboard  │  │ Inspecciones│  │  Reportes  │            │
│  └────────────┘  └────────────┘  └────────────┘            │
└─────────────────────────────────────────────────────────────┘
                            │
                    ┌───────▼────────┐
                    │   API REST     │
                    │  (FastAPI)     │
                    └───────┬────────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
    ┌─────▼─────┐    ┌─────▼─────┐    ┌─────▼─────┐
    │   MySQL   │    │Filesystem │    │  Static   │
    │ Database  │    │ (capturas)│    │   Files   │
    └───────────┘    └───────────┘    └───────────┘
```

---

## 📦 Requisitos

| Software | Versión Mínima | Propósito |
|----------|----------------|-----------|
| **Python** | 3.10+ | Backend FastAPI |
| **Node.js** | 18.0+ | Frontend React |
| **MySQL** | 8.0+ | Base de datos |
| **XAMPP** | 8.0+ | Servidor MySQL local |

### Verificación Rápida

```powershell
python --version  # Debe mostrar 3.10 o superior
node --version   # Debe mostrar v18.0 o superior
npm --version    # Debe mostrar 9.0 o superior
```

---

## 🚀 Instalación Rápida

### Opción 1: Script Automático (Recomendado)

```powershell
# 1. Clonar o descargar el proyecto
cd "C:\ruta\al\proyecto\Planta-"

# 2. Ejecutar script de instalación
.\install.ps1

# 3. Configurar base de datos
.\setup-database.ps1

# 4. Iniciar servicios
.\start-dev.ps1
```

### 🌐 Acceder a la Aplicación

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

---

## 📂 Estructura del Proyecto

```
Planta-/
├── backend/                    # Backend FastAPI
│   ├── app/
│   │   ├── core/              # Configuración y BD
│   │   ├── models/            # Modelos SQLAlchemy
│   │   ├── schemas/           # Schemas Pydantic
│   │   ├── repositories/      # Repositorios (acceso a datos)
│   │   ├── services/          # Lógica de negocio
│   │   ├── routers/           # Endpoints API
│   │   ├── utils/             # Utilidades
│   │   └── main.py            # Aplicación principal
│   ├── alembic/               # Migraciones de BD
│   ├── venv/                  # Entorno virtual Python
│   ├── .env                   # Variables de entorno
│   └── requirements.txt       # Dependencias Python
│
├── frontend/                   # Frontend React + Vite
│   ├── src/
│   │   ├── components/        # Componentes reutilizables
│   │   ├── pages/             # Páginas principales
│   │   ├── services/          # API clients
│   │   ├── store/             # Estado global (Zustand)
│   │   ├── types/             # Tipos TypeScript
│   │   └── utils/             # Utilidades
│   ├── package.json           # Dependencias frontend
│   └── vite.config.ts         # Config Vite
│
├── capturas/                   # Almacenamiento de archivos
│   ├── inspecciones/          # Fotos de inspecciones
│   └── firmas/                # Firmas digitales
│
├── impeccioncontenedor.sql    # Schema y datos iniciales
├── install.ps1                # Script de instalación
├── setup-database.ps1         # Script de configuración de BD
├── start-dev.ps1              # Script para iniciar servicios
├── TUTORIAL.md                # Tutorial paso a paso
└── README.md                  # Este archivo
```

---

## 🎯 Uso

### 1️⃣ Crear una Inspección

1. Acceder a **Nueva Inspección** en el menú lateral
2. Seleccionar **Planta** y **Naviera**
3. Ingresar **Número de Contenedor**
4. Ingresar **Temperatura** (opcional)
5. **Capturar Fotos** con la cámara
6. **Firmar** en el canvas
7. Hacer clic en **Guardar Inspección**

### 2️⃣ Ver Dashboard

Acceder a **Dashboard** para ver KPIs en tiempo real:
- Total de inspecciones
- Pendientes, Aprobadas, Rechazadas
- Tasa de aprobación
- Inspecciones recientes

### 3️⃣ Gestionar Inspecciones

1. Ir a **Inspecciones**
2. Filtrar por estado o buscar por número de contenedor
3. Ver detalles y cambiar estado

---

## 🔌 API Endpoints

### Inspecciones
```
GET/POST   /api/inspecciones/
GET/PUT/DELETE /api/inspecciones/{id}
POST       /api/inspecciones/{id}/subir-fotos
POST       /api/inspecciones/{id}/subir-firma
```

### Reportes
```
GET    /api/reportes/conteo-estado
GET    /api/reportes/resumen
GET    /api/reportes/exportar-csv
```

### Catálogos
```
GET/POST   /api/plantas/
GET/POST   /api/navieras/
GET/POST   /api/usuarios/
```

**Documentación Completa**: http://localhost:8000/docs

---

## 🛠️ Tecnologías

### Backend
- **FastAPI** 0.109.0 - Framework web
- **SQLAlchemy** 2.0.25 - ORM
- **Pydantic** 2.5.3 - Validación
- **MySQL** 8.0+ - Base de datos

### Frontend
- **React** 18.2.0 - Biblioteca UI
- **TypeScript** 5.3.3 - Tipado estático
- **Vite** 5.0.11 - Build tool
- **TailwindCSS** 3.4.1 - CSS Framework
- **Zustand** 4.5.0 - Estado global

---

## 🐛 Solución de Problemas

### Backend no inicia
```powershell
# Verificar MySQL en XAMPP
# Activar entorno virtual
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Frontend no inicia
```powershell
cd frontend
npm install
npm run dev
```

### Error de conexión a BD
```powershell
# Verificar que MySQL esté corriendo en XAMPP
# Verificar credenciales en backend/.env
```

---

## 📚 Scripts Disponibles

```powershell
.\install.ps1           # Instala todas las dependencias
.\setup-database.ps1    # Configura la base de datos
.\start-dev.ps1        # Inicia backend y frontend
```

---

## 📞 Soporte

Para soporte técnico o preguntas:
- **Documentación API**: http://localhost:8000/docs
- **Tutorial completo**: Ver [TUTORIAL.md](TUTORIAL.md)

---

**🚀 ¡Listo para usar!** Sigue el [TUTORIAL.md](TUTORIAL.md) para una guía paso a paso detallada.
