# ⚡ Inicio Rápido - 5 Minutos

Guía express para tener el sistema funcionando en menos de 5 minutos.

---

## 🚀 Instalación Express

### 1. Requisitos (2 minutos)

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

### 3. Instalar TODO (1 minuto)

```powershell
.\install.ps1
```

Este script instala:
- ✅ Backend (FastAPI + dependencias)
- ✅ Frontend (React + TypeScript)
- ✅ Todas las librerías necesarias

### 4. Configurar Base de Datos (30 segundos)

```powershell
.\setup-database.ps1
```

Este script:
- ✅ Crea la BD `impeccioncontenedor`
- ✅ Importa el schema
- ✅ Crea usuarios de prueba

### 5. Iniciar Sistema (30 segundos)

```powershell
.\start-dev.ps1
```

Abre automáticamente:
- 🟢 Backend: http://localhost:8000
- 🟢 Frontend: http://localhost:5173

---

## 🔐 Login Instantáneo

Ve a **http://localhost:5173** y usa:

```
Inspector:
📧 inspector@empresa.com
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

### Backend no inicia
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend no inicia
```powershell
cd frontend
npm install
npm run dev
```

### Base de datos no conecta
1. Abre XAMPP Control Panel
2. Inicia "MySQL"
3. Ve a http://localhost/phpmyadmin
4. Importa `impeccioncontenedor.sql`

---

**¿Listo? ¡Empieza a usar el sistema! 🚀**
