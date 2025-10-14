"""Utilidades para manejo de archivos"""
import os
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Tuple
from fastapi import UploadFile


def ensure_dir(directory: str) -> None:
    """Crea directorio si no existe"""
    Path(directory).mkdir(parents=True, exist_ok=True)


def generate_unique_filename(original_filename: str, prefix: str = "") -> str:
    """Genera nombre único para archivo"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    extension = Path(original_filename).suffix
    if prefix:
        return f"{prefix}_{timestamp}{extension}"
    return f"{timestamp}{extension}"


def calculate_file_hash(file_content: bytes) -> str:
    """Calcula hash SHA256 de archivo"""
    return hashlib.sha256(file_content).hexdigest()


async def save_upload_file(
    upload_file: UploadFile,
    destination_dir: str,
    filename: str = None
) -> Tuple[str, str, str]:
    """
    Guarda archivo subido y retorna (ruta_completa, ruta_relativa, hash)
    """
    ensure_dir(destination_dir)
    
    # Nombre de archivo
    if not filename:
        filename = generate_unique_filename(upload_file.filename)
    
    # Leer contenido
    content = await upload_file.read()
    
    # Calcular hash
    file_hash = calculate_file_hash(content)
    
    # Guardar archivo
    full_path = os.path.join(destination_dir, filename)
    with open(full_path, "wb") as f:
        f.write(content)
    
    # Ruta relativa para BD (debe empezar con /capturas)
    relative_path = full_path.replace("\\", "/").split("capturas/")[-1]
    relative_path = f"/capturas/{relative_path}"
    
    return full_path, relative_path, file_hash


def delete_file_safe(file_path: str) -> bool:
    """Elimina archivo de forma segura"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        print(f"Error al eliminar archivo {file_path}: {e}")
        return False


def get_mime_type(filename: str) -> str:
    """Determina MIME type basado en extensión"""
    extension = Path(filename).suffix.lower()
    mime_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp"
    }
    return mime_types.get(extension, "application/octet-stream")
