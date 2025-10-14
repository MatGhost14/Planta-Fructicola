-- Script para crear usuarios de prueba con autenticación
-- Contraseña para todos: password123
-- Hash generado con bcrypt (rounds=12)

USE impeccioncontenedor;

-- Actualizar usuarios existentes con contraseñas hasheadas
-- Hash de "password123" con bcrypt
UPDATE usuarios 
SET password_hash = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYfQRvxJPri'
WHERE password_hash IS NULL OR password_hash = '';

-- Asegurar que tenemos usuarios de cada rol
-- Si no existe, crear un admin
INSERT INTO usuarios (nombre, correo, password_hash, rol, estado)
SELECT 'Administrador Sistema', 'admin@empresa.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYfQRvxJPri', 'admin', 'active'
WHERE NOT EXISTS (
    SELECT 1 FROM usuarios WHERE correo = 'admin@empresa.com'
);

-- Si no existe, crear un supervisor
INSERT INTO usuarios (nombre, correo, password_hash, rol, estado)
SELECT 'Carlos Supervisor', 'supervisor@empresa.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYfQRvxJPri', 'supervisor', 'active'
WHERE NOT EXISTS (
    SELECT 1 FROM usuarios WHERE correo = 'supervisor@empresa.com'
);

-- Si no existe, crear un inspector
INSERT INTO usuarios (nombre, correo, password_hash, rol, estado)
SELECT 'Juan Inspector', 'inspector@empresa.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYfQRvxJPri', 'inspector', 'active'
WHERE NOT EXISTS (
    SELECT 1 FROM usuarios WHERE correo = 'inspector@empresa.com'
);

-- Verificar usuarios creados
SELECT id_usuario, nombre, correo, rol, estado 
FROM usuarios 
WHERE correo IN ('admin@empresa.com', 'supervisor@empresa.com', 'inspector@empresa.com');
