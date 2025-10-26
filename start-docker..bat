@echo off
echo.
echo ==========================================
echo   Sistema de Inspeccion de Contenedores
echo ==========================================
echo.

echo 🔍 Verificando Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Docker no encontrado
    echo.
    echo 📥 Por favor instala Docker Desktop desde:
    echo    https://www.docker.com/products/docker-desktop
    echo.
    pause
    exit /b 1
)
echo ✓ Docker encontrado

echo.
echo 🔍 Verificando Docker Compose...
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Docker Compose no encontrado
    echo.
    pause
    exit /b 1
)
echo ✓ Docker Compose encontrado

echo.
echo 🚀 Iniciando contenedores Docker...
echo    (Esto puede tardar la primera vez mientras descarga imágenes)
echo.
docker-compose up -d --build

if errorlevel 1 (
    echo.
    echo ❌ ERROR: Falló el inicio de contenedores
    echo.
    echo 💡 Posibles soluciones:
    echo    1. Ejecuta: reset-docker.bat
    echo    2. Verifica que los puertos 3307, 8000 y 5173 estén libres
    echo    3. Revisa los logs: docker-compose logs
    echo.
    pause
    exit /b 1
)

echo.
echo ⏳ Esperando que los servicios estén listos...
echo    - MySQL inicializando base de datos...
echo    - Backend esperando a MySQL...
echo    - Frontend construyendo...
echo.
timeout /t 15 /nobreak >nul

echo.
echo ==========================================
echo   ✓ Sistema iniciado correctamente!
echo ==========================================
echo.
echo 🌐 URLs de acceso:
echo    Backend API:    http://localhost:8000
echo    API Docs:       http://localhost:8000/docs
echo    Frontend:       http://localhost:5173
echo    MySQL:          localhost:3307
echo.
echo 🔑 Credenciales de prueba:
echo    Inspector:  juan.diaz@empresa.com / 123456
echo    Supervisor: maria.lopez@empresa.com / 123456
echo    Admin:      carlos.ruiz@empresa.com / 123456
echo.
echo 📊 Base de datos ya incluye:
echo    ✓ Estructura completa de tablas
echo    ✓ Usuarios de prueba
echo    ✓ Plantas y navieras de ejemplo
echo    ✓ Triggers y vistas
echo.
echo 💡 Comandos útiles:
echo    Detener:        docker-compose down
echo    Ver logs:       docker-compose logs -f
echo    Reset completo: reset-docker.bat
echo.
echo 🚀 Abriendo el navegador...
start http://localhost:5173
echo.
echo ✓ Listo para usar!
echo.
pause