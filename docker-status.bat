@echo off
echo.
echo ==========================================
echo   Estado del Sistema Docker
echo ==========================================
echo.

echo Verificando contenedores...
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo.
echo Verificando servicios...
echo.

echo [Backend API]
curl -s http://localhost:8000/api/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Backend no disponible en http://localhost:8000
) else (
    echo ✅ Backend funcionando en http://localhost:8000
)

echo.
echo [Frontend]
curl -s http://localhost:5173 >nul 2>&1
if errorlevel 1 (
    echo ❌ Frontend no disponible en http://localhost:5173
) else (
    echo ✅ Frontend funcionando en http://localhost:5173
)

echo.
echo [Base de Datos]
docker exec planta-mysql mysql -u planta_user -pplanta_password -e "SELECT 1;" >nul 2>&1
if errorlevel 1 (
    echo ❌ Base de datos no disponible
) else (
    echo ✅ Base de datos funcionando
)

echo.
echo [Usuarios de Prueba]
docker exec planta-mysql mysql -u planta_user -pplanta_password inspeccioncontenedor -e "SELECT COUNT(*) as total_usuarios FROM usuarios;" 2>nul
if errorlevel 1 (
    echo ❌ No se pueden verificar los usuarios
) else (
    echo ✅ Usuarios de prueba disponibles
)

echo.
echo ==========================================
echo   Informacion del Sistema
echo ==========================================
echo.
echo URLs disponibles:
echo   Frontend:    http://localhost:5173
echo   Backend:     http://localhost:8000
echo   API Docs:    http://localhost:8000/docs
echo   MySQL:       localhost:3307
echo.
echo Comandos utiles:
echo   Ver logs:    .\docker-logs.bat
echo   Detener:     .\stop-docker.bat
echo   Reiniciar:   docker-compose restart
echo.
pause
