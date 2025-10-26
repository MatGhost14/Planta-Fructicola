# 🍊 Sistema de Inspección de Contenedores Frutícolas

Sistema web completo para la gestión y control de inspecciones de contenedores de productos frutícolas, con captura de fotos, firmas digitales, generación de reportes y exportación a PDF/Excel.

---

## 📋 Descripción General

Este sistema permite a inspectores, supervisores y administradores gestionar el proceso completo de inspección de contenedores frutícolas de manera digital, eliminando el uso de papel y mejorando la trazabilidad de las operaciones.

### ✨ Características Principales

#### 🔐 **Autenticación y Roles**
- Sistema de autenticación JWT con bcrypt
- 3 niveles de acceso: Inspector, Supervisor y Administrador
- Control de permisos por rol
- Sesiones seguras con tokens de 8 horas

#### 📸 **Gestión de Inspecciones**
- Creación de inspecciones con datos del contenedor
- Captura de fotos directamente desde la cámara web
- Firma digital del inspector
- Registro de temperatura y observaciones
- Organización automática de fotos por fecha (dd-mm-yyyy)
- Almacenamiento estructurado: `capturas/inspecciones/26-10-2025/[id]/`

#### 📊 **Reportes y Estadísticas**
- Dashboard con métricas en tiempo real
- Estadísticas por planta, naviera y estado
- Gráficos interactivos de tendencias
- Exportación a PDF con formato profesional
- Exportación a Excel para análisis

#### 🏭 **Gestión de Catálogos**
- Administración de plantas
- Gestión de navieras
- Control de usuarios
- Configuración de preferencias

#### 🔍 **Búsqueda y Filtros**
- Búsqueda por número de contenedor
- Filtros por planta, naviera, estado y fecha
- Paginación de resultados
- Ordenamiento personalizable

---

## 🏗️ Arquitectura del Sistema

### **Backend**
- **Framework**: FastAPI 0.104+
- **Base de Datos**: MySQL/MariaDB
- **ORM**: SQLAlchemy 2.0+
- **Autenticación**: JWT + bcrypt
- **Validación**: Pydantic v2
- **Documentación**: Swagger UI / ReDoc

### **Frontend**
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite 5
- **Estilos**: Tailwind CSS 3
- **Estado**: Zustand
- **HTTP Client**: Axios
- **Routing**: React Router v6

### **Base de Datos**
```
├── usuarios (inspectores, supervisores, admins)
├── plantas (ubicaciones de inspección)
├── navieras (compañías navieras)
├── inspecciones (registros principales)
├── fotos_inspeccion (imágenes capturadas)
├── bitacora_auditoria (logs de sistema)
└── preferencias_usuario (configuración)
```

---

## 🚀 Inicio Rápido

### **Requisitos Previos**
- Python 3.8 o superior
- Node.js 16 o superior
- MySQL/MariaDB (XAMPP recomendado)
- Git

### **Instalación Automática**

Ejecuta el script de instalación que configura todo automáticamente:

```bash
start-local.bat
```

Este script:
1. ✅ Verifica requisitos del sistema
2. ✅ Crea el archivo `.env` con configuración
3. ✅ Instala dependencias de Python
4. ✅ Instala dependencias de Node.js
5. ✅ Importa la base de datos
6. ✅ Inicia el backend (puerto 8001)
7. ✅ Inicia el frontend (puerto 5173)
8. ✅ Abre el navegador automáticamente

### **Instalación Manual**

Si prefieres instalar manualmente, consulta [INSTALACION.md](INSTALACION.md) para instrucciones detalladas paso a paso.

---

## 🌐 Acceso al Sistema

Una vez iniciado el sistema:

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8001
- **Documentación API**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

### **Credenciales de Prueba**

| Rol | Correo | Contraseña |
|-----|--------|------------|
| **Administrador** | carlos.ruiz@empresa.com | 123456 |
| **Supervisor** | maria.lopez@empresa.com | 123456 |
| **Inspector** | juan.diaz@empresa.com | 123456 |

---

## 📁 Estructura del Proyecto

