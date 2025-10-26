@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1

:: ============================================================================
:: SCRIPT DE INSTALACION Y EJECUCION AUTOMATICA
:: Sistema de Inspeccion de Contenedores Fruticolas
:: ============================================================================

cd /d "%~dp0"

echo.
echo ============================================================================
echo   SISTEMA DE INSPECCION DE CONTENEDORES - INSTALACION AUTOMATICA
echo ============================================================================
echo.

:: ============================================================================
:: PASO 1: VERIFICAR REQUISITOS DEL SISTEMA
:: ============================================================================

echo [1/8] Verificando requisitos del sistema...
echo.

:: Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado
    echo Por favor instala Python 3.8 o superior desde: https://python.org
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% detectado

:: Verificar Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js no esta instalado
    echo Por favor instala Node.js 16 o superior desde: https://nodejs.org
    pause
    exit /b 1
)

for /f "tokens=1" %%i in ('node --version 2^>^&1') do set NODE_VERSION=%%i
echo [OK] Node.js %NODE_VERSION% detectado

:: Verificar npm
npm --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npm no esta instalado
    pause
    exit /b 1
)

for /f "tokens=1" %%i in ('npm --version 2^>^&1') do set NPM_VERSION=%%i
echo [OK] npm %NPM_VERSION% detectado

:: Verificar MySQL
echo.
echo Verificando MySQL...
netstat -ano | findstr :3306 >nul 2>&1
if errorlevel 1 (
    echo [ADVERTENCIA] MySQL no parece estar ejecutandose en puerto 3306
    echo Por favor inicia XAMPP y asegurate de que MySQL este activo
    echo.
    choice /C SN /M "Deseas continuar de todas formas? (S/N)"
    if errorlevel 2 exit /b 1
) else (
    echo [OK] MySQL detectado en puerto 3306
)

echo.
echo ============================================================================
echo   REQUISITOS VERIFICADOS CORRECTAMENTE
echo ============================================================================
echo.
timeout /t 2 /nobreak >nul

:: ============================================================================
:: PASO 2: CONFIGURAR ARCHIVO .ENV
:: ============================================================================

echo [2/8] Configurando archivo .env...
echo.

if exist "backend\.env" (
    echo [INFO] Archivo .env ya existe
    choice /C SN /M "Deseas recrearlo? (S/N)"
    if errorlevel 2 goto :skip_env
)

echo Creando archivo .env...

:: Solicitar datos de configuracion
set DB_HOST=localhost
set DB_PORT=3306
set DB_USER=root
set DB_PASSWORD=
set DB_NAME=inspeccioncontenedor

echo.
echo Configuracion de Base de Datos:
echo --------------------------------
set /p "DB_HOST=Host de MySQL [%DB_HOST%]: " || set DB_HOST=localhost
set /p "DB_PORT=Puerto de MySQL [%DB_PORT%]: " || set DB_PORT=3306
set /p "DB_USER=Usuario de MySQL [%DB_USER%]: " || set DB_USER=root
set /p "DB_PASSWORD=Password de MySQL [vacio]: "
set /p "DB_NAME=Nombre de BD [%DB_NAME%]: " || set DB_NAME=inspeccioncontenedor

:: Generar SECRET_KEY aleatorio
set "SECRET_KEY=secret-key-%RANDOM%%RANDOM%%RANDOM%%RANDOM%-%DATE:/=-%-%TIME::=-%"

:: Crear archivo .env
(
echo # Base de datos
echo DB_HOST=%DB_HOST%
echo DB_PORT=%DB_PORT%
echo DB_USER=%DB_USER%
echo DB_PASSWORD=%DB_PASSWORD%
echo DB_NAME=%DB_NAME%
echo.
echo # Seguridad
echo SECRET_KEY=%SECRET_KEY%
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
) > backend\.env

echo [OK] Archivo .env creado correctamente
goto :after_env

:skip_env
echo [INFO] Usando archivo .env existente

:after_env
echo.
timeout /t 1 /nobreak >nul

:: ============================================================================
:: PASO 3: CREAR DIRECTORIOS NECESARIOS
:: ============================================================================

echo [3/8] Creando directorios necesarios...
echo.

if not exist "capturas" mkdir capturas
if not exist "capturas\inspecciones" mkdir capturas\inspecciones
if not exist "capturas\firmas" mkdir capturas\firmas

echo [OK] Directorios creados

echo.
timeout /t 1 /nobreak >nul

:: ============================================================================
:: PASO 4: VERIFICAR BASE DE DATOS
:: ============================================================================

echo [4/8] Verificando base de datos...
echo.

