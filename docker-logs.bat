@echo off
echo.
echo ==========================================
echo   Logs del Sistema Docker
echo ==========================================
echo.

echo Mostrando logs en tiempo real...
echo Presiona Ctrl+C para salir
echo.

docker-compose logs -f
