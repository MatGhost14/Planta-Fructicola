@echo off
echo.
echo ==========================================
echo   Sistema de Inspeccion de Contenedores
echo ==========================================
echo.

echo Verificando dependencias...

REM Verificar XAMPP
if not exist "C:\xampp" (
    echo ERROR: XAMPP no encontrado en C:\xampp
    pause
    exit /b 1
)
echo ✓ XAMPP encontrado

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no encontrado
    pause
    exit /b 1
)
echo ✓ Python encontrado

REM Verificar Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js no encontrado
    pause
    exit /b 1
)
echo ✓ Node.js encontrado

echo.
echo Iniciando Backend...
start "Backend - FastAPI" cmd /k "cd /d %~dp0backend && call venv\Scripts\activate.bat && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo.
echo Iniciando Frontend...
start "Frontend - React" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ==========================================
echo   Sistema iniciado correctamente!
echo ==========================================
echo.
echo ✓ Backend API:    http://localhost:8000
echo ✓ API Docs:      http://localhost:8000/docs
echo ✓ Frontend:      http://localhost:5173
echo.
echo 🔑 Credenciales de prueba:
echo   Inspector:  juan.diaz@empresa.com / 123456
echo   Supervisor: maria.lopez@empresa.com / 123456
echo   Admin:      carlos.ruiz@empresa.com / 123456
echo.
echo 💡 Los servicios se ejecutan en ventanas separadas
echo    Puedes cerrar esta ventana sin afectar el sistema
echo.
pause
