@echo off
echo.
echo ==========================================
echo   Sistema Docker - Inspeccion Contenedores
echo ==========================================
echo.

echo Verificando Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker no encontrado
    echo Por favor instala Docker Desktop desde https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)
echo ✓ Docker encontrado

echo.
echo Construyendo y ejecutando contenedores...
docker-compose up --build -d

echo.
echo Esperando que los servicios se inicien...
timeout /t 10 /nobreak >nul

echo.
echo ==========================================
echo   Sistema iniciado en Docker!
echo ==========================================
echo.
echo ✓ Backend API:    http://localhost:8000
echo ✓ API Docs:      http://localhost:8000/docs
echo ✓ Frontend:      http://localhost:5173
echo ✓ MySQL:         localhost:3306
echo.
echo 🔑 Credenciales de prueba:
echo   Inspector:  juan.diaz@empresa.com / password123
echo   Supervisor: maria.lopez@empresa.com / password123
echo   Admin:      carlos.ruiz@empresa.com / password123
echo.
echo 💡 Comandos útiles:
echo   Ver logs:        docker-compose logs -f
echo   Detener:         docker-compose down
echo   Reiniciar:       docker-compose restart
echo.
echo Presiona cualquier tecla para salir...
pause >nul
