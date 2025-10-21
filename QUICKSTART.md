# ⚡ Inicio Rápido - 5 Minutos

Guía express para tener el sistema funcionando en menos de 5 minutos.

---

## 🚀 Instalación Express

### 1. Requisitos (2 minutos)

**Opción A: Docker (Recomendado)**
✅ Instalar solo:
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

**Opción B: Tradicional**
✅ Instalar si no tienes:
- [Python 3.10+](https://python.org)
- [Node.js 18+](https://nodejs.org)
- [XAMPP](https://www.apachefriends.org/) (para MySQL)

### 2. Clonar/Descargar Proyecto

```powershell
cd "C:\Users\TuUsuario\Desktop"
# Si tienes el proyecto descargado, ve a la carpeta
cd Planta-
```

### 3. Iniciar Sistema (1 minuto)

**Opción A: Docker (Recomendado para Colaboradores)**
```cmd
.\start-docker.bat
```

**Opción B: Script Tradicional**
```cmd
.\start-system-simple.bat
```

**Docker automáticamente:**
- ✅ Instala todas las dependencias
- ✅ Configura MySQL en contenedor
- ✅ Crea la BD `inspeccioncontenedor`
- ✅ Importa el schema de la base de datos
- ✅ Inicia el backend (FastAPI) en puerto 8000
- ✅ Inicia el frontend (React) en puerto 5173
- ✅ Sin problemas de dependencias

---

## 🔐 Login Instantáneo

Ve a **http://localhost:5173** y usa:

```
Inspector:
📧 juan.diaz@empresa.com
🔑 password123

Supervisor:
📧 maria.lopez@empresa.com
🔑 password123

Admin:
📧 carlos.ruiz@empresa.com
🔑 password123
```

---

## ✨ ¡Eso es todo!

Ahora puedes:
- ✅ Ver el Dashboard
- ✅ Crear inspecciones
- ✅ Subir fotos
- ✅ Ver detalles en modal

---

## 📚 Siguiente Paso

Lee el [TUTORIAL.md](TUTORIAL.md) para aprender todas las funcionalidades.

---

## 🐛 Si algo falla

### Docker no inicia
```cmd
# Verificar Docker
docker --version

# Ver logs
.\docker-logs.bat

# Reiniciar contenedores
docker-compose restart
```

### Contenedores no se construyen
```cmd
# Limpiar y reconstruir
docker-compose down
docker-compose up --build -d
```

### Puerto ya en uso
```cmd
# Detener contenedores
.\stop-docker.bat

# Cambiar puertos en docker-compose.yml
# Luego reiniciar
.\start-docker.bat
```

### Script Tradicional (si no usas Docker)
```cmd
# Backend
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

---

**¿Listo? ¡Empieza a usar el sistema! 🚀**
