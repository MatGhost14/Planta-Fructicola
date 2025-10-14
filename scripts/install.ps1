# Script de instalacion completa
# Uso: .\install.ps1

Write-Host "Instalacion del Sistema de Inspeccion de Contenedores" -ForegroundColor Green
Write-Host "=========================================================" -ForegroundColor Green
Write-Host ""

# Verificar Node.js
Write-Host "Verificando Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "Node.js instalado: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Node.js no esta instalado. Descargalo desde https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Verificar Python
Write-Host "Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "Python instalado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python no esta instalado. Descargalo desde https://www.python.org/" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Instalando dependencias del Backend..." -ForegroundColor Cyan
Write-Host ""

cd backend

# Crear entorno virtual
if (-not (Test-Path "venv")) {
    Write-Host "Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "Entorno virtual creado" -ForegroundColor Green
}

# Activar y instalar dependencias
Write-Host "Instalando dependencias Python desde requirements.txt..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1
pip install -r ..\requirements.txt
Write-Host "Dependencias Python instaladas" -ForegroundColor Green

# Crear .env si no existe
if (-not (Test-Path ".env")) {
    Write-Host "Creando archivo .env..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "IMPORTANTE: Edita backend/.env con tus credenciales de MySQL" -ForegroundColor Yellow
}

cd ..

Write-Host ""
Write-Host "Instalando dependencias del Frontend..." -ForegroundColor Magenta
Write-Host ""

cd frontend
npm install
Write-Host "Dependencias npm instaladas" -ForegroundColor Green

cd ..

Write-Host ""
Write-Host "Instalacion completada!" -ForegroundColor Green
Write-Host ""
Write-Host "Proximos pasos:" -ForegroundColor White
Write-Host "1. Iniciar MySQL en XAMPP" -ForegroundColor Gray
Write-Host "2. Importar ImpeccionContenedor.sql en phpMyAdmin" -ForegroundColor Gray
Write-Host "3. Editar backend\.env con tus credenciales" -ForegroundColor Gray
Write-Host "4. Ejecutar migraciones: cd backend; .\venv\Scripts\Activate.ps1; alembic upgrade head" -ForegroundColor Gray
Write-Host "5. Iniciar servicios: .\start-dev.ps1" -ForegroundColor Gray
Write-Host ""
