"""
Script para crear usuarios de prueba con contraseñas hasheadas
"""
from passlib.context import CryptContext
import pymysql
import sys

# Configuración
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Contraseña para todos los usuarios
PASSWORD = "password123"
PASSWORD_HASH = pwd_context.hash(PASSWORD)

print(f"Hash de contraseña generado: {PASSWORD_HASH[:50]}...")

# Usuarios a crear
usuarios = [
    {
        "nombre": "Juan Inspector",
        "correo": "inspector@empresa.com",
        "rol": "inspector",
        "estado": "active"
    },
    {
        "nombre": "Carlos Supervisor", 
        "correo": "supervisor@empresa.com",
        "rol": "supervisor",
        "estado": "active"
    },
    {
        "nombre": "Administrador Sistema",
        "correo": "admin@empresa.com",
        "rol": "admin",
        "estado": "active"
    }
]

try:
    # Conectar a MySQL
    conexion = pymysql.connect(
        host='localhost',
        user='root',
        password='',  # Cambiar si tienes contraseña en XAMPP
        database='inspecciocontenedor',
        charset='utf8mb4'
    )
    
    cursor = conexion.cursor()
    
    print("\nConectado a la base de datos 'inspecciocontenedor'")
    
    # Actualizar usuarios existentes sin contraseña
    cursor.execute("""
        UPDATE usuarios 
        SET password_hash = %s
        WHERE password_hash IS NULL OR password_hash = ''
    """, (PASSWORD_HASH,))
    
    actualizados = cursor.rowcount
    print(f"\n✓ {actualizados} usuarios existentes actualizados con contraseña")
    
    # Crear usuarios de prueba si no existen
    for usuario in usuarios:
        # Verificar si ya existe
        cursor.execute("SELECT id_usuario FROM usuarios WHERE correo = %s", (usuario['correo'],))
        existe = cursor.fetchone()
        
        if existe:
            # Actualizar
            cursor.execute("""
                UPDATE usuarios 
                SET nombre = %s, password_hash = %s, rol = %s, estado = %s
                WHERE correo = %s
            """, (usuario['nombre'], PASSWORD_HASH, usuario['rol'], usuario['estado'], usuario['correo']))
            print(f"✓ Usuario actualizado: {usuario['correo']} ({usuario['rol']})")
        else:
            # Insertar
            cursor.execute("""
                INSERT INTO usuarios (nombre, correo, password_hash, rol, estado)
                VALUES (%s, %s, %s, %s, %s)
            """, (usuario['nombre'], usuario['correo'], PASSWORD_HASH, usuario['rol'], usuario['estado']))
            print(f"✓ Usuario creado: {usuario['correo']} ({usuario['rol']})")
    
    # Confirmar cambios
    conexion.commit()
    
    # Verificar usuarios creados
    print("\n" + "="*60)
    print("USUARIOS DE PRUEBA CREADOS:")
    print("="*60)
    
    cursor.execute("""
        SELECT id_usuario, nombre, correo, rol, estado 
        FROM usuarios 
        WHERE correo IN ('inspector@empresa.com', 'supervisor@empresa.com', 'admin@empresa.com')
        ORDER BY 
            CASE rol 
                WHEN 'inspector' THEN 1 
                WHEN 'supervisor' THEN 2 
                WHEN 'admin' THEN 3 
            END
    """)
    
    for fila in cursor.fetchall():
        id_usuario, nombre, correo, rol, estado = fila
        print(f"\nID: {id_usuario}")
        print(f"  Nombre: {nombre}")
        print(f"  Correo: {correo}")
        print(f"  Rol: {rol}")
        print(f"  Estado: {estado}")
        print(f"  Contraseña: {PASSWORD}")
    
    print("\n" + "="*60)
    print("✅ Usuarios de prueba configurados correctamente")
    print("="*60)
    
    cursor.close()
    conexion.close()
    
except pymysql.Error as e:
    print(f"\n❌ Error de MySQL: {e}")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Error: {e}")
    sys.exit(1)
