# 🛠️ Guía para Desarrolladores - Sistema de Inspección de Contenedores

## 📖 Índice
1. [Introducción](#introducción)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Configuración del Entorno](#configuración-del-entorno)
5. [Convenciones de Código](#convenciones-de-código)
6. [Flujo de Trabajo](#flujo-de-trabajo)
7. [Testing](#testing)
8. [Deployment](#deployment)

---

## 🎯 Introducción

Bienvenido al Sistema de Inspección de Contenedores v2.1.0. Este documento está diseñado para nuevos desarrolladores que se unan al proyecto.

### Stack Tecnológico

**Backend:**
- Python 3.11+
- FastAPI (Web framework)
- SQLAlchemy (ORM)
- MySQL (Base de datos)
- Pydantic (Validación de datos)
- JWT (Autenticación)
- Slowapi (Rate limiting)

**Frontend:**
- React 18+ con TypeScript
- Vite (Build tool)
- TailwindCSS (Estilos)
- Recharts (Visualizaciones)
- Axios (Cliente HTTP)

---

## 🏗️ Arquitectura del Sistema

### Patrón Arquitectónico: MVC + Repository

```
┌─────────────────────────────────────────────────────────┐
│                      FRONTEND (React)                    │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐            │
│  │  Pages   │──>│Components│──>│  Hooks   │            │
│  └──────────┘   └──────────┘   └──────────┘            │
│        │              │              │                   │
│        └──────────────┴──────────────┘                   │
│                      │                                   │
│              ┌───────▼───────┐                          │
│              │   API Client  │                          │
│              │   (axios)     │                          │
└──────────────┴───────────────┴──────────────────────────┘
                       │
                       │ HTTP/REST
                       ▼
┌─────────────────────────────────────────────────────────┐
│                   BACKEND (FastAPI)                      │
│  ┌──────────────────────────────────────────────────┐  │
│  │ main.py (Aplicación principal)                   │  │
│  └─────────────────┬────────────────────────────────┘  │
│                    │                                    │
│    ┌───────────────┴────────────────┐                  │
│    │                                │                  │
│  ┌─▼───────┐   ┌─────────┐   ┌────▼──────┐           │
│  │ Routers │──>│ Services│──>│ Models    │           │
│  └─────────┘   └─────────┘   └───────────┘           │
│      │              │              │                   │
│      │              └──────────────┴───────┐           │
│      │                                     │           │
│  ┌───▼──────┐                      ┌──────▼─────┐    │
│  │ Schemas  │                      │  Database  │    │
│  │(Pydantic)│                      │ (SQLAlchemy)│    │
│  └──────────┘                      └────────────┘    │
└─────────────────────────────────────────────────────────┘
                       │
                       ▼
              ┌────────────────┐
              │  MySQL Database│
              └────────────────┘
```

### Flujo de una Petición

1. **Usuario** hace una acción en el frontend (ej: clic en "Guardar Inspección")
2. **Frontend** envía petición HTTP a través de `axios` (ej: `POST /api/inspecciones`)
3. **Middleware** de FastAPI procesa la petición:
   - `LoggingMiddleware`: Registra la petición
   - `CORSMiddleware`: Valida origen
   - `RateLimiter`: Verifica límites
4. **Router** recibe la petición (ej: `inspecciones_router`)
5. **Dependencies** se ejecutan:
   - `get_db()`: Proporciona sesión de BD
   - `get_current_active_user()`: Autentica usuario
6. **Función del endpoint** ejecuta lógica de negocio
7. **Service layer** (opcional): Lógica compleja
8. **Models** (SQLAlchemy): Interacción con BD
9. **Schemas** (Pydantic): Validación de datos
10. **Response** se envía al frontend
11. **Frontend** actualiza UI con los datos

---

## 📁 Estructura del Proyecto

```
Planta-/
├── backend/                          # Backend FastAPI
│   ├── app/
│   │   ├── core/                     # Configuración central
│   │   │   ├── settings.py           # ⭐ Variables de entorno
│   │   │   ├── logging.py            # ⭐ Sistema de logs
│   │   │   └── database.py           # ⭐ Conexión BD
│   │   ├── middleware/               # Middlewares personalizados
│   │   │   ├── logging_middleware.py # Logging HTTP + Seguridad
│   │   │   └── __init__.py
│   │   ├── models/                   # Modelos SQLAlchemy (ORM)
│   │   │   ├── usuario.py
│   │   │   ├── inspeccion.py
│   │   │   ├── planta.py
│   │   │   └── ...
│   │   ├── routers/                  # Endpoints API
│   │   │   ├── auth.py               # ⭐ Autenticación
│   │   │   ├── inspecciones.py       # ⭐ CRUD Inspecciones
│   │   │   ├── estadisticas.py       # Dashboard
│   │   │   ├── reportes_export.py    # PDF/Excel
│   │   │   └── ...
│   │   ├── schemas/                  # Validación Pydantic
│   │   │   ├── auth.py
│   │   │   ├── inspeccion.py
│   │   │   └── ...
│   │   ├── services/                 # Lógica de negocio compleja
│   │   │   └── inspecciones.py
│   │   ├── utils/                    # Utilidades
│   │   │   ├── auth.py               # JWT, hashing
│   │   │   └── __init__.py
│   │   └── main.py                   # ⭐ Punto de entrada
│   ├── scripts/                      # Scripts utilitarios
│   │   └── create_admin.py           # Crear admin
│   ├── logs/                         # Logs de la aplicación
│   ├── .env                          # ⚠️ Variables de entorno (NO commitear)
│   ├── .env.example                  # Template de .env
│   ├── requirements.txt              # Dependencias Python
│   └── alembic.ini                   # Migraciones de BD
│
├── frontend/                         # Frontend React
│   ├── src/
│   │   ├── api/                      # Clientes API
│   │   │   ├── axios.ts              # ⭐ Configuración Axios
│   │   │   ├── inspecciones.ts
│   │   │   ├── estadisticas.ts
│   │   │   └── index.ts
│   │   ├── components/               # Componentes reutilizables
│   │   │   ├── Layout.tsx            # Layout principal
│   │   │   ├── ProtectedRoute.tsx    # Protección de rutas
│   │   │   └── Toast.tsx             # Notificaciones
│   │   ├── contexts/                 # Context API
│   │   │   └── AuthContext.tsx       # ⭐ Contexto de autenticación
│   │   ├── pages/                    # Páginas/Vistas
│   │   │   ├── Login.tsx
│   │   │   ├── Dashboard.tsx         # ⭐ Estadísticas
│   │   │   ├── Inspecciones.tsx
│   │   │   ├── Reportes.tsx          # ⭐ PDF/Excel
│   │   │   └── ...
│   │   ├── types/                    # Tipos TypeScript
│   │   │   └── index.ts
│   │   ├── utils/                    # Utilidades
│   │   │   └── index.ts
│   │   ├── App.tsx                   # ⭐ Componente raíz
│   │   └── main.tsx                  # ⭐ Punto de entrada
│   ├── package.json                  # Dependencias npm
│   └── vite.config.ts                # Configuración Vite
│
├── scripts/                          # Scripts de sistema
│   └── backup-database.ps1           # Backup MySQL
├── docs/                             # Documentación
│   ├── SISTEMA-LISTO-PRODUCCION.md
│   └── ...
└── README.md                         # Documentación principal
```

### Archivos Clave 🔑

| Archivo | Descripción | Cuándo modificar |
|---------|-------------|------------------|
| `backend/app/main.py` | Inicialización de FastAPI, registro de routers | Agregar nuevo router o middleware |
| `backend/app/core/settings.py` | Variables de entorno | Agregar nueva configuración |
| `backend/app/core/database.py` | Conexión a BD | Cambiar configuración de pool |
| `backend/app/routers/auth.py` | Autenticación JWT | Modificar proceso de login |
| `frontend/src/api/axios.ts` | Cliente HTTP | Cambiar URL base o interceptores |
| `frontend/src/contexts/AuthContext.tsx` | Estado de autenticación | Modificar lógica de sesión |

---

## ⚙️ Configuración del Entorno

### 1. Requisitos Previos

- **Python:** 3.11 o superior
- **Node.js:** 18 o superior
- **MySQL:** 8.0 o superior
- **Git:** Para control de versiones

### 2. Clonar el Repositorio

```bash
git clone https://github.com/Balternology/Planta-Fruticola.git
cd Planta-Fruticola
```

### 3. Configurar Backend

```bash
# Navegar al backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
.\venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Copiar archivo de configuración
cp .env.example .env

# ⚠️ EDITAR .env con tus credenciales
# - DATABASE_URL
# - SECRET_KEY (usar valor único)
# - ALLOWED_ORIGINS

# Ejecutar migraciones de BD
alembic upgrade head

# Crear usuario administrador
python scripts/create_admin.py
```

### 4. Configurar Frontend

```bash
# Navegar al frontend (desde raíz del proyecto)
cd frontend

# Instalar dependencias
npm install

# Copiar archivo de configuración (si existe)
cp .env.example .env  # Opcional

# El frontend usa VITE_API_URL, por defecto: http://localhost:8000
```

### 5. Ejecutar el Proyecto

**Terminal 1 - Backend:**
```bash
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Acceder a:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Documentación API: http://localhost:8000/docs

---

## 📐 Convenciones de Código

### Python (Backend)

#### Nomenclatura

```python
# Variables y funciones: snake_case
nombre_usuario = "Juan"
def obtener_inspecciones():
    pass

# Clases: PascalCase
class Usuario:
    pass

# Constantes: UPPER_CASE
MAX_FILE_SIZE = 10485760

# Privado: prefijo _
def _funcion_interna():
    pass
```

#### Estructura de Archivos

```python
"""
Descripción breve del módulo
=============================
Descripción detallada de qué hace este archivo

Autor: Sistema de Inspección
Versión: 2.1.0
"""

# 1. Imports estándar
import os
from datetime import datetime

# 2. Imports de terceros
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# 3. Imports locales
from ..core.database import get_db
from ..models import Usuario

# 4. Configuración
router = APIRouter()

# 5. Funciones/Clases
```

#### Documentación de Funciones

```python
def crear_inspeccion(data: InspeccionCreate, db: Session):
    """
    Crea una nueva inspección en la base de datos
    
    Este función valida los datos, crea el registro en BD
    y envía notificaciones si es necesario.
    
    Args:
        data: Datos de la inspección a crear
        db: Sesión de base de datos
        
    Returns:
        Inspeccion: Objeto de inspección creado
        
    Raises:
        HTTPException 400: Datos inválidos
        HTTPException 404: Planta no existe
        
    Example:
        >>> data = InspeccionCreate(numero_contenedor="ABC123")
        >>> inspeccion = crear_inspeccion(data, db)
    """
    pass
```

### TypeScript/React (Frontend)

#### Nomenclatura

```typescript
// Variables y funciones: camelCase
const nombreUsuario = "Juan";
function obtenerInspecciones() {}

// Componentes: PascalCase
function Dashboard() {}

// Tipos e Interfaces: PascalCase
interface Usuario {
  id: number;
  nombre: string;
}

// Constantes: UPPER_CASE
const MAX_FILE_SIZE = 10485760;

// Hooks personalizados: prefijo use
function useAuth() {}
```

#### Estructura de Componentes

```typescript
/**
 * Dashboard - Vista principal de estadísticas
 * 
 * Muestra KPIs, gráficos y tablas con datos de inspecciones.
 * Requiere autenticación.
 */

// 1. Imports de React
import React, { useState, useEffect } from 'react';

// 2. Imports de librerías
import { PieChart, Pie } from 'recharts';

// 3. Imports locales
import { estadisticasApi } from '../api';
import type { DashboardData } from '../api/estadisticas';

// 4. Tipos locales
interface Props {
  userId: number;
}

// 5. Componente
const Dashboard: React.FC<Props> = ({ userId }) => {
  // Estados
  const [data, setData] = useState<DashboardData | null>(null);
  
  // Efectos
  useEffect(() => {
    cargarDatos();
  }, []);
  
  // Funciones
  const cargarDatos = async () => {
    // ...
  };
  
  // Renderizado
  return (
    <div>
      {/* ... */}
    </div>
  );
};

export default Dashboard;
```

### Git Commits

Usar convención de commits semánticos:

```bash
# Formato: <tipo>(<alcance>): <descripción>

# Tipos:
feat:     # Nueva funcionalidad
fix:      # Corrección de bug
docs:     # Cambios en documentación
style:    # Cambios de formato (no afectan lógica)
refactor: # Refactorización de código
test:     # Agregar o modificar tests
chore:    # Tareas de mantenimiento

# Ejemplos:
git commit -m "feat(inspecciones): agregar filtro por fecha"
git commit -m "fix(auth): corregir validación de token expirado"
git commit -m "docs(readme): actualizar guía de instalación"
```

---

## 🔄 Flujo de Trabajo

### 1. Crear Nueva Funcionalidad

#### Backend

1. **Crear modelo** (si es necesario): `backend/app/models/nuevo_modelo.py`
2. **Crear schema**: `backend/app/schemas/nuevo_schema.py`
3. **Crear router**: `backend/app/routers/nuevo_router.py`
4. **Registrar router** en `main.py`:
   ```python
   from .routers import nuevo_router
   app.include_router(nuevo_router, prefix="/api")
   ```
5. **Probar** en http://localhost:8000/docs

#### Frontend

1. **Crear servicio API**: `frontend/src/api/nuevo_servicio.ts`
2. **Exportar** en `frontend/src/api/index.ts`
3. **Crear página/componente**: `frontend/src/pages/NuevaPagina.tsx`
4. **Agregar ruta** en `App.tsx`
5. **Agregar menú** en `Layout.tsx` (si aplica)

### 2. Testing

#### Backend (pytest)

```bash
cd backend
pytest tests/  # Todos los tests
pytest tests/test_inspecciones.py  # Un archivo
pytest -v  # Verbose
pytest --cov  # Con cobertura
```

#### Frontend (Vitest)

```bash
cd frontend
npm run test  # Todos los tests
npm run test:ui  # UI interactiva
npm run test:coverage  # Con cobertura
```

### 3. Deployment

Ver documentación completa en `docs/SISTEMA-LISTO-PRODUCCION.md`

---

## 🐛 Debugging

### Backend

```python
# Agregar breakpoint
import pdb; pdb.set_trace()

# O usar debugger de VS Code
# 1. Crear .vscode/launch.json
# 2. Configurar Python Debugger
# 3. Poner breakpoints (F9)
# 4. Iniciar debug (F5)
```

### Frontend

```typescript
// Console logs
console.log('Variable:', variable);

// Debugger
debugger;  // Pausa ejecución si DevTools abierto

// React DevTools (extensión de navegador)
// 1. Instalar React Developer Tools
// 2. Abrir DevTools > Components/Profiler
```

### Logs del Sistema

```bash
# Backend logs
tail -f backend/logs/app.log

# Frontend logs
# Ver consola del navegador (F12)
```

---

## 📚 Recursos Adicionales

### Documentación Oficial

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [React](https://react.dev/)
- [TypeScript](https://www.typescriptlang.org/docs/)
- [Recharts](https://recharts.org/)

### Documentación Interna

- `docs/SISTEMA-LISTO-PRODUCCION.md` - Guía de producción
- `docs/RESUMEN-SEGURIDAD.md` - Implementaciones de seguridad
- `ESTRUCTURA.md` - Estructura detallada del proyecto

---

## 🤝 Contribuir

1. **Fork** del repositorio
2. Crear **branch** de feature: `git checkout -b feature/nueva-funcionalidad`
3. **Commits** siguiendo convención semántica
4. **Push** al branch: `git push origin feature/nueva-funcionalidad`
5. Crear **Pull Request** con descripción detallada

---

## 📧 Contacto

Para preguntas o soporte:
- Email: soporte@sistema-inspeccion.com
- Slack: #desarrollo-planta-fruticola

---

**¡Feliz coding! 🚀**
