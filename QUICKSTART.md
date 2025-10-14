# ⚡ Inicio Rápido - Sistema de Inspección de Contenedores

Guía de inicio rápido en 5 minutos.

---

## ✅ Pre-requisitos

- ✅ Python 3.10+
- ✅ Node.js 18+
- ✅ XAMPP con MySQL

---

## 🚀 Instalación en 3 Pasos

### 1️⃣ Instalar Dependencias

```powershell
.\install.ps1
```

### 2️⃣ Configurar Base de Datos

```powershell
.\setup-database.ps1
```

### 3️⃣ Iniciar Aplicación

```powershell
.\start-dev.ps1
```

---

## 🌐 Acceder

- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs

---

## 📚 Documentación Completa

Para instrucciones detalladas, ver:
- [README.md](README.md) - Información general
- [TUTORIAL.md](TUTORIAL.md) - Tutorial paso a paso completo

---

## 🐛 Problemas Comunes

### Backend no inicia
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Frontend no inicia
```powershell
cd frontend
npm install
```

### Error de BD
- Verificar que MySQL esté corriendo en XAMPP
- Verificar `backend\.env`

---

**¿Primera vez?** → Lee el [TUTORIAL.md](TUTORIAL.md) completo
