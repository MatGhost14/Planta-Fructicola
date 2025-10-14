# 📁 Estructura del Proyecto

```
Planta-Fruticola/
│
├── 📂 backend/                    # Backend FastAPI
│   ├── 📂 app/
│   │   ├── 📂 core/              # Configuración central
│   │   │   ├── database.py       # Conexión BD
│   │   │   ├── settings.py       # Configuraciones
│   │   │   └── security.py       # Seguridad
│   │   ├── 📂 models/            # Modelos SQLAlchemy
│   │   │   └── __init__.py
│   │   ├── 📂 routers/           # Endpoints API
│   │   │   ├── auth.py           # Autenticación
│   │   │   ├── inspecciones.py  # CRUD Inspecciones
│   │   │   ├── usuarios.py      # CRUD Usuarios (admin)
│   │   │   ├── plantas.py       # CRUD Plantas (supervisor)
│   │   │   └── navieras.py      # CRUD Navieras (supervisor)
│   │   ├── 📂 schemas/           # Pydantic schemas
│   │   │   └── __init__.py
│   │   ├── 📂 utils/             # Utilidades
│   │   │   ├── auth.py           # JWT, passwords
│   │   │   └── files.py          # Manejo de archivos
│   │   └── main.py               # Aplicación principal
│   ├── 📂 alembic/               # Migraciones BD
│   ├── 📂 tests/                 # Tests unitarios
│   ├── .env.example              # Ejemplo variables entorno
│   ├── .env                      # Variables entorno (no commitear)
│   ├── requirements.txt          # Dependencias Python
│   └── pytest.ini                # Configuración pytest
│
├── 📂 frontend/                   # Frontend React + TypeScript
│   ├── 📂 public/                # Assets estáticos
│   ├── 📂 src/
│   │   ├── 📂 api/               # Llamadas API
│   │   │   ├── auth.ts
│   │   │   ├── inspecciones.ts
│   │   │   ├── usuarios.ts
│   │   │   ├── plantas.ts
│   │   │   └── navieras.ts
│   │   ├── 📂 components/        # Componentes reutilizables
│   │   │   ├── Layout.tsx
│   │   │   ├── ProtectedRoute.tsx
│   │   │   ├── InspeccionModal.tsx
│   │   │   └── InspeccionForm.tsx
│   │   ├── 📂 pages/             # Páginas de la app
│   │   │   ├── Login.tsx
│   │   │   ├── Inspecciones.tsx
│   │   │   ├── Usuarios.tsx
│   │   │   ├── Plantas.tsx
│   │   │   └── Navieras.tsx
│   │   ├── 📂 types/             # TypeScript types
│   │   │   └── index.ts
│   │   ├── App.tsx               # Componente principal
│   │   └── main.tsx              # Entry point
│   ├── .env.example              # Ejemplo variables entorno
│   ├── package.json              # Dependencias Node
│   ├── tsconfig.json             # Config TypeScript
│   ├── vite.config.ts            # Config Vite
│   └── tailwind.config.js        # Config Tailwind CSS
│
├── 📂 database/                   # SQL y migraciones
│   └── impeccioncontenedor.sql   # Schema inicial
│
├── 📂 capturas/                   # Archivos subidos
│   ├── 📂 firmas/                # Firmas digitales
│   └── 📂 inspecciones/          # Fotos de inspecciones
│
├── 📂 docs/                       # Documentación técnica
│   ├── PREPARACION-PRODUCCION.md
│   ├── GUIA-PRUEBAS.md
│   ├── REPORTE-PRUEBAS.md
│   ├── IMPLEMENTACION-FASE-2.md
│   └── RESUMEN-SESION-2.md
│
├── 📂 scripts/                    # Scripts de utilidad
│   ├── install.ps1               # Instalación inicial
│   ├── setup-database.ps1        # Setup BD
│   └── start-dev.ps1             # Inicio desarrollo
│
├── 📄 README.md                   # Documentación principal
├── 📄 QUICKSTART.md               # Guía inicio rápido
├── 📄 TUTORIAL.md                 # Tutorial completo
└── 📄 .gitignore                  # Archivos ignorados por git
```

## 🗂️ Organización por Funcionalidad

### 🔐 Autenticación (JWT)
- Backend: `backend/app/routers/auth.py`, `backend/app/utils/auth.py`
- Frontend: `frontend/src/api/auth.ts`, `frontend/src/pages/Login.tsx`

### 📋 Inspecciones
- Backend: `backend/app/routers/inspecciones.py`
- Frontend: `frontend/src/pages/Inspecciones.tsx`, `frontend/src/components/InspeccionModal.tsx`

### 👥 Gestión Usuarios (Admin)
- Backend: `backend/app/routers/usuarios.py`
- Frontend: `frontend/src/pages/Usuarios.tsx`

### 🏭 Gestión Plantas (Supervisor)
- Backend: `backend/app/routers/plantas.py`
- Frontend: `frontend/src/pages/Plantas.tsx`

### 🚢 Gestión Navieras (Supervisor)
- Backend: `backend/app/routers/navieras.py`
- Frontend: `frontend/src/pages/Navieras.tsx`

## 📦 Archivos de Configuración

| Archivo | Propósito |
|---------|-----------|
| `backend/.env` | Variables de entorno (SECRET_KEY, DATABASE_URL) |
| `backend/requirements.txt` | Dependencias Python |
| `frontend/package.json` | Dependencias Node.js |
| `frontend/vite.config.ts` | Configuración del bundler |
| `frontend/tailwind.config.js` | Estilos CSS |
| `.gitignore` | Archivos excluidos de git |

## 🚀 Comandos Principales

```powershell
# Instalación inicial
.\scripts\install.ps1

# Setup base de datos
.\scripts\setup-database.ps1

# Iniciar desarrollo
.\scripts\start-dev.ps1

# Backend (manual)
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000

# Frontend (manual)
cd frontend
npm run dev

# Tests
cd backend
pytest
```

## 📝 Notas

- **Capturas**: Las imágenes subidas se almacenan en `capturas/`
- **Logs**: Los logs de desarrollo aparecen en consola
- **Base de datos**: MySQL en `localhost:3306`
- **Puertos**: Backend 8000, Frontend 5173

---

**Última actualización**: 14 de octubre de 2025  
**Versión**: 2.1.0
