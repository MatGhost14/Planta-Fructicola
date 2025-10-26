@echo off
echo.
echo ==========================================
echo   Reiniciando Sistema Docker
echo ==========================================
echo.

echo Deteniendo contenedores...
docker-compose down

echo.
echo Esperando 5 segundos...
timeout /t 5 /nobreak >nul

echo.
echo Iniciando contenedores...
docker-compose up -d

if errorlevel 1 (
    echo ERROR: Fallo al reiniciar los contenedores
    pause
    exit /b 1
)

echo.
echo Esperando que los servicios esten listos...
timeout /t 15 /nobreak >nul

echo.
echo ==========================================
echo   Sistema reiniciado correctamente!
echo ==========================================
echo.
echo ✓ Backend API:    http://localhost:8000
echo ✓ Frontend:      http://localhost:5173
echo.
echo 💡 Para ver logs: .\docker-logs.bat
echo.
pause