echo [INFO] Asegurate de que la base de datos '%DB_NAME%' exista
echo [INFO] Si no existe, importa el archivo: database\inspeccioncontenedor.sql
echo.
echo Puedes hacerlo desde phpMyAdmin (http://localhost/phpmyadmin) o con:
echo   mysql -u %DB_USER% -p %DB_NAME% ^< database\inspeccioncontenedor.sql
echo.

choice /C SN /M "La base de datos esta lista? (S/N)"
if errorlevel 2 (
    echo.
    echo [INFO] Por favor configura la base de datos y ejecuta este script nuevamente
    pause
    exit /b 1
)

echo [OK] Base de datos confirmada
echo.
timeout /t 1 /nobreak >nul

:: ============================================================================
:: PASO 5: INSTALAR DEPENDENCIAS DEL BACKEND
:: ============================================================================

echo [5/8] Instalando dependencias del backend...
echo.

cd backend

:: Verificar si existe requirements.txt
if not exist "requirements.txt" (
    echo [ERROR] No se encuentra requirements.txt
    cd ..
    pause
    exit /b 1
)

echo Actualizando pip...
python -m pip install --upgrade pip --quiet

echo Instalando dependencias de Python...
pip install -r requirements.txt --quiet

if errorlevel 1 (
    echo [ERROR] Fallo la instalacion de dependencias de Python
    cd ..
    pause
    exit /b 1
)

echo [OK] Dependencias de Python instaladas

cd ..
echo.
timeout /t 1 /nobreak >nul

:: ============================================================================
:: PASO 6: INSTALAR DEPENDENCIAS DEL FRONTEND
:: ============================================================================

echo [6/8] Instalando dependencias del frontend...
echo.

cd frontend

:: Verificar si existe package.json
if not exist "package.json" (
    echo [ERROR] No se encuentra package.json
    cd ..
    pause
    exit /b 1
)

echo Instalando dependencias de Node.js...
echo [INFO] Esto puede tomar varios minutos...

call npm install --loglevel=error

if errorlevel 1 (
    echo [ERROR] Fallo la instalacion de dependencias de Node.js
    cd ..
    pause
    exit /b 1
)

echo [OK] Dependencias de Node.js instaladas

cd ..
echo.
timeout /t 1 /nobreak >nul

:: ============================================================================
:: PASO 7: VERIFICAR PUERTOS DISPONIBLES
:: ============================================================================

echo [7/8] Verificando puertos disponibles...
echo.

:: Verificar puerto 8001 (Backend)
netstat -ano | findstr :8001 >nul 2>&1
if not errorlevel 1 (
    echo [ADVERTENCIA] Puerto 8001 esta en uso
    echo.
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8001') do (
        set PID=%%a
        goto :found_pid_8001
    )
    :found_pid_8001
    echo Proceso usando puerto 8001: PID !PID!
    choice /C SN /M "Deseas terminar este proceso? (S/N)"
    if not errorlevel 2 (
        taskkill /F /PID !PID! >nul 2>&1
        echo [OK] Proceso terminado
    )
) else (
    echo [OK] Puerto 8001 disponible
)

:: Verificar puerto 5173 (Frontend)
netstat -ano | findstr :5173 >nul 2>&1
if not errorlevel 1 (
    echo [ADVERTENCIA] Puerto 5173 esta en uso
    echo.
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5173') do (
        set PID=%%a
        goto :found_pid_5173
    )
    :found_pid_5173
    echo Proceso usando puerto 5173: PID !PID!
    choice /C SN /M "Deseas terminar este proceso? (S/N)"
    if not errorlevel 2 (
        taskkill /F /PID !PID! >nul 2>&1
        echo [OK] Proceso terminado
    )
) else (
    echo [OK] Puerto 5173 disponible
)

echo.
timeout /t 1 /nobreak >nul

:: ============================================================================
:: PASO 8: INICIAR SERVICIOS
:: ============================================================================

echo [8/8] Iniciando servicios...
echo.

:: Iniciar Backend
echo Iniciando Backend en puerto 8001...
start "Backend - Sistema Inspeccion" cmd /k "cd /d "%CD%\backend" && python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload"

:: Esperar a que el backend inicie
echo Esperando que el backend inicie...
timeout /t 8 /nobreak >nul

:: Iniciar Frontend
echo Iniciando Frontend en puerto 5173...
start "Frontend - Sistema Inspeccion" cmd /k "cd /d "%CD%\frontend" && npm run dev"

:: Esperar a que el frontend inicie
echo Esperando que el frontend inicie...
timeout /t 5 /nobreak >nul

:: Abrir navegador
echo Abriendo navegador...
timeout /t 3 /nobreak >nul
start http://localhost:5173

echo.
echo ============================================================================
echo   SISTEMA INICIADO CORRECTAMENTE
echo ============================================================================
echo.
echo Backend:  http://localhost:8001
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8001/docs
echo.
echo Credenciales de prueba:
echo   Admin:      carlos.ruiz@empresa.com / 123456
echo   Supervisor: maria.lopez@empresa.com / 123456
echo   Inspector:  juan.diaz@empresa.com / 123456
echo.
echo [INFO] Se han abierto dos ventanas adicionales:
echo   - Backend (puerto 8001)
echo   - Frontend (puerto 5173)
echo.
echo [INFO] NO cierres esas ventanas mientras uses el sistema
echo.
echo ============================================================================
echo.
echo Presiona cualquier tecla para cerrar esta ventana...
pause >nul
exit /b 0