@echo off
echo.
echo ==========================================
echo   Modo Desarrollo Docker
echo ==========================================
echo.

echo Verificando que Docker este ejecutandose...
docker ps >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker no esta ejecutandose
    echo Por favor inicia Docker Desktop primero
    pause
    exit /b 1
)

echo.
echo Iniciando en modo desarrollo...
echo Esto montara los directorios locales para desarrollo en tiempo real
echo.

echo Deteniendo contenedores anteriores...
docker-compose down >nul 2>&1

echo.
echo Iniciando solo la base de datos...
docker-compose up -d mysql

echo.
echo Esperando que MySQL este listo...
timeout /t 10 /nobreak >nul

echo.
echo ==========================================
echo   Modo Desarrollo Activo
echo ==========================================
echo.
echo ✓ MySQL:         localhost:3307
echo ✓ Base de datos:  inspeccioncontenedor
echo.
echo Para iniciar el backend en desarrollo:
echo   cd backend
echo   python -m venv venv
echo   .\venv\Scripts\Activate.ps1
echo   pip install -r requirements.txt
echo   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
echo.
echo Para iniciar el frontend en desarrollo:
echo   cd frontend
echo   npm install
echo   npm run dev -- --port 5173
echo.
echo 💡 Comandos utiles:
echo   Ver logs BD:    docker logs planta-mysql
echo   Detener BD:     docker-compose stop mysql
echo   Reiniciar BD:   docker-compose restart mysql
echo.
pause