```
Planta-Fruticola/
├── backend/                    # API FastAPI
│   ├── app/
│   │   ├── core/              # Configuración central
│   │   ├── models/            # Modelos SQLAlchemy
│   │   ├── schemas/           # Esquemas Pydantic
│   │   ├── routers/           # Endpoints API
│   │   ├── repositories/      # Acceso a datos
│   │   ├── services/          # Lógica de negocio
│   │   ├── middleware/        # Middleware personalizado
│   │   └── utils/             # Utilidades
│   ├── scripts/               # Scripts de utilidad
│   ├── requirements.txt       # Dependencias Python
│   └── env.example            # Plantilla de configuración
├── frontend/                   # Aplicación React
│   ├── src/
│   │   ├── api/               # Clientes API
│   │   ├── components/        # Componentes React
│   │   ├── contexts/          # Context API
│   │   ├── pages/             # Páginas
│   │   ├── store/             # Estado global
│   │   ├── types/             # TypeScript types
│   │   └── utils/             # Utilidades
│   ├── package.json           # Dependencias Node.js
│   └── vite.config.ts         # Configuración Vite
├── database/                   # Scripts SQL
│   └── inspeccioncontenedor.sql
├── capturas/                   # Archivos subidos
│   ├── inspecciones/          # Fotos por fecha
│   └── firmas/                # Firmas digitales
├── start-local.bat            # Script de inicio automático
├── README.md                  # Este archivo
└── INSTALACION.md             # Guía de instalación
```

---

## 🔧 Configuración

### **Variables de Entorno**

El archivo `.env` se genera automáticamente con `start-local.bat`, pero puedes personalizarlo:

```env
# Base de datos
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=inspeccioncontenedor

# Seguridad
SECRET_KEY=tu-clave-secreta-super-segura
ACCESS_TOKEN_EXPIRE_MINUTES=480

# CORS
ALLOWED_ORIGINS=http://localhost:5173

# Servidor
BACKEND_PORT=8001
```

---

## 📚 Documentación Adicional

- **[INSTALACION.md](INSTALACION.md)** - Guía completa de instalación manual
- **[API Docs](http://localhost:8001/docs)** - Documentación interactiva de la API (cuando el backend esté ejecutándose)

---

## 🛠️ Desarrollo

### **Comandos Útiles**

#### Backend
```bash
cd backend

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor de desarrollo
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload

# Crear usuario administrador
python scripts/create_admin.py
```

#### Frontend
```bash
cd frontend

# Instalar dependencias
npm install

# Ejecutar servidor de desarrollo
npm run dev

# Build para producción
npm run build
```

---

## 🧪 Testing

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm run test
```

---

## 📦 Tecnologías Utilizadas

### Backend
- FastAPI - Framework web moderno
- SQLAlchemy - ORM para Python
- Pydantic - Validación de datos
- python-jose - JWT tokens
- passlib - Hash de contraseñas
- ReportLab - Generación de PDFs
- OpenPyXL - Generación de Excel

### Frontend
- React - Librería UI
- TypeScript - Tipado estático
- Vite - Build tool
- Tailwind CSS - Framework CSS
- Zustand - Gestión de estado
- Axios - Cliente HTTP
- React Router - Enrutamiento

---

## 🤝 Contribución

Este es un proyecto privado. Para contribuir:

1. Crea una rama para tu feature: `git checkout -b feature/nueva-funcionalidad`
2. Commit tus cambios: `git commit -m 'Agrega nueva funcionalidad'`
3. Push a la rama: `git push origin feature/nueva-funcionalidad`
4. Abre un Pull Request

---

## 📄 Licencia

Este proyecto es propietario y confidencial. Todos los derechos reservados.

---

## 👥 Soporte

Para soporte técnico o consultas:
- Revisa la documentación en [INSTALACION.md](INSTALACION.md)
- Consulta los logs del sistema
- Contacta al equipo de desarrollo

---

## 🎯 Roadmap

### Versión Actual: 2.1.0
- ✅ Sistema de autenticación completo
- ✅ Gestión de inspecciones
- ✅ Captura de fotos y firmas
- ✅ Reportes y estadísticas
- ✅ Exportación PDF/Excel
- ✅ Organización de fotos por fecha

### Próximas Versiones
- 📱 Aplicación móvil nativa
- 🌐 Modo offline con sincronización
- 📧 Notificaciones por email
- 🔔 Alertas en tiempo real
- 📊 Dashboard avanzado con BI
- 🌍 Soporte multiidioma

---

**Desarrollado con ❤️ para la industria frutícola**

*Última actualización: Octubre 2025*