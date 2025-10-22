@echo off
echo.
echo ==========================================
echo   Sistema de Inspeccion de Contenedores
echo ==========================================
echo.

echo Verificando Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker no encontrado
    echo Por favor instala Docker Desktop
    pause
    exit /b 1
)
echo ✓ Docker encontrado

echo.
echo Verificando Docker Compose...
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker Compose no encontrado
    pause
    exit /b 1
)
echo ✓ Docker Compose encontrado

echo.
echo Iniciando contenedores Docker...
docker-compose up -d

echo.
echo Esperando que los servicios estén listos...
timeout /t 10 /nobreak >nul

echo.
echo ==========================================
echo   Sistema iniciado correctamente!
echo ==========================================
echo.
echo ✓ Backend API:    http://localhost:8000
echo ✓ API Docs:      http://localhost:8000/docs
echo ✓ Frontend:      http://localhost:5173
echo ✓ MySQL:         localhost:3307
echo.
echo 🔑 Credenciales de prueba:
echo   Inspector:  juan.diaz@empresa.com / 123456
echo   Supervisor: maria.lopez@empresa.com / 123456
echo   Admin:      carlos.ruiz@empresa.com / 123456
echo.
echo 💡 Los servicios se ejecutan en contenedores Docker
echo    Para detener: docker-compose down
echo.
echo Abriendo el navegador...
start http://localhost:5173
echo.
pause