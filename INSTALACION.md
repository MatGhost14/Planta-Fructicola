# 📦 Guía de Instalación - Sistema de Inspección de Contenedores

Esta guía te llevará paso a paso por la instalación completa del sistema, tanto automática como manual.

---

## 🎯 Instalación Automática (Recomendada)

La forma más rápida de instalar y ejecutar el sistema.

### **Paso 1: Clonar el Repositorio**

```bash
git clone <url-del-repositorio>
cd Planta-Fruticola
```

### **Paso 2: Ejecutar Script de Instalación**

```bash
start-local.bat
```

El script realizará automáticamente:
- ✅ Verificación de requisitos (Python, Node.js, MySQL)
- ✅ Creación del archivo `.env` con configuración
- ✅ Instalación de dependencias del backend
- ✅ Instalación de dependencias del frontend
- ✅ Importación de la base de datos
- ✅ Inicio del backend en puerto 8001
- ✅ Inicio del frontend en puerto 5173
- ✅ Apertura automática del navegador

### **Paso 3: Acceder al Sistema**

El navegador se abrirá automáticamente en http://localhost:5173

**Credenciales de prueba:**
- **Admin**: carlos.ruiz@empresa.com / 123456
- **Supervisor**: maria.lopez@empresa.com / 123456
- **Inspector**: juan.diaz@empresa.com / 123456

---

## 🔧 Instalación Manual

Si prefieres instalar manualmente o el script automático falla.

### **Requisitos del Sistema**

#### Software Necesario
| Software | Versión Mínima | Descarga |
|----------|----------------|----------|
| Python | 3.8+ | https://python.org |
| Node.js | 16+ | https://nodejs.org |
| MySQL/MariaDB | 5.7+ / 10.3+ | https://www.apachefriends.org (XAMPP) |
| Git | 2.0+ | https://git-scm.com |

#### Verificar Instalaciones

```bash
# Verificar Python
python --version
# Debe mostrar: Python 3.8.x o superior

# Verificar Node.js
node --version
# Debe mostrar: v16.x.x o superior

# Verificar npm
npm --version
# Debe mostrar: 8.x.x o superior

# Verificar Git
git --version
# Debe mostrar: git version 2.x.x
```

---

### **Paso 1: Clonar el Repositorio**

```bash
git clone <url-del-repositorio>
cd Planta-Fruticola
```

---

### **Paso 2: Configurar MySQL/MariaDB**

#### 2.1. Iniciar XAMPP

1. Abre **XAMPP Control Panel**
2. Inicia **MySQL** (debe quedar en verde)
3. Verifica que esté ejecutándose en puerto **3306**

#### 2.2. Crear Base de Datos

**Opción A: Usando phpMyAdmin**
1. Abre http://localhost/phpmyadmin
2. Clic en "Nuevo" para crear base de datos
3. Nombre: `inspeccioncontenedor`
4. Cotejamiento: `utf8mb4_general_ci`
5. Clic en "Crear"

**Opción B: Usando línea de comandos**
```bash
mysql -u root -p
CREATE DATABASE inspeccioncontenedor CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
exit;
```

#### 2.3. Importar Estructura y Datos

**Opción A: phpMyAdmin**
1. Selecciona la base de datos `inspeccioncontenedor`
2. Clic en pestaña "Importar"
3. Selecciona el archivo `database/inspeccioncontenedor.sql`
4. Clic en "Continuar"

**Opción B: Línea de comandos**
```bash
mysql -u root -p inspeccioncontenedor < database/inspeccioncontenedor.sql
```

#### 2.4. Verificar Importación

```sql
USE inspeccioncontenedor;
SHOW TABLES;
-- Debe mostrar 8 tablas

SELECT COUNT(*) FROM usuarios;
-- Debe mostrar 3 usuarios
```

---

### **Paso 3: Configurar Backend**

#### 3.1. Navegar al Directorio

```bash
cd backend
```

#### 3.2. Crear Entorno Virtual (Recomendado)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3.3. Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3.4. Crear Archivo .env

Crea un archivo `.env` en el directorio `backend/` con el siguiente contenido:

```env
# Base de datos
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=inspeccioncontenedor

# Seguridad
SECRET_KEY=tu-clave-secreta-super-segura-cambiar-en-produccion-2025
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
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8001

# Logging
LOG_LEVEL=INFO
LOG_FILE=app.log
```

**Importante:** Cambia `SECRET_KEY` por una clave aleatoria segura.

#### 3.5. Verificar Instalación

```bash
python -c "import fastapi; print('FastAPI:', fastapi.__version__)"
python -c "import sqlalchemy; print('SQLAlchemy:', sqlalchemy.__version__)"
```

---

### **Paso 4: Configurar Frontend**

#### 4.1. Navegar al Directorio

```bash
cd ../frontend
```

#### 4.2. Instalar Dependencias

```bash
npm install
```

Este proceso puede tomar varios minutos.

#### 4.3. Verificar Configuración

