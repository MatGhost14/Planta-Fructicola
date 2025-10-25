@echo off
echo.
echo ==========================================
echo   Inicializacion de Usuarios de Prueba
echo ==========================================
echo.

echo Verificando si los usuarios ya existen...
docker exec planta-mysql mysql -u planta_user -pplanta_password inspeccioncontenedor -e "SELECT COUNT(*) as total FROM usuarios;" 2>nul | findstr "3" >nul
if not errorlevel 1 (
    echo ✅ Los usuarios de prueba ya estan configurados
    echo.
    echo Usuarios disponibles:
    echo   Inspector:  juan.diaz@empresa.com / 123456
    echo   Supervisor: maria.lopez@empresa.com / 123456
    echo   Admin:      carlos.ruiz@empresa.com / 123456
    echo.
    pause
    exit /b 0
)

echo.
echo ⚠️  Los usuarios de prueba no estan configurados
echo.
echo Esto puede suceder si:
echo   1. Es la primera vez que ejecutas el sistema
echo   2. La base de datos no se inicializo correctamente
echo   3. Los contenedores se crearon sin los datos de prueba
echo.
echo Soluciones:
echo   1. Ejecutar: .\docker-clean.bat
echo   2. Luego: .\start-docker.bat
echo   3. O reiniciar: .\docker-restart.bat
echo.
echo ¿Quieres reiniciar el sistema ahora? (s/N)
set /p restart="Respuesta: "
if /i "%restart%"=="s" (
    echo.
    echo Reiniciando sistema...
    .\docker-restart.bat
) else (
    echo.
    echo Para solucionar manualmente:
    echo   1. .\docker-clean.bat
    echo   2. .\start-docker.bat
)

echo.
pause
