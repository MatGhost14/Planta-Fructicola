@echo off
echo.
echo ==========================================
echo   Deteniendo Sistema Docker
echo ==========================================
echo.

echo Deteniendo contenedores...
docker-compose down

echo.
echo Limpiando contenedores no utilizados...
docker system prune -f

echo.
echo ==========================================
echo   Sistema Docker detenido correctamente
echo ==========================================
echo.
echo 💡 Para volver a iniciar: .\start-docker.bat
echo.
pause
