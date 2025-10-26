#!/bin/bash
set -e

echo "=========================================="
echo "  Backend Initialization Script"
echo "=========================================="
echo ""

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Función para esperar a que MySQL esté listo
wait_for_mysql() {
    echo -e "${YELLOW}⏳ Esperando a que MySQL esté disponible...${NC}"
    
    MAX_TRIES=30
    COUNT=0
    
    while [ $COUNT -lt $MAX_TRIES ]; do
        if python -c "
import pymysql
import sys
import os
from urllib.parse import urlparse

db_url = os.environ.get('DATABASE_URL', '')
parsed = urlparse(db_url.replace('mysql://', 'mysql+pymysql://'))

try:
    conn = pymysql.connect(
        host=parsed.hostname,
        port=parsed.port or 3306,
        user=parsed.username,
        password=parsed.password,
        database=parsed.path[1:] if parsed.path else None
    )
    conn.close()
    sys.exit(0)
except Exception as e:
    sys.exit(1)
" 2>/dev/null; then
            echo -e "${GREEN}✓ MySQL está listo!${NC}"
            return 0
        fi
        
        COUNT=$((COUNT + 1))
        echo -e "${YELLOW}  Intento $COUNT/$MAX_TRIES - Esperando...${NC}"
        sleep 2
    done
    
    echo -e "${RED}✗ ERROR: MySQL no respondió después de $MAX_TRIES intentos${NC}"
    exit 1
}

# Función para verificar si la base de datos está inicializada
check_database_initialized() {
    echo -e "${YELLOW}🔍 Verificando estado de la base de datos...${NC}"
    
    TABLES_COUNT=$(python -c "
import pymysql
import os
from urllib.parse import urlparse

db_url = os.environ.get('DATABASE_URL', '')
parsed = urlparse(db_url.replace('mysql://', 'mysql+pymysql://'))

try:
    conn = pymysql.connect(
        host=parsed.hostname,
        port=parsed.port or 3306,
        user=parsed.username,
        password=parsed.password,
        database=parsed.path[1:] if parsed.path else None
    )
    cursor = conn.cursor()
    cursor.execute('SHOW TABLES')
    tables = cursor.fetchall()
    print(len(tables))
    conn.close()
except Exception as e:
    print('0')
" 2>/dev/null)
    
    if [ "$TABLES_COUNT" -gt "5" ]; then
        echo -e "${GREEN}✓ Base de datos ya está inicializada ($TABLES_COUNT tablas encontradas)${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠ Base de datos parece estar vacía o incompleta ($TABLES_COUNT tablas)${NC}"
        return 1
    fi
}

# Esperar a MySQL
wait_for_mysql

# Verificar estado de la BD
check_database_initialized

# Pequeña pausa adicional para asegurar que MySQL esté completamente listo
echo -e "${YELLOW}⏳ Esperando estabilización del servicio...${NC}"
sleep 3

echo ""
echo -e "${GREEN}=========================================="
echo "  ✓ Inicialización completada"
echo "==========================================${NC}"
echo ""

# Ejecutar el comando principal (uvicorn)
exec "$@"

