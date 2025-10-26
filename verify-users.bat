@echo off
echo.
echo ==========================================
echo   Verificacion de Usuarios de Prueba
echo ==========================================
echo.

echo Verificando usuarios en la base de datos...
docker exec planta-mysql mysql -u planta_user -pplanta_password inspeccioncontenedor -e "SELECT id_usuario, nombre, correo, rol FROM usuarios ORDER BY id_usuario;"

echo.
echo Verificando que las contraseñas funcionen...
echo Probando login con juan.diaz@empresa.com...

curl -s -X POST http://localhost:8000/api/auth/login -H "Content-Type: application/json" -d "{\"correo\":\"juan.diaz@empresa.com\",\"password\":\"123456\"}" >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: No se pudo conectar al backend
    echo Verifica que el backend este ejecutandose en http://localhost:8000
) else (
    echo ✅ Backend respondiendo correctamente
)

echo.
echo ==========================================
echo   Verificacion completada
echo ==========================================
echo.
echo 💡 Si hay problemas:
echo   1. Verifica que todos los servicios esten corriendo: .\docker-status.bat
echo   2. Reinicia el sistema: .\docker-restart.bat
echo   3. Limpia y reinicia: .\docker-clean.bat && .\start-docker.bat
echo.
pause
