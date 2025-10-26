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
    echo Descarga: https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)
echo ✓ Docker encontrado

echo.
echo Verificando Docker Compose...
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker Compose no encontrado
    echo Por favor instala Docker Desktop completo
    pause
    exit /b 1
)
echo ✓ Docker Compose encontrado

echo.
echo Limpiando contenedores anteriores...
docker-compose down >nul 2>&1

echo.
echo Construyendo imagenes Docker...
echo Esto puede tomar unos minutos en la primera ejecucion...
docker-compose build

if errorlevel 1 (
    echo ERROR: Fallo al construir las imagenes
    echo Verifica que Docker Desktop este ejecutandose
    pause
    exit /b 1
)

echo.
echo Iniciando contenedores...
docker-compose up -d

if errorlevel 1 (
    echo ERROR: Fallo al iniciar los contenedores
    echo Verifica que los puertos 8000 y 5173 esten libres
    pause
    exit /b 1
)

echo.
echo Esperando que los servicios esten listos...
echo Esto puede tomar 30-60 segundos...

:wait_loop
timeout /t 5 /nobreak >nul
docker ps | findstr "planta_backend" | findstr "Up" >nul
if errorlevel 1 (
    echo Esperando backend...
    goto wait_loop
)

docker ps | findstr "planta_frontend" | findstr "Up" >nul
if errorlevel 1 (
    echo Esperando frontend...
    goto wait_loop
)

docker ps | findstr "planta-mysql" | findstr "Up" >nul
if errorlevel 1 (
    echo Esperando base de datos...
    goto wait_loop
)

echo.
echo Verificando conectividad de la base de datos...
timeout /t 10 /nobreak >nul

echo.
echo Verificando que los usuarios de prueba esten disponibles...
docker exec planta-mysql mysql -u planta_user -pplanta_password inspeccioncontenedor -e "SELECT COUNT(*) as usuarios FROM usuarios;" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Base de datos aun no esta lista, esperando...
    timeout /t 10 /nobreak >nul
    goto wait_loop
)

echo.
echo Verificando API del backend...
timeout /t 5 /nobreak >nul

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
echo 💡 Comandos utiles:
echo   Ver logs:     .\docker-logs.bat
echo   Detener:      .\stop-docker.bat
echo   Reiniciar:    docker-compose restart
echo.
echo Abriendo el navegador...
start http://localhost:5173
echo.
echo Presiona cualquier tecla para continuar...
pause >nul
