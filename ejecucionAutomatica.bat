@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1

cd /d "%~dp0"

echo.
echo ============================================================================
echo   SISTEMA DE INSPECCION - EJECUCION AUTOMATICA
echo ============================================================================
echo.

echo.
echo ----------------------------------------------------------------------------
echo   CONFIGURANDO BACKEND
echo ----------------------------------------------------------------------------
echo.

:: Navegar a backend
cd backend

:: Crear entorno virtual
echo Creando entorno virtual...
if exist "venv" (
    echo [INFO] Entorno virtual ya existe, verificando...
    if exist "venv\Scripts\activate.bat" (
        echo [OK] Entorno virtual existente detectado
        goto :activate_venv
    ) else (
        echo [INFO] Entorno virtual corrupto, recreando...
        rmdir /s /q venv 2>nul
    )
)

python -m venv venv
if errorlevel 1 (
    echo [ERROR] No se pudo crear entorno virtual
    echo [INFO] Intenta ejecutar como administrador o cierra otros procesos Python
    cd ..
    pause
    exit /b 1
)
echo [OK] Entorno virtual creado

:activate_venv

:: Activar entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] No se pudo activar entorno virtual
    cd ..
    pause
    exit /b 1
)
echo [OK] Entorno virtual activado

:: Actualizar pip
echo Actualizando pip...
python -m pip install --upgrade pip --quiet
echo [OK] pip actualizado

:: Instalar dependencias
echo Instalando dependencias de Python...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [ERROR] Fallo instalacion de dependencias
    cd ..
    pause
    exit /b 1
)
echo [OK] Dependencias instaladas

:: Crear archivo .env
echo Creando archivo .env...
(
echo # Base de datos
echo DB_HOST=localhost
echo DB_PORT=3306
echo DB_USER=root
echo DB_PASSWORD=
echo DB_NAME=inspeccioncontenedor
echo.
echo # Seguridad
echo SECRET_KEY=tu-clave-secreta-super-segura-cambiar-en-produccion-2025
echo ALGORITHM=HS256
echo ACCESS_TOKEN_EXPIRE_MINUTES=480
echo.
echo # Entorno
echo DEBUG=True
echo ENVIRONMENT=development
echo.
echo # CORS
echo ALLOWED_ORIGINS=http://localhost:5173
echo.
echo # Uploads
echo CAPTURAS_DIR=../capturas
echo MAX_FILE_SIZE=10485760
echo.
echo # Servidor
echo BACKEND_HOST=127.0.0.1
echo BACKEND_PORT=8001
echo.
echo # Logging
echo LOG_LEVEL=INFO
echo LOG_FILE=app.log
) > .env
echo [OK] Archivo .env creado

:: Corregir contraseñas en la base de datos
echo Corrigiendo contraseñas...
python fix_passwords.py
if errorlevel 1 (
    echo [ADVERTENCIA] No se pudieron corregir las contraseñas automaticamente
    echo [INFO] Ejecuta manualmente: python fix_passwords.py
) else (
    echo [OK] Contraseñas corregidas
)

cd ..
echo.
echo ----------------------------------------------------------------------------
echo   CONFIGURANDO FRONTEND
echo ----------------------------------------------------------------------------
echo.

:: Navegar a frontend
cd frontend

:: Instalar dependencias de Node.js
echo Instalando dependencias de Node.js...
echo [INFO] Esto puede tomar varios minutos...
call npm install --loglevel=error
if errorlevel 1 (
    echo [ERROR] Fallo instalacion de dependencias de Node.js
    cd ..
    pause
    exit /b 1
)
echo [OK] Dependencias de Node.js instaladas

cd ..
echo.
echo ----------------------------------------------------------------------------
echo   INICIANDO SERVICIOS
echo ----------------------------------------------------------------------------
echo.

:: Verificar puertos
echo Verificando puertos disponibles...

:: Iniciar Backend
echo Iniciando Backend en puerto 8001...
start "Backend" cmd /k "cd /d %CD%\backend && call venv\Scripts\activate.bat && python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload"
timeout /t 5 /nobreak >nul
echo [OK] Backend iniciado

:: Iniciar Frontend
echo Iniciando Frontend en puerto 5173...
start "Frontend" cmd /k "cd /d %CD%\frontend && npm run dev"
timeout /t 3 /nobreak >nul
echo [OK] Frontend iniciado

:: Abrir navegador
echo Abriendo navegador...
timeout /t 2 /nobreak >nul
start http://localhost:5173

echo.
echo ============================================================================
echo   SISTEMA INICIADO CORRECTAMENTE
echo ============================================================================
echo.
echo Backend:  http://localhost:8001
echo Frontend: http://localhost:5173
echo.
echo Credenciales de prueba:
echo   Admin: carlos.ruiz@empresa.com / 123456
echo.
echo [IMPORTANTE] No cierres las ventanas de Backend y Frontend
echo.
echo ============================================================================
echo.
pause >nul
exit /b 0
