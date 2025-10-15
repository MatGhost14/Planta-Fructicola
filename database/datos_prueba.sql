-- Script para agregar datos de prueba al sistema
-- Fecha: 15 de octubre de 2025

USE impeccioncontenedor;

-- 1. Actualizar usuarios con contraseñas (bcrypt hash de "password123")
UPDATE usuarios 
SET password_hash = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5QK7TBR3vXjpe'
WHERE password_hash IS NULL;

-- 2. Insertar inspecciones de prueba
INSERT INTO inspecciones (
    codigo,
    numero_contenedor,
    id_planta,
    id_navieras,
    temperatura_c,
    observaciones,
    id_inspector,
    estado,
    inspeccionado_en,
    creado_en
) VALUES
-- Inspecciones del último mes (octubre 2025)
('INS-2025-001', 'MAEU1234567', 1, 1, -18.5, 'Contenedor en óptimas condiciones. Sin daños visibles.', 1, 'approved', '2025-10-01 08:30:00', NOW()),
('INS-2025-002', 'MSCU2345678', 2, 2, -19.0, 'Pequeño golpe en esquina inferior derecha. Funcional.', 1, 'approved', '2025-10-02 09:15:00', NOW()),
('INS-2025-003', 'CSQU3456789', 3, 3, -17.8, 'Contenedor limpio y en buen estado.', 1, 'approved', '2025-10-03 10:00:00', NOW()),
('INS-2025-004', 'HLCU4567890', 4, 4, -20.0, 'Sistema de refrigeración trabajando perfectamente.', 1, 'approved', '2025-10-04 11:20:00', NOW()),
('INS-2025-005', 'MAEU5678901', 1, 1, -15.5, 'Temperatura ligeramente alta. Requiere ajuste.', 1, 'pending', '2025-10-05 14:30:00', NOW()),

('INS-2025-006', 'MSCU6789012', 2, 2, -18.0, 'Contenedor en buenas condiciones generales.', 1, 'approved', '2025-10-06 08:45:00', NOW()),
('INS-2025-007', 'CSQU7890123', 3, 3, -21.0, 'RECHAZADO: Falla en sistema de refrigeración.', 1, 'rejected', '2025-10-07 09:00:00', NOW()),
('INS-2025-008', 'HLCU8901234', 4, 4, -19.5, 'Excelente estado. Aprobado sin observaciones.', 1, 'approved', '2025-10-08 10:30:00', NOW()),
('INS-2025-009', 'MAEU9012345', 1, 1, -18.8, 'Documentación completa. Estado óptimo.', 1, 'approved', '2025-10-09 11:00:00', NOW()),
('INS-2025-010', 'MSCU0123456', 2, 2, -17.5, 'Pendiente de revisión de documentos.', 1, 'pending', '2025-10-10 13:15:00', NOW()),

('INS-2025-011', 'CSQU1234560', 3, 3, -19.2, 'Contenedor limpio, sin daños estructurales.', 1, 'approved', '2025-10-11 08:00:00', NOW()),
('INS-2025-012', 'HLCU2345671', 4, 4, -18.5, 'Sellos de seguridad en orden.', 1, 'approved', '2025-10-12 09:30:00', NOW()),
('INS-2025-013', 'MAEU3456782', 1, 1, -10.0, 'RECHAZADO: Temperatura fuera de rango permitido.', 1, 'rejected', '2025-10-13 10:00:00', NOW()),
('INS-2025-014', 'MSCU4567893', 2, 2, -19.8, 'Aprobado. Listo para embarque.', 1, 'approved', '2025-10-14 11:30:00', NOW()),
('INS-2025-015', 'CSQU5678904', 3, 3, -18.0, 'En proceso de inspección final.', 1, 'pending', '2025-10-15 08:00:00', NOW()),

-- Inspecciones del mes anterior (septiembre 2025)
('INS-2025-016', 'HLCU6789015', 4, 4, -19.0, 'Contenedor septiembre - estado bueno.', 1, 'approved', '2025-09-25 09:00:00', NOW()),
('INS-2025-017', 'MAEU7890126', 1, 1, -18.5, 'Inspección septiembre - aprobado.', 1, 'approved', '2025-09-26 10:30:00', NOW()),
('INS-2025-018', 'MSCU8901237', 2, 2, -20.0, 'Contenedor septiembre - rechazado por óxido.', 1, 'rejected', '2025-09-27 11:00:00', NOW()),
('INS-2025-019', 'CSQU9012348', 3, 3, -17.8, 'Inspección septiembre - pendiente.', 1, 'pending', '2025-09-28 13:30:00', NOW()),
('INS-2025-020', 'HLCU0123459', 4, 4, -19.5, 'Contenedor septiembre - excelente.', 1, 'approved', '2025-09-29 14:00:00', NOW()),

-- Más inspecciones recientes para dashboard
('INS-2025-021', 'MAEU1234561', 1, 1, -18.7, 'Inspección reciente - aprobado.', 1, 'approved', NOW(), NOW()),
('INS-2025-022', 'MSCU2345672', 2, 2, -19.1, 'Inspección reciente - pendiente.', 1, 'pending', NOW(), NOW()),
('INS-2025-023', 'CSQU3456783', 3, 3, -18.3, 'Inspección reciente - aprobado.', 1, 'approved', NOW(), NOW()),
('INS-2025-024', 'HLCU4567894', 4, 4, -19.8, 'Inspección reciente - aprobado.', 1, 'approved', NOW(), NOW()),
('INS-2025-025', 'MAEU5678905', 1, 1, -16.0, 'Inspección reciente - requiere seguimiento.', 1, 'pending', NOW(), NOW());

-- 3. Verificar datos insertados
SELECT 
    'Usuarios actualizados' as item,
    COUNT(*) as cantidad
FROM usuarios
WHERE password_hash IS NOT NULL

UNION ALL

SELECT 
    'Inspecciones totales' as item,
    COUNT(*) as cantidad
FROM inspecciones

UNION ALL

SELECT 
    'Inspecciones Aprobadas' as item,
    COUNT(*) as cantidad
FROM inspecciones
WHERE estado = 'approved'

UNION ALL

SELECT 
    'Inspecciones Pendientes' as item,
    COUNT(*) as cantidad
FROM inspecciones
WHERE estado = 'pending'

UNION ALL

SELECT 
    'Inspecciones Rechazadas' as item,
    COUNT(*) as cantidad
FROM inspecciones
WHERE estado = 'rejected';

-- 4. Verificar distribución por planta
SELECT 
    p.nombre as planta,
    COUNT(i.id_inspeccion) as total_inspecciones,
    SUM(CASE WHEN i.estado = 'approved' THEN 1 ELSE 0 END) as aprobadas,
    SUM(CASE WHEN i.estado = 'pending' THEN 1 ELSE 0 END) as pendientes,
    SUM(CASE WHEN i.estado = 'rejected' THEN 1 ELSE 0 END) as rechazadas
FROM plantas p
LEFT JOIN inspecciones i ON p.id_planta = i.id_planta
GROUP BY p.id_planta, p.nombre
ORDER BY total_inspecciones DESC;

-- 5. Verificar distribución por naviera
SELECT 
    n.nombre as naviera,
    COUNT(i.id_inspeccion) as total_inspecciones
FROM navieras n
LEFT JOIN inspecciones i ON n.id_navieras = i.id_navieras
GROUP BY n.id_navieras, n.nombre
ORDER BY total_inspecciones DESC;
