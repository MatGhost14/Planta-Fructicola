#!/usr/bin/env python3
"""
Script para corregir contraseñas en la base de datos
Ejecutar cuando las contraseñas no funcionen después de importar la BD
"""

import pymysql
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def fix_passwords():
    """Corrige las contraseñas en la base de datos"""
    
    # Configuración de conexión desde .env
    connection = pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'inspeccioncontenedor'),
        charset='utf8mb4'
    )
    
    # Hash pre-generado para contraseña "123456" (sin usar passlib)
    password_hash = '$2b$12$KucH7A.w1Lwro8NnNgdU3uh28rlyHoYcKAq6ocQVPup2CSiDi8wNG'
    print(f"Usando hash pre-generado: {password_hash}")
    
    try:
        with connection.cursor() as cursor:
            # Actualizar contraseñas de todos los usuarios
            cursor.execute("""
                UPDATE usuarios 
                SET password_hash = %s 
                WHERE correo IN ('juan.diaz@empresa.com', 'maria.lopez@empresa.com', 'carlos.ruiz@empresa.com')
            """, (password_hash,))
            
            connection.commit()
            print("OK - Contraseñas actualizadas correctamente")
            print("Usuarios actualizados:")
            print("   - juan.diaz@empresa.com (Inspector)")
            print("   - maria.lopez@empresa.com (Supervisor)")
            print("   - carlos.ruiz@empresa.com (Admin)")
            print("Contraseña para todos: 123456")
            
    except Exception as e:
        print(f"ERROR al actualizar contraseñas: {e}")
        connection.rollback()
    finally:
        connection.close()

if __name__ == "__main__":
    print("Corrigiendo contraseñas en la base de datos...")
    fix_passwords()