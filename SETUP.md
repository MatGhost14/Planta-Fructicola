# 🚀 Guía de Configuración - Sistema de Inspección de Contenedores

Esta guía está diseñada para que cualquier colaborador pueda levantar el proyecto en minutos.

## 📋 Requisitos Previos

1. **Docker Desktop** instalado y ejecutándose
   - Windows: [Descargar Docker Desktop](https://www.docker.com/products/docker-desktop)
   - Verifica con: `docker --version` y `docker-compose --version`

2. **Git** instalado
   - Windows: [Descargar Git](https://git-scm.com/download/win)

3. **Puertos libres**: 3307 (MySQL), 8000 (Backend), 5173 (Frontend)

---

## 🎯 Inicio Rápido (3 pasos)

### 1️⃣ Clonar el repositorio

```bash
git clone <URL-DEL-REPOSITORIO>
cd Planta-
```

### 2️⃣ Iniciar Docker Desktop

Asegúrate de que Docker Desktop esté ejecutándose (ícono en la bandeja del sistema).

### 3️⃣ Ejecutar el script de inicio

```bash
# En Windows:
start-docker.bat

# O manualmente:
docker-compose up -d --build
```

**¡Eso es todo!** 🎉

El script automáticamente:
- ✅ Verifica que Docker esté instalado
- ✅ Descarga las imágenes necesarias (primera vez)
- ✅ Crea los contenedores (MySQL, Backend, Frontend)
- ✅ Inicializa la base de datos con estructura y datos de prueba
- ✅ Espera a que MySQL esté listo antes de iniciar el backend
- ✅ Abre el navegador en http://localhost:5173

---

## 🌐 URLs de Acceso

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **Frontend** | http://localhost:5173 | Aplicación web React |
| **Backend API** | http://localhost:8000 | API FastAPI |
| **API Docs** | http://localhost:8000/docs | Swagger UI interactiva |
| **MySQL** | localhost:3307 | Base de datos (usuario: `planta_user`, password: `planta_password`) |

---

## 🔑 Credenciales de Prueba

La base de datos viene pre-configurada con usuarios de prueba:

| Rol | Email | Contraseña |
|-----|-------|------------|
| **Inspector** | juan.diaz@empresa.com | 123456 |
| **Supervisor** | maria.lopez@empresa.com | 123456 |
| **Admin** | carlos.ruiz@empresa.com | 123456 |

---

## 📊 Contenido de la Base de Datos

Al iniciar por primera vez, la base de datos incluye automáticamente:

✅ **Estructura completa**:
- Tablas: `usuarios`, `plantas`, `navieras`, `inspecciones`, `fotos_inspeccion`, `bitacora_auditoria`
- Triggers: Auditoría automática de inspecciones
- Vistas: Resúmenes y conteos

✅ **Datos iniciales**:
- 3 usuarios (Inspector, Supervisor, Admin)
- 5 plantas de ejemplo
- 5 navieras de ejemplo
- Configuración de preferencias

---

## 🛠️ Comandos Útiles

### Iniciar el sistema
```bash
start-docker.bat
# O manualmente:
docker-compose up -d
```

### Detener el sistema
```bash
stop-docker.bat
# O manualmente:
docker-compose down
```

### Reset completo (limpia la BD)
```bash
reset-docker.bat
# Útil cuando necesitas empezar desde cero
```

### Ver logs en tiempo real
```bash
# Todos los servicios
docker-compose logs -f

# Solo el backend
docker-compose logs -f backend

# Solo MySQL
docker-compose logs -f mysql
```

### Ver estado de los contenedores
```bash
docker-compose ps
```

### Acceder al contenedor
```bash
# Backend
docker exec -it planta_backend bash

# MySQL
docker exec -it planta-mysql mysql -u planta_user -pplanta_password inspeccioncontenedor
```

---

## 🔄 Flujo de Inicialización Automática

```mermaid
graph TD
    A[Ejecutar start-docker.bat] --> B[Docker Compose Up]
    B --> C[Crear contenedor MySQL]
    C --> D[MySQL ejecuta init.sql]
    D --> E[MySQL health check: OK]
    E --> F[Crear contenedor Backend]
    F --> G[Backend espera a MySQL]
    G --> H[Backend verifica BD]
    H --> I[Backend inicia Uvicorn]
    I --> J[Crear contenedor Frontend]
    J --> K[Sistema listo!]
```

### ¿Qué hace el script `entrypoint.sh` del backend?

1. ⏳ **Espera a MySQL**: Intenta conectar hasta 30 veces (1 minuto)
2. 🔍 **Verifica la BD**: Comprueba que las tablas existan
3. ✅ **Inicia el servidor**: Ejecuta Uvicorn cuando todo está listo

---

## ❓ Solución de Problemas

### Problema: "ERROR: Docker no encontrado"
**Solución**: Instala Docker Desktop y asegúrate de que esté ejecutándose.

### Problema: "Port is already in use"
**Solución**: 
```bash
# Identifica el proceso que usa el puerto
netstat -ano | findstr :3307
netstat -ano | findstr :8000
netstat -ano | findstr :5173

# Mata el proceso o cambia el puerto en docker-compose.yml
```

### Problema: "Base de datos vacía o sin datos"
**Solución**:
```bash
# Ejecuta el reset completo
reset-docker.bat

# Luego reinicia
start-docker.bat
```

### Problema: "Backend no se conecta a MySQL"
**Solución**:
```bash
# Ver logs del backend
docker-compose logs backend

# Ver logs de MySQL
docker-compose logs mysql

# Verificar que MySQL esté saludable
docker-compose ps
```

### Problema: "La aplicación funciona pero no hay datos"
**Solución**: El volumen de MySQL puede tener datos viejos:
```bash
# Limpia y reconstruye
reset-docker.bat
start-docker.bat
```

---

## 🏗️ Arquitectura del Sistema

```
Planta-/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── main.py         # Punto de entrada
│   │   ├── routers/        # Endpoints
│   │   ├── models/         # Modelos SQLAlchemy
│   │   └── services/       # Lógica de negocio
│   ├── entrypoint.sh       # Script de inicialización
│   ├── Dockerfile          # Imagen del backend
│   └── requirements.txt    # Dependencias Python
│
├── frontend/               # Aplicación React + TypeScript
│   ├── src/
│   │   ├── pages/         # Páginas principales
│   │   ├── components/    # Componentes reutilizables
│   │   └── api/          # Cliente API
│   └── Dockerfile        # Imagen del frontend
│
├── database/
│   └── inspeccioncontenedor.sql  # Script de inicialización de BD
│
├── docker-compose.yml      # Orquestación de servicios
├── start-docker.bat        # Script de inicio
├── stop-docker.bat         # Script de detención
└── reset-docker.bat        # Script de reset
```

---

## 🔐 Variables de Entorno

### Backend (`docker-compose.yml`)
```yaml
DATABASE_URL: mysql://planta_user:planta_password@mysql:3306/inspeccioncontenedor
SECRET_KEY: tu_clave_secreta_super_segura_aqui
CAPTURAS_DIR: /app/capturas
```

### Frontend
```yaml
VITE_API_URL: http://localhost:8000
```

---

## 📝 Notas Importantes

### ✅ Primera ejecución
- La primera vez tardará más (descarga imágenes Docker)
- MySQL necesita ~30 segundos para inicializar
- El backend espera automáticamente a que MySQL esté listo

### ✅ Persistencia de datos
- Los datos de MySQL se guardan en un volumen Docker (`mysql_data`)
- Los datos persisten entre reinicios de contenedores
- Para limpiar: ejecuta `reset-docker.bat`

### ✅ Capturas de fotos y firmas
- Las capturas se guardan en `./capturas/`
- Este directorio está montado como volumen
- Los archivos persisten fuera de los contenedores

---

## 🤝 Soporte

Si tienes problemas:

1. **Revisa los logs**: `docker-compose logs -f`
2. **Verifica el estado**: `docker-compose ps`
3. **Reset completo**: `reset-docker.bat`
4. **Contacta al equipo**: [Agregar contacto]

---

## 🎓 Próximos Pasos

Una vez que el sistema esté funcionando:

1. 📖 Lee la documentación del API: http://localhost:8000/docs
2. 👤 Inicia sesión con las credenciales de prueba
3. 🔍 Explora las funcionalidades de inspección
4. 💻 Revisa el código en `backend/app/` y `frontend/src/`

---

¡Feliz desarrollo! 🚀

