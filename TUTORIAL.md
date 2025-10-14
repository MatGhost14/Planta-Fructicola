# 📚 Tutorial Completo - Sistema de Inspección de Contenedores

Guía paso a paso para configurar, ejecutar y usar el sistema de inspección de contenedores.

---

## 📑 Tabla de Contenidos

1. [Preparación del Entorno](#1-preparación-del-entorno)
2. [Instalación del Proyecto](#2-instalación-del-proyecto)
3. [Configuración de la Base de Datos](#3-configuración-de-la-base-de-datos)
4. [Primer Inicio](#4-primer-inicio)
5. [Uso de la Aplicación](#5-uso-de-la-aplicación)
6. [Resolución de Problemas](#6-resolución-de-problemas)
7. [Comandos Útiles](#7-comandos-útiles)

---

## 1. Preparación del Entorno

### 📥 Paso 1.1: Instalar Software Requerido

#### Python 3.10+

1. Descargar desde: https://www.python.org/downloads/
2. Durante la instalación:
   - ✅ Marcar "Add Python to PATH"
   - ✅ Click en "Install Now"
3. Verificar instalación:
```powershell
python --version
```
Debe mostrar: `Python 3.10.x` o superior

#### Node.js 18+

1. Descargar desde: https://nodejs.org/
2. Instalar versión LTS (Long Term Support)
3. Verificar instalación:
```powershell
node --version
npm --version
```
Debe mostrar: `v18.x.x` o superior

#### XAMPP 8.0+

1. Descargar desde: https://www.apachefriends.org/
2. Instalar en: `C:\xampp`
3. Abrir **XAMPP Control Panel**
4. Hacer click en **Start** junto a **MySQL**
5. Verificar que el indicador esté verde

---

## 2. Instalación del Proyecto

### 📦 Paso 2.1: Obtener el Proyecto

Opción A: **Clonar desde Git**
```powershell
git clone https://tu-repositorio.com/inspeccion-contenedores.git
cd inspeccion-contenedores
```

Opción B: **Descargar ZIP**
1. Descargar el archivo ZIP del proyecto
2. Extraer en: `C:\Users\TuUsuario\Desktop\Planta-`
3. Abrir PowerShell en esa carpeta

### 🚀 Paso 2.2: Instalación Automática

```powershell
# Ejecutar el script de instalación
.\install.ps1
```

Este script hará lo siguiente:
1. ✅ Crear entorno virtual Python en `backend/venv/`
2. ✅ Instalar dependencias Python desde `requirements.txt`
3. ✅ Crear archivo `.env` con configuración por defecto
4. ✅ Instalar dependencias de Node.js en `frontend/`
5. ✅ Crear directorios `capturas/`

**Tiempo estimado**: 5-10 minutos (dependiendo de tu conexión)

### 🔍 Paso 2.3: Verificar Instalación

```powershell
# Verificar backend
cd backend
.\venv\Scripts\Activate.ps1
pip list | Select-String "fastapi|sqlalchemy|pydantic"

# Verificar frontend
cd ../frontend
npm list --depth=0 | Select-String "react|vite|typescript"
```

---

## 3. Configuración de la Base de Datos

### 🗄️ Paso 3.1: Importar Schema

#### Opción A: Usando el Script (Recomendado)

```powershell
cd "C:\Users\TuUsuario\Desktop\Planta-"
.\setup-database.ps1
```

#### Opción B: Manualmente con phpMyAdmin

1. Abrir navegador en: http://localhost/phpmyadmin
2. Click en **"New"** o **"Nueva"** (lado izquierdo)
3. Nombre de la base de datos: `ImpeccionContenedor`
4. Collation: `utf8mb4_general_ci`
5. Click en **"Create"** o **"Crear"**
6. Click en la pestaña **"Import"** o **"Importar"**
7. Click en **"Choose File"** o **"Seleccionar archivo"**
8. Seleccionar: `C:\Users\TuUsuario\Desktop\Planta-\impeccioncontenedor.sql`
9. Scroll hasta abajo y click en **"Go"** o **"Continuar"**
10. Esperar mensaje: **"Import has been successfully finished"**

### ✅ Paso 3.2: Verificar Datos Iniciales

En phpMyAdmin, ejecutar:

```sql
USE ImpeccionContenedor;

-- Ver tablas creadas
SHOW TABLES;

-- Ver usuarios
SELECT nombre, correo, rol FROM usuarios;

-- Ver plantas
SELECT codigo, nombre FROM plantas;

-- Ver navieras
SELECT codigo, nombre FROM navieras;
```

Deberías ver:
- 11 usuarios (inspectores, supervisores, admins)
- 12 plantas en diferentes ubicaciones
- 5 navieras internacionales

### 🔧 Paso 3.3: Configurar Conexión

Editar el archivo: `backend\.env`

```env
# Base de datos
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=           # Dejar vacío si no tienes contraseña
DB_NAME=ImpeccionContenedor

# Archivos
CAPTURAS_DIR=../capturas

# Servidor
BACKEND_PORT=8000

# CORS
CORS_ORIGINS=http://localhost:5173
```

**Nota**: Si tu MySQL tiene contraseña, agrégala en `DB_PASSWORD=tu_contraseña`

---

## 4. Primer Inicio

### 🎬 Paso 4.1: Iniciar Servicios

```powershell
cd "C:\Users\TuUsuario\Desktop\Planta-"
.\start-dev.ps1
```

Este script abrirá **DOS ventanas de PowerShell**:

**Ventana 1 - Backend (Puerto 8000)**
```
Backend FastAPI
==================
Virtual environment activado
Iniciando Uvicorn en http://localhost:8000
API Docs: http://localhost:8000/docs

INFO: Uvicorn running on http://localhost:8000 (Press CTRL+C to quit)
INFO: Started reloader process
INFO: Started server process
INFO: Waiting for application startup.
INFO: Application startup complete.
```

**Ventana 2 - Frontend (Puerto 5173)**
```
Frontend React + Vite
=====================

  VITE v5.0.11  ready in 1234 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

### 🌐 Paso 4.2: Acceder a la Aplicación

Abrir navegador en:

1. **Frontend**: http://localhost:5173
   - Interfaz principal de usuario
   - Dashboard, inspecciones, reportes

2. **Backend API**: http://localhost:8000
   - Información de la API

3. **Documentación Interactiva**: http://localhost:8000/docs
   - Swagger UI con todos los endpoints
   - Probar API directamente

### ✅ Paso 4.3: Verificar que Todo Funciona

#### Probar Backend:

Abrir en navegador: http://localhost:8000/api/health

Deberías ver:
```json
{
  "status": "ok",
  "timestamp": "2025-10-14T02:15:30.123456"
}
```

#### Probar Frontend:

Abrir: http://localhost:5173

Deberías ver:
- ✅ Sidebar con menú de navegación
- ✅ Dashboard con 4 tarjetas de KPIs
- ✅ Tabla de inspecciones recientes

---

## 5. Uso de la Aplicación

### 📋 5.1 Crear tu Primera Inspección

#### Paso a Paso:

1. **Navegar a Nueva Inspección**
   - Click en **"Nueva Inspección"** en el menú lateral
   - O ir a: http://localhost:5173/inspeccion-nueva

2. **Completar Formulario**
   
   **Planta**: Seleccionar de la lista
   - Ejemplo: "Planta Norte - Monterrey"
   
   **Naviera**: Seleccionar de la lista
   - Ejemplo: "Maersk Line"
   
   **Número de Contenedor**: Ingresar código alfanumérico
   - Ejemplo: `MAEU1234567`
   - Formato típico: 4 letras + 7 números
   
   **Temperatura (°C)**: Opcional, para contenedores refrigerados
   - Ejemplo: `-18.5`
   - Rango sugerido: -25°C a -15°C
   
   **Observaciones**: Opcional, texto libre
   - Ejemplo: "Contenedor en excelente estado, sellos intactos"

3. **Capturar Fotos**
   
   - Click en botón **"Abrir Cámara"**
   - Permitir acceso a la cámara cuando el navegador lo solicite
   - Posicionar el contenedor en el visor
   - Click en **"Capturar Foto"**
   - Repetir para múltiples fotos (mínimo 2 recomendado)
   - Las fotos aparecerán como miniaturas abajo

4. **Agregar Firma Digital**
   
   - Usar el mouse o dedo (en táctil) para dibujar firma
   - Click en **"Limpiar"** si necesitas reiniciar
   - La firma debe ser legible

5. **Guardar Inspección**
   
   - Click en botón **"Guardar Inspección"**
   - Esperar mensaje de éxito: "Inspección creada exitosamente"
   - Automáticamente irás al Dashboard

### 📊 5.2 Ver Dashboard

**URL**: http://localhost:5173/

El Dashboard muestra:

**Tarjetas de KPI**:
- 📦 **Total**: Todas las inspecciones
- ⏳ **Pendientes**: Esperando revisión
- ✅ **Aprobadas**: Inspeccionadas correctamente
- ❌ **Rechazadas**: Con problemas

**Tabla de Inspecciones Recientes**:
- Código de inspección
- Número de contenedor
- Planta y Naviera
- Estado con color
- Fecha de inspección

**Actualización en Tiempo Real**:
- Los números se actualizan automáticamente al crear/modificar inspecciones

### 🔍 5.3 Buscar y Filtrar Inspecciones

**URL**: http://localhost:5173/inspecciones

**Filtros Disponibles**:

1. **Por Estado**:
   - Todos
   - Pendientes
   - Aprobadas
   - Rechazadas

2. **Por Búsqueda**:
   - Buscar por número de contenedor
   - Ejemplo: Escribir "MAEU" para ver todos los contenedores de Maersk

**Ver Detalles**:
- Click en cualquier fila de la tabla
- Ver fotos capturadas
- Ver firma digital
- Ver toda la información

### 📈 5.4 Ver Reportes

**URL**: http://localhost:5173/reportes

**Información Mostrada**:

**Resumen General**:
- Total de inspecciones
- Cantidad aprobadas
- Cantidad pendientes
- Cantidad rechazadas
- Tasa de aprobación (%)

**Filtros de Fecha**:
- Fecha Desde: Seleccionar fecha inicial
- Fecha Hasta: Seleccionar fecha final
- Click en **"Aplicar Filtros"**

**Visualización**:
- Barras de progreso con colores
- Porcentajes calculados automáticamente

### 👥 5.5 Administrar Catálogos

**URL**: http://localhost:5173/admin

**Pestañas**:

1. **Plantas**
   - Ver todas las plantas
   - Agregar nueva planta
   - Editar existente
   - Eliminar (si no tiene inspecciones asociadas)

2. **Navieras**
   - Ver todas las navieras
   - Agregar nueva naviera
   - Editar existente
   - Eliminar (si no tiene inspecciones asociadas)

3. **Usuarios**
   - Ver todos los usuarios
   - Agregar nuevo usuario
   - Editar existente
   - Cambiar rol (Inspector, Supervisor, Admin)

---

## 6. Resolución de Problemas

### ❌ Problema: "Backend no inicia"

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solución**:
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

### ❌ Problema: "Frontend no carga"

**Error**: `npm ERR! code ENOENT`

**Solución**:
```powershell
cd frontend
npm install
npm run dev
```

---

### ❌ Problema: "Error de conexión a base de datos"

**Error**: `sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError) (2003...)`

**Solución**:
1. Verificar que XAMPP esté corriendo:
   - Abrir XAMPP Control Panel
   - MySQL debe estar en verde "Running"
   
2. Verificar credenciales en `backend\.env`:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=          # Dejar vacío o agregar contraseña
DB_NAME=ImpeccionContenedor
```

3. Verificar que la base de datos exista:
```powershell
cd "C:\xampp\mysql\bin"
.\mysql.exe -u root
```
```sql
SHOW DATABASES LIKE 'ImpeccionContenedor';
```

---

### ❌ Problema: "Puerto ya en uso"

**Error**: `Error: listen EADDRINUSE: address already in use :::8000`

**Solución**:
```powershell
# Para puerto 8000 (Backend)
netstat -ano | findstr :8000
taskkill /PID <número_del_PID> /F

# Para puerto 5173 (Frontend)
netstat -ano | findstr :5173
taskkill /PID <número_del_PID> /F
```

---

### ❌ Problema: "Cámara no funciona"

**Error**: `NotAllowedError: Permission denied`

**Solución**:
1. Permitir acceso a la cámara en el navegador
2. En Chrome: Hacer click en el icono de candado en la barra de direcciones
3. Permisos → Cámara → Permitir
4. Recargar la página (F5)

**Alternativa**:
- Usar HTTPS en lugar de HTTP (la cámara funciona mejor con conexión segura)
- O usar localhost (que es considerado seguro)

---

### ❌ Problema: "Las fotos no se guardan"

**Error**: `500 Internal Server Error` al subir fotos

**Solución**:
```powershell
# Verificar que existan los directorios
cd "C:\Users\TuUsuario\Desktop\Planta-"
Test-Path "capturas\inspecciones"
Test-Path "capturas\firmas"

# Si no existen, crearlos
New-Item -ItemType Directory -Path "capturas\inspecciones" -Force
New-Item -ItemType Directory -Path "capturas\firmas" -Force
```

---

## 7. Comandos Útiles

### 🔄 Reiniciar Servicios

```powershell
# Detener servicios (Ctrl+C en cada ventana de PowerShell)
# Luego reiniciar:
cd "C:\Users\TuUsuario\Desktop\Planta-"
.\start-dev.ps1
```

### 🧹 Limpiar Caché

```powershell
# Backend
cd backend
Remove-Item __pycache__ -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item app\__pycache__ -Recurse -Force -ErrorAction SilentlyContinue

# Frontend
cd ../frontend
Remove-Item node_modules -Recurse -Force
Remove-Item package-lock.json -Force
npm install
```

### 📊 Ver Logs del Backend

```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000 --log-level debug
```

### 🔍 Probar API con PowerShell

```powershell
# Health Check
Invoke-RestMethod -Uri "http://localhost:8000/api/health" -Method GET

# Listar Inspecciones
$response = Invoke-RestMethod -Uri "http://localhost:8000/api/inspecciones/?limit=5" -Method GET
$response.items

# Listar Plantas
Invoke-RestMethod -Uri "http://localhost:8000/api/plantas/" -Method GET

# Ver conteo por estado
Invoke-RestMethod -Uri "http://localhost:8000/api/reportes/conteo-estado" -Method GET
```

### 🗄️ Comandos MySQL Útiles

```powershell
# Abrir MySQL CLI
cd "C:\xampp\mysql\bin"
.\mysql.exe -u root

# En MySQL:
USE ImpeccionContenedor;
SHOW TABLES;
SELECT COUNT(*) FROM inspecciones;
SELECT estado, COUNT(*) FROM inspecciones GROUP BY estado;
DESCRIBE inspecciones;
```

### 🔄 Aplicar Migraciones de Base de Datos

```powershell
cd backend
.\venv\Scripts\Activate.ps1

# Ver estado actual
alembic current

# Ver historial
alembic history

# Aplicar todas las migraciones
alembic upgrade head

# Rollback una migración
alembic downgrade -1
```

### 📦 Actualizar Dependencias

```powershell
# Backend
cd backend
.\venv\Scripts\Activate.ps1
pip list --outdated
pip install --upgrade nombre-paquete

# Frontend
cd ../frontend
npm outdated
npm update
```

---

## 8. Flujo de Trabajo Recomendado

### 🌅 Al Empezar el Día

1. Abrir XAMPP Control Panel → Start MySQL
2. Ejecutar: `.\start-dev.ps1`
3. Verificar que ambos servicios inicien correctamente
4. Abrir navegador en http://localhost:5173

### 📝 Durante el Trabajo

1. Crear inspecciones según lleguen los contenedores
2. Revisar Dashboard periódicamente
3. Supervisores: Revisar y aprobar/rechazar pendientes
4. Generar reportes al final del día/semana

### 🌙 Al Terminar el Día

1. Exportar reportes si es necesario
2. Cerrar navegador
3. Presionar Ctrl+C en cada ventana de PowerShell
4. Opcional: Detener MySQL en XAMPP

---

## 9. Tips y Mejores Prácticas

### 📸 Captura de Fotos

- ✅ Tomar al menos 2-3 fotos por inspección
- ✅ Capturar diferentes ángulos del contenedor
- ✅ Asegurar buena iluminación
- ✅ Enfocar bien el número del contenedor
- ✅ Capturar detalles de daños si existen

### ✍️ Firma Digital

- ✅ Usar trazo claro y legible
- ✅ Asegurar que la firma se vea completa
- ✅ No usar firmas genéricas (X, línea simple)
- ✅ Debe ser identificable

### 📝 Observaciones

- ✅ Ser específico y claro
- ✅ Mencionar cualquier daño visible
- ✅ Indicar si los sellos están intactos
- ✅ Incluir condiciones especiales (temperatura, humedad)

### 🔍 Búsqueda y Filtros

- ✅ Usar filtros para encontrar inspecciones rápidamente
- ✅ Buscar por número parcial de contenedor
- ✅ Filtrar por estado para revisiones pendientes

---

## 10. Glosario de Términos

| Término | Descripción |
|---------|-------------|
| **Inspección** | Revisión completa de un contenedor |
| **Planta** | Ubicación física donde se realiza la inspección |
| **Naviera** | Compañía de transporte marítimo dueña del contenedor |
| **Estado** | Pending (Pendiente), Approved (Aprobada), Rejected (Rechazada) |
| **Inspector** | Usuario que realiza inspecciones |
| **Supervisor** | Usuario que aprueba/rechaza inspecciones |
| **Admin** | Usuario con acceso completo al sistema |
| **API** | Interfaz de programación de aplicaciones (backend) |
| **Endpoint** | Ruta de API específica (ej: /api/inspecciones/) |

---

## ✅ Checklist de Verificación

Usar esta lista para confirmar que todo está funcionando:

- [ ] Python 3.10+ instalado
- [ ] Node.js 18+ instalado
- [ ] XAMPP instalado y MySQL corriendo
- [ ] Base de datos `ImpeccionContenedor` creada
- [ ] Datos iniciales importados
- [ ] Backend iniciado en puerto 8000
- [ ] Frontend iniciado en puerto 5173
- [ ] Dashboard carga correctamente
- [ ] Puedo ver la lista de inspecciones
- [ ] Puedo crear una nueva inspección
- [ ] La cámara funciona
- [ ] Puedo capturar firma
- [ ] Los reportes muestran datos
- [ ] Admin panel carga catálogos

---

## 📞 ¿Necesitas Ayuda?

Si después de seguir este tutorial aún tienes problemas:

1. Revisar la sección [Resolución de Problemas](#6-resolución-de-problemas)
2. Verificar los logs del backend (ventana de PowerShell)
3. Abrir la consola del navegador (F12) para ver errores del frontend
4. Consultar la documentación de la API: http://localhost:8000/docs

---

**¡Felicidades! Ya estás listo para usar el Sistema de Inspección de Contenedores 🚢**

Este tutorial fue creado el 14 de octubre de 2025.
