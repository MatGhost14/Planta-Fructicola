# Script para Backup Automático de MySQL
# Crea backup diario de la base de datos

param(
    [string]$BackupDir = "C:\backups\inspeccion",
    [string]$DBName = "ImpeccionContenedor",
    [string]$DBUser = "root",
    [string]$DBPassword = "",
    [int]$RetainDays = 7
)

# Crear directorio de backups si no existe
if (!(Test-Path $BackupDir)) {
    New-Item -Path $BackupDir -ItemType Directory -Force | Out-Null
    Write-Host "✅ Directorio de backups creado: $BackupDir"
}

# Nombre del archivo con timestamp
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupFile = Join-Path $BackupDir "${DBName}_${timestamp}.sql"

Write-Host "🔄 Iniciando backup de base de datos..."
Write-Host "  Base de datos: $DBName"
Write-Host "  Archivo: $backupFile"

# Ejecutar mysqldump
try {
    $mysqldumpPath = "mysqldump"
    
    if ($DBPassword) {
        & $mysqldumpPath -u $DBUser -p$DBPassword --databases $DBName --result-file=$backupFile
    } else {
        & $mysqldumpPath -u $DBUser --databases $DBName --result-file=$backupFile
    }
    
    if ($LASTEXITCODE -eq 0) {
        $fileSize = (Get-Item $backupFile).Length / 1MB
        Write-Host "✅ Backup completado exitosamente"
        Write-Host "  Tamaño: $([math]::Round($fileSize, 2)) MB"
        
        # Eliminar backups antiguos
        Write-Host "`n🧹 Limpiando backups antiguos (> $RetainDays días)..."
        $cutoffDate = (Get-Date).AddDays(-$RetainDays)
        $oldBackups = Get-ChildItem -Path $BackupDir -Filter "*.sql" | Where-Object { $_.LastWriteTime -lt $cutoffDate }
        
        if ($oldBackups) {
            $oldBackups | ForEach-Object {
                Write-Host "  Eliminando: $($_.Name)"
                Remove-Item $_.FullName -Force
            }
            Write-Host "✅ $($oldBackups.Count) backups antiguos eliminados"
        } else {
            Write-Host "  No hay backups antiguos para eliminar"
        }
        
        # Registrar en log
        $logFile = Join-Path $BackupDir "backup.log"
        $logEntry = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - Backup exitoso: $backupFile ($([math]::Round($fileSize, 2)) MB)"
        Add-Content -Path $logFile -Value $logEntry
        
        Write-Host "`n✅ Proceso completado"
    } else {
        throw "mysqldump falló con código de error $LASTEXITCODE"
    }
    
} catch {
    Write-Host "❌ ERROR: $_"
    $logFile = Join-Path $BackupDir "backup.log"
    $logEntry = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - ERROR: $_"
    Add-Content -Path $logFile -Value $logEntry
    exit 1
}
