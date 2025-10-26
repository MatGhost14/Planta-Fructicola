@echo off
echo.
echo ==========================================
echo   Prueba Completa del Sistema
echo ==========================================
echo.

echo [1/5] Verificando contenedores...
docker ps --format "table {{.Names}}\t{{.Status}}" | findstr "planta"
if errorlevel 1 (
    echo ❌ Contenedores no estan ejecutandose
    echo Ejecuta: .\start-docker.bat
    pause
    exit /b 1
)
echo ✅ Contenedores ejecutandose

echo.
echo [2/5] Verificando base de datos...
docker exec planta-mysql mysql -u planta_user -pplanta_password inspeccioncontenedor -e "SELECT 1;" >nul 2>&1
if errorlevel 1 (
    echo ❌ Base de datos no disponible
    echo Ejecuta: .\docker-restart.bat
    pause
    exit /b 1
)
echo ✅ Base de datos funcionando

echo.
echo [3/5] Verificando usuarios de prueba...
docker exec planta-mysql mysql -u planta_user -pplanta_password inspeccioncontenedor -e "SELECT COUNT(*) as total FROM usuarios;" 2>nul | findstr "3" >nul
if errorlevel 1 (
    echo ❌ Usuarios de prueba no encontrados
    echo Ejecuta: .\init-users.bat
    pause
    exit /b 1
)
echo ✅ Usuarios de prueba disponibles

echo.
echo [4/5] Verificando backend API...
curl -s http://localhost:8000/api/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Backend API no disponible
    echo Ejecuta: .\docker-restart.bat
    pause
    exit /b 1
)
echo ✅ Backend API funcionando

echo.
echo [5/5] Verificando frontend...
curl -s http://localhost:5173 >nul 2>&1
if errorlevel 1 (
    echo ❌ Frontend no disponible
    echo Ejecuta: .\docker-restart.bat
    pause
    exit /b 1
)
echo ✅ Frontend funcionando

echo.
echo ==========================================
echo   ✅ SISTEMA COMPLETAMENTE FUNCIONAL
echo ==========================================
echo.
echo 🎉 Todo esta funcionando correctamente!
echo.
echo 📋 Informacion del sistema:
echo   Frontend:    http://localhost:5173
echo   Backend:     http://localhost:8000
echo   API Docs:    http://localhost:8000/docs
echo.
echo 🔑 Credenciales de prueba:
echo   Inspector:  juan.diaz@empresa.com / 123456
echo   Supervisor: maria.lopez@empresa.com / 123456
echo   Admin:      carlos.ruiz@empresa.com / 123456
echo.
echo 💡 Comandos utiles:
echo   Ver estado:  .\docker-status.bat
echo   Ver logs:    .\docker-logs.bat
echo   Detener:     .\stop-docker.bat
echo.
pause
