@echo off
echo.
echo ==========================================
echo   RESET - Sistema de Inspeccion
echo ==========================================
echo.
echo ⚠️  ADVERTENCIA: Este script eliminará:
echo    - Todos los contenedores del sistema
echo    - El volumen de la base de datos (mysql_data)
echo    - Caché de imágenes Docker
echo.
echo    Esto es útil cuando:
echo    - Actualizas la estructura de la BD
echo    - Tienes problemas de sincronización
echo    - Quieres empezar desde cero
echo.
set /p CONFIRM="¿Estás seguro? (escribe SI para continuar): "
if /i not "%CONFIRM%"=="SI" (
    echo.
    echo ❌ Operación cancelada
    echo.
    pause
    exit /b 0
)

echo.
echo 🛑 Deteniendo contenedores...
docker-compose down

echo.
echo 🗑️  Eliminando volumen de base de datos...
docker volume rm planta-_mysql_data 2>nul
if errorlevel 1 (
    echo ⚠️  El volumen no existía o ya fue eliminado
) else (
    echo ✓ Volumen eliminado
)

echo.
echo 🧹 Limpiando sistema Docker...
docker system prune -f

echo.
echo ==========================================
echo   ✓ Reset completado
echo ==========================================
echo.
echo 💡 Siguiente paso:
echo    Ejecuta start-docker.bat para reconstruir
echo    el sistema desde cero
echo.
pause

