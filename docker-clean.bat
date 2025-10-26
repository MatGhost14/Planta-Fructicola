@echo off
echo.
echo ==========================================
echo   Limpieza Completa del Sistema Docker
echo ==========================================
echo.
echo ⚠️  ADVERTENCIA: Esto eliminara todos los datos!
echo.

set /p confirm="¿Estas seguro? (s/N): "
if /i not "%confirm%"=="s" (
    echo Operacion cancelada.
    pause
    exit /b 0
)

echo.
echo Deteniendo y eliminando contenedores...
docker-compose down -v

echo.
echo Eliminando imagenes...
docker-compose down --rmi all

echo.
echo Limpiando sistema Docker...
docker system prune -af

echo.
echo Eliminando archivos de capturas...
if exist "capturas\inspecciones" rmdir /s /q "capturas\inspecciones"
if exist "capturas\firmas" rmdir /s /q "capturas\firmas"
mkdir "capturas\inspecciones" 2>nul
mkdir "capturas\firmas" 2>nul

echo.
echo ==========================================
echo   Limpieza completada!
echo ==========================================
echo.
echo 💡 Para iniciar de nuevo: .\start-docker.bat
echo.
pause
