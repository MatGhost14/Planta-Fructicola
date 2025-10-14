# Script PowerShell para iniciar backend y frontend simultaneamente
# Uso: .\start-dev.ps1

Write-Host "Iniciando Sistema de Inspeccion de Contenedores..." -ForegroundColor Green
Write-Host ""

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "backend") -or -not (Test-Path "frontend")) {
    Write-Host "Error: Ejecutar desde la raiz del proyecto (donde estan las carpetas backend/ y frontend/)" -ForegroundColor Red
    exit 1
}

# Verificar MySQL
Write-Host "Verificando MySQL..." -ForegroundColor Yellow
$mysqlRunning = Get-Process mysqld -ErrorAction SilentlyContinue
if (-not $mysqlRunning) {
    Write-Host "MySQL no esta corriendo. Asegurate de iniciar XAMPP primero." -ForegroundColor Yellow
    $continue = Read-Host "Continuar de todas formas? (s/n)"
    if ($continue -ne "s") {
        exit 0
    }
}

Write-Host ""
Write-Host "Iniciando servicios..." -ForegroundColor Cyan
Write-Host ""

# Iniciar Backend
Write-Host "Iniciando Backend (FastAPI)..." -ForegroundColor Blue
Start-Process powershell -ArgumentList @"
    -NoExit
    -Command
    cd '$PWD\backend';
    Write-Host 'Backend FastAPI' -ForegroundColor Blue;
    Write-Host '==================' -ForegroundColor Blue;
    Write-Host '';
    if (Test-Path 'venv\Scripts\Activate.ps1') {
        .\venv\Scripts\Activate.ps1;
        Write-Host 'Virtual environment activado' -ForegroundColor Green;
    } else {
        Write-Host 'No se encontro venv. Ejecutar: python -m venv venv' -ForegroundColor Yellow;
    }
    Write-Host 'Iniciando Uvicorn en http://localhost:8000' -ForegroundColor Cyan;
    Write-Host 'API Docs: http://localhost:8000/docs' -ForegroundColor Cyan;
    Write-Host '';
    uvicorn app.main:app --reload --port 8000
"@

Start-Sleep -Seconds 2

# Iniciar Frontend
Write-Host "Iniciando Frontend (React + Vite)..." -ForegroundColor Magenta
Start-Process powershell -ArgumentList @"
    -NoExit
    -Command
    cd '$PWD\frontend';
    Write-Host 'Frontend React + Vite' -ForegroundColor Magenta;
    Write-Host '=======================' -ForegroundColor Magenta;
    Write-Host '';
    Write-Host 'Iniciando Vite dev server en http://localhost:5173' -ForegroundColor Cyan;
    Write-Host '';
    npm run dev
"@

Write-Host ""
Write-Host "Servicios iniciados!" -ForegroundColor Green
Write-Host ""
Write-Host "URLs:" -ForegroundColor White
Write-Host "   Frontend:  http://localhost:5173" -ForegroundColor Cyan
Write-Host "   Backend:   http://localhost:8000" -ForegroundColor Cyan
Write-Host "   API Docs:  http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Presiona Ctrl+C en cada ventana para detener los servicios." -ForegroundColor Gray