El archivo `frontend/src/api/axios.ts` debe tener:

```typescript
baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8001/api'
```

---

### **Paso 5: Iniciar el Sistema**

#### 5.1. Iniciar Backend

**Terminal 1:**
```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

**Espera a ver:**
```
INFO: Uvicorn running on http://127.0.0.1:8001
INFO: CORS configurado: http://localhost:5173
```

#### 5.2. Iniciar Frontend

**Terminal 2:**
```bash
cd frontend
npm run dev
```

**Espera a ver:**
```
VITE v5.x.x  ready in xxx ms
➜  Local:   http://localhost:5173/
```

#### 5.3. Acceder al Sistema

Abre tu navegador en: http://localhost:5173

---

## ✅ Verificación de la Instalación

### **Checklist de Verificación**

- [ ] MySQL ejecutándose en puerto 3306
- [ ] Base de datos `inspeccioncontenedor` creada
- [ ] 8 tablas importadas correctamente
- [ ] 3 usuarios de prueba en la base de datos
- [ ] Backend ejecutándose en puerto 8001
- [ ] Frontend ejecutándose en puerto 5173
- [ ] http://localhost:8001/docs carga correctamente
- [ ] http://localhost:5173 carga la página de login
- [ ] Login funciona con credenciales de prueba
- [ ] Módulo "Nueva Inspección" carga sin errores

### **Pruebas Funcionales**

#### 1. Probar Backend
```bash
# Abrir en navegador
http://localhost:8001/docs
```
Deberías ver la documentación interactiva de Swagger UI.

#### 2. Probar Autenticación

Desde la documentación (http://localhost:8001/docs):
1. Expande `POST /api/auth/login`
2. Clic en "Try it out"
3. Ingresa:
   ```json
   {
     "correo": "carlos.ruiz@empresa.com",
     "password": "123456"
   }
   ```
4. Clic en "Execute"
5. Deberías recibir un token JWT

#### 3. Probar Frontend

1. Abre http://localhost:5173
2. Inicia sesión con: carlos.ruiz@empresa.com / 123456
3. Navega a "Nueva Inspección"
4. Verifica que los dropdowns de Planta y Naviera carguen
5. Intenta capturar una foto
6. Intenta crear una firma

---

## 🔧 Solución de Problemas

### **Error: Puerto 8001 en uso**

```bash
# Windows
netstat -ano | findstr :8001
taskkill /F /PID [número_del_proceso]

# Linux/Mac
lsof -ti:8001 | xargs kill -9
```

### **Error: Puerto 5173 en uso**

```bash
# Windows
netstat -ano | findstr :5173
taskkill /F /PID [número_del_proceso]

# Linux/Mac
lsof -ti:5173 | xargs kill -9
```

### **Error: MySQL no conecta**

1. Verifica que XAMPP esté ejecutándose
2. Verifica que MySQL esté en verde
3. Verifica el puerto:
   ```bash
   netstat -ano | findstr :3306
   ```
4. Verifica credenciales en `.env`

### **Error: Módulo no encontrado (Python)**

```bash
cd backend
pip install -r requirements.txt --force-reinstall
```

### **Error: Dependencias npm**

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### **Error: CORS bloqueado**

Verifica que:
1. Backend esté en puerto 8001 (no 8000)
2. `.env` tenga: `ALLOWED_ORIGINS=http://localhost:5173`
3. Backend se haya reiniciado después de cambios

### **Error: Fotos no se visualizan**

1. Verifica que exista el directorio `capturas/`
2. Verifica permisos de escritura
3. Verifica que las rutas en BD sean correctas:
   ```sql
   SELECT foto_path FROM fotos_inspeccion LIMIT 5;
   ```

### **Error: Base de datos vacía**

Reimporta la base de datos:
```bash
mysql -u root -p inspeccioncontenedor < database/inspeccioncontenedor.sql
```

---

## 🚀 Comandos Rápidos

### **Reiniciar Todo**

```bash
# Detener servicios (Ctrl + C en cada terminal)

# Backend
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload

# Frontend (nueva terminal)
cd frontend
npm run dev
```

### **Ver Logs**

```bash
# Backend
cd backend
tail -f app.log

# Frontend
# Los logs aparecen en la terminal donde ejecutaste npm run dev
```

### **Actualizar Dependencias**

```bash
# Backend
cd backend
pip install -r requirements.txt --upgrade

# Frontend
cd frontend
npm update
```

---

## 📚 Recursos Adicionales

- **Documentación API**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc
- **README Principal**: [README.md](README.md)

---

## 🆘 Soporte

Si después de seguir esta guía aún tienes problemas:

1. Revisa los logs del backend (`backend/app.log`)
2. Revisa la consola del navegador (F12)
3. Verifica que todos los requisitos estén instalados
4. Asegúrate de que no haya conflictos de puertos
5. Contacta al equipo de desarrollo

---

**¡Listo! El sistema debería estar funcionando correctamente** 🎉

*Última actualización: Octubre 2025*
