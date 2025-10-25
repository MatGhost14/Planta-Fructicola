"""Script sencillo para esperar a que la base de datos MySQL acepte conexiones.

Este script lee las variables de entorno DB_HOST, DB_PORT, DB_USER, DB_PASSWORD y
trata de abrir una conexión con pymysql. Reintenta durante un periodo antes de
fallar con error no cero — esto evita que el backend intente iniciar antes de
que el contenedor MySQL esté listo.

Uso: se ejecuta automáticamente desde el Dockerfile antes de arrancar uvicorn.
"""
import os
import time
import sys
import pymysql


def wait_for_db(retries=30, delay=2):
    host = os.getenv("DB_HOST", "localhost")
    port = int(os.getenv("DB_PORT", 3306))
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    db = os.getenv("DB_NAME", "inspeccioncontenedor")

    attempt = 0
    while attempt < retries:
        try:
            print(f"[wait_for_db] Intento {attempt+1}/{retries} -> conectando a {host}:{port}...")
            conn = pymysql.connect(host=host, port=port, user=user, password=password, database=db, connect_timeout=5)
            conn.close()
            print("[wait_for_db] Conexión OK")
            return 0
        except Exception as e:
            print(f"[wait_for_db] No disponible ({e}), reintentando en {delay}s...")
            attempt += 1
            time.sleep(delay)

    print(f"[wait_for_db] Error: No se pudo conectar a la base de datos en {host}:{port} después de {retries} intentos")
    return 1


if __name__ == "__main__":
    exit_code = wait_for_db()
    sys.exit(exit_code)
