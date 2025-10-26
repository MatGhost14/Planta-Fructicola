"""
Script para crear usuario administrador con contraseña segura
Valida política de contraseñas y elimina usuarios de prueba
"""
import sys
import os
import re
from getpass import getpass

# Agregar el directorio padre al path para importar app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models import Usuario
from app.utils.auth import get_password_hash
from datetime import datetime


def validar_contrasena(password: str) -> tuple[bool, str]:
    """
    Valida que la contraseña cumpla con la política de seguridad
    
    Requisitos:
    - Mínimo 8 caracteres
    - Al menos 1 mayúscula
    - Al menos 1 minúscula
    - Al menos 1 número
    - Al menos 1 símbolo especial
    """
    if len(password) < 8:
        return False, "X La contraseña debe tener al menos 8 caracteres"
    
    if not re.search(r'[A-Z]', password):
        return False, "X La contraseña debe contener al menos una mayúscula"
    
    if not re.search(r'[a-z]', password):
        return False, "X La contraseña debe contener al menos una minúscula"
    
    if not re.search(r'[0-9]', password):
        return False, "X La contraseña debe contener al menos un número"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "X La contraseña debe contener al menos un símbolo especial (!@#$%^&*...)"
    
    return True, "OK Contraseña válida"


def validar_correo(email: str) -> bool:
    """Valida formato de correo electrónico"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def eliminar_usuarios_prueba(db: Session):
    """Elimina usuarios de prueba del sistema"""
    print("\nBuscando usuarios de prueba...")
    
    usuarios_prueba = db.query(Usuario).filter(
        Usuario.correo.in_([
            'inspector@empresa.com',
            'supervisor@empresa.com',
            'admin@empresa.com'
        ])
    ).all()
    
    if not usuarios_prueba:
        print("OK No se encontraron usuarios de prueba")
        return
    
    print(f"\n! Se encontraron {len(usuarios_prueba)} usuarios de prueba:")
    for u in usuarios_prueba:
        print(f"  - {u.correo} ({u.rol})")
    
    respuesta = input("\n¿Desea eliminarlos? (s/n): ").lower().strip()
    
    if respuesta == 's':
        for usuario in usuarios_prueba:
            db.delete(usuario)
        db.commit()
        print(f"OK {len(usuarios_prueba)} usuarios de prueba eliminados")
    else:
        print("SALTAR Usuarios de prueba conservados")


def crear_admin():
    """Función principal para crear administrador"""
    print("=" * 60)
    print("CREACION DE USUARIO ADMINISTRADOR")
    print("=" * 60)
    
    # Conectar a BD
    db = SessionLocal()
    
    try:
        # Paso 1: Eliminar usuarios de prueba (opcional)
        eliminar_usuarios_prueba(db)
        
        print("\n" + "=" * 60)
        print("CREAR NUEVO ADMINISTRADOR")
        print("=" * 60)
        
        # Paso 2: Solicitar datos del nuevo admin
        while True:
            nombre = input("\nNombre completo: ").strip()
            if len(nombre) >= 3:
                break
            print("X El nombre debe tener al menos 3 caracteres")
        
        while True:
            correo = input("Correo electrónico: ").strip().lower()
            if not validar_correo(correo):
                print("X Formato de correo inválido")
                continue
            
            # Verificar que no exista
            usuario_existe = db.query(Usuario).filter(Usuario.correo == correo).first()
            if usuario_existe:
                print(f"X Ya existe un usuario con el correo {correo}")
                continue
            
            break
        
        # Paso 3: Solicitar contraseña segura
        print("\nPolítica de contraseñas:")
        print("  • Mínimo 8 caracteres")
        print("  • Al menos 1 mayúscula (A-Z)")
        print("  • Al menos 1 minúscula (a-z)")
        print("  • Al menos 1 número (0-9)")
        print("  • Al menos 1 símbolo especial (!@#$%...)")
        
        while True:
            password = getpass("\nContraseña: ")
            valida, mensaje = validar_contrasena(password)
            
            if not valida:
                print(mensaje)
                continue
            
            password_confirm = getpass("Confirmar contraseña: ")
            
            if password != password_confirm:
                print("X Las contraseñas no coinciden")
                continue
            
            print(mensaje)
            break
        
        # Paso 4: Crear usuario admin
        print("\nCreando usuario administrador...")
        
        nuevo_admin = Usuario(
            nombre=nombre,
            correo=correo,
            password_hash=get_password_hash(password),
            rol='admin',
            estado='active',
            creado_en=datetime.utcnow(),
            actualizado_en=datetime.utcnow()
        )
        
        db.add(nuevo_admin)
        db.commit()
        db.refresh(nuevo_admin)
        
        print("\n" + "=" * 60)
        print("OK ADMINISTRADOR CREADO EXITOSAMENTE!")
        print("=" * 60)
        print(f"\nCorreo: {nuevo_admin.correo}")
        print(f"Nombre: {nuevo_admin.nombre}")
        print(f"Rol: {nuevo_admin.rol}")
        print(f"Estado: {nuevo_admin.estado}")
        print(f"\nYa puedes iniciar sesión con estas credenciales")
        print("=" * 60)
        
    except Exception as e:
        db.rollback()
        print(f"\nX ERROR: {str(e)}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    try:
        crear_admin()
    except KeyboardInterrupt:
        print("\n\n! Operación cancelada por el usuario")
        sys.exit(0)
