@echo off
echo.
echo ==========================================
echo   Configuracion Completa del Sistema
echo ==========================================
echo.

echo Este script configurara todo el sistema desde cero
echo para que funcione correctamente para colaboradores.
echo.

set /p confirm="¿Continuar? (s/N): "
if /i not "%confirm%"=="s" (
    echo Operacion cancelada.
    pause
    exit /b 0
)

echo.
echo [Paso 1/4] Limpiando sistema anterior...
.\docker-clean.bat
if errorlevel 1 (
    echo ❌ Error en limpieza
    pause
    exit /b 1
)

echo.
echo [Paso 2/4] Iniciando sistema...
.\start-docker.bat
if errorlevel 1 (
    echo ❌ Error al iniciar sistema
    pause
    exit /b 1
)

echo.
echo [Paso 3/4] Verificando usuarios...
.\verify-users.bat
if errorlevel 1 (
    echo ⚠️  Problemas con usuarios, intentando inicializar...
    .\init-users.bat
)

echo.
echo [Paso 4/4] Ejecutando prueba completa...
.\test-system.bat
if errorlevel 1 (
    echo ❌ El sistema no esta funcionando correctamente
    echo.
    echo Soluciones:
    echo   1. .\docker-restart.bat
    echo   2. .\docker-clean.bat && .\start-docker.bat
    echo   3. Verificar logs: .\docker-logs.bat
    pause
    exit /b 1
)

echo.
echo ==========================================
echo   ✅ CONFIGURACION COMPLETADA
echo ==========================================
echo.
echo 🎉 El sistema esta listo para usar!
echo.
echo 📋 Proximos pasos:
echo   1. Abrir: http://localhost:5173
echo   2. Login: juan.diaz@empresa.com / 123456
echo   3. Comenzar a trabajar
echo.
echo 💡 Comandos utiles:
echo   Ver estado:  .\docker-status.bat
echo   Ver logs:    .\docker-logs.bat
echo   Detener:     .\stop-docker.bat
echo.
pause
