# Script para configurar la base de datos
# Uso: .\setup-database.ps1

Write-Host "Configuracion de Base de Datos" -ForegroundColor Green
Write-Host "===============================" -ForegroundColor Green
Write-Host ""

# Verificar que MySQL este corriendo
Write-Host "Verificando MySQL..." -ForegroundColor Yellow
$mysqlRunning = Get-Process mysqld -ErrorAction SilentlyContinue
if (-not $mysqlRunning) {
    Write-Host "ERROR: MySQL no esta corriendo." -ForegroundColor Red
    Write-Host "Por favor, inicia XAMPP y arranca el servicio MySQL primero." -ForegroundColor Yellow
    exit 1
}
Write-Host "MySQL esta corriendo" -ForegroundColor Green
Write-Host ""

# Leer credenciales del .env
Write-Host "Leyendo credenciales de backend\.env..." -ForegroundColor Yellow
$envContent = Get-Content backend\.env
$dbUser = ($envContent | Where-Object { $_ -match "^DB_USER=" }) -replace "DB_USER=", ""
$dbPassword = ($envContent | Where-Object { $_ -match "^DB_PASSWORD=" }) -replace "DB_PASSWORD=", ""
$dbName = ($envContent | Where-Object { $_ -match "^DB_NAME=" }) -replace "DB_NAME=", ""

Write-Host "Usuario: $dbUser" -ForegroundColor Cyan
Write-Host "Base de datos: $dbName" -ForegroundColor Cyan
Write-Host ""

# Ruta al mysql.exe de XAMPP
$mysqlPath = "C:\xampp\mysql\bin\mysql.exe"
if (-not (Test-Path $mysqlPath)) {
    Write-Host "No se encontro MySQL en $mysqlPath" -ForegroundColor Yellow
    $mysqlPath = Read-Host "Ingresa la ruta completa a mysql.exe"
}

# Importar base de datos
Write-Host "Importando base de datos desde ImpeccionContenedor.sql..." -ForegroundColor Yellow

if ($dbPassword -eq "") {
    # Sin contrasena
    & $mysqlPath -u $dbUser -e "CREATE DATABASE IF NOT EXISTS $dbName CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    & $mysqlPath -u $dbUser $dbName < ImpeccionContenedor.sql
} else {
    # Con contrasena
    & $mysqlPath -u $dbUser -p$dbPassword -e "CREATE DATABASE IF NOT EXISTS $dbName CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    & $mysqlPath -u $dbUser -p$dbPassword $dbName < ImpeccionContenedor.sql
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "Base de datos importada correctamente" -ForegroundColor Green
} else {
    Write-Host "ERROR: Hubo un problema al importar la base de datos" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Ejecutando migraciones de Alembic..." -ForegroundColor Yellow
cd backend
.\venv\Scripts\Activate.ps1
alembic upgrade head

if ($LASTEXITCODE -eq 0) {
    Write-Host "Migraciones ejecutadas correctamente" -ForegroundColor Green
} else {
    Write-Host "ERROR: Hubo un problema al ejecutar las migraciones" -ForegroundColor Red
    cd ..
    exit 1
}

cd ..

Write-Host ""
Write-Host "Base de datos configurada correctamente!" -ForegroundColor Green
Write-Host ""
Write-Host "Proximo paso:" -ForegroundColor White
Write-Host "Ejecutar: .\start-dev.ps1" -ForegroundColor Cyan
Write-Host ""
