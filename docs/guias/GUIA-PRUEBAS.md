# 🧪 Guía de Pruebas - Sistema de Inspección de Contenedores

## 📋 Checklist de Pruebas

---

## 🔐 Fase 1: Pruebas de Autenticación

### ✅ Test 1.1: Login Inspector
- [ ] Ir a http://localhost:5173/login
- [ ] Email: `inspector@empresa.com`
- [ ] Contraseña: `password123`
- [ ] Click "Iniciar Sesión"
- [ ] **Esperado**: Redirige a /dashboard
- [ ] **Verificar**: Menú lateral muestra solo: Dashboard, Nueva Inspección, Inspecciones, Reportes

### ✅ Test 1.2: Login Supervisor
- [ ] Logout (botón en sidebar)
- [ ] Email: `supervisor@empresa.com`
- [ ] Contraseña: `password123`
- [ ] Click "Iniciar Sesión"
- [ ] **Esperado**: Redirige a /dashboard
- [ ] **Verificar**: Menú lateral muestra: Dashboard, Nueva Inspección, Inspecciones, Reportes, **Plantas**, **Navieras**

### ✅ Test 1.3: Login Admin
- [ ] Logout
- [ ] Email: `admin@empresa.com`
- [ ] Contraseña: `password123`
- [ ] Click "Iniciar Sesión"
- [ ] **Esperado**: Redirige a /dashboard
- [ ] **Verificar**: Menú lateral muestra TODO: Dashboard, Nueva Inspección, Inspecciones, Reportes, Plantas, Navieras, **Usuarios**, **Configuración**

### ✅ Test 1.4: Sesión Activa
- [ ] Con sesión iniciada, ir a http://localhost:5173/login
- [ ] **Esperado**: Pantalla "Sesión Activa" con nombre de usuario
- [ ] **Opciones**: "Ir al Dashboard" o "Iniciar sesión con otra cuenta"
- [ ] Click "Ir al Dashboard" → Va a /dashboard
- [ ] Volver a /login, click "Iniciar sesión con otra cuenta" → Limpia sesión

---

## 👥 Fase 2: Gestión de Usuarios (Solo Admin)

### ✅ Test 2.1: Ver Lista de Usuarios
- [ ] Login como admin
- [ ] Click en "Usuarios" en menú lateral
- [ ] **Esperado**: Tabla con usuarios existentes
- [ ] **Verificar columnas**: Avatar, Nombre, Email, Rol (con badge de color), Estado, Último Acceso, Acciones

### ✅ Test 2.2: Crear Usuario Inspector
- [ ] Click botón "Nuevo Usuario"
- [ ] Modal se abre
- [ ] Llenar formulario:
  - Nombre: `Test Inspector`
  - Email: `test.inspector@test.com`
  - Rol: `Inspector`
  - Contraseña: `test123456`
- [ ] Click "Crear Usuario"
- [ ] **Esperado**: Alert "Usuario creado exitosamente"
- [ ] **Verificar**: Usuario aparece en tabla con badge verde

### ✅ Test 2.3: Editar Usuario
- [ ] Click botón "Editar" (ícono lápiz) del usuario recién creado
- [ ] Modal se abre con datos precargados
- [ ] Cambiar nombre a: `Test Inspector Editado`
- [ ] Cambiar rol a: `Supervisor`
- [ ] Dejar contraseña vacía
- [ ] Click "Actualizar"
- [ ] **Esperado**: Alert "Usuario actualizado exitosamente"
- [ ] **Verificar**: Nombre y rol (badge azul) actualizados

### ✅ Test 2.4: Toggle Estado
- [ ] Click en badge de estado "Activo" del usuario
- [ ] **Esperado**: Cambia a "Inactivo" (rojo)
- [ ] Click nuevamente
- [ ] **Esperado**: Vuelve a "Activo" (verde)

### ✅ Test 2.5: Validación - Email Duplicado
- [ ] Click "Nuevo Usuario"
- [ ] Email: `admin@empresa.com` (ya existe)
- [ ] Llenar otros campos
- [ ] Click "Crear Usuario"
- [ ] **Esperado**: Error "Ya existe un usuario con correo 'admin@empresa.com'"

### ✅ Test 2.6: Eliminar Usuario
- [ ] Click botón "Eliminar" (ícono basura) del usuario test
- [ ] **Esperado**: Confirmación "¿Está seguro que desea eliminar al usuario...?"
- [ ] Click "Aceptar"
- [ ] **Esperado**: Alert "Usuario eliminado exitosamente"
- [ ] **Verificar**: Usuario desaparece de la tabla

### ✅ Test 2.7: Restricción de Acceso
- [ ] Logout
- [ ] Login como inspector
- [ ] Intentar ir a http://localhost:5173/usuarios
- [ ] **Esperado**: Pantalla "Acceso Denegado" con mensaje de permisos

---

## 🏭 Fase 3: Gestión de Plantas (Supervisor/Admin)

### ✅ Test 3.1: Ver Lista de Plantas
- [ ] Login como supervisor
- [ ] Click en "Plantas" en menú lateral
- [ ] **Esperado**: Tabla con plantas existentes

### ✅ Test 3.2: Crear Planta
- [ ] Click botón "Nueva Planta"
- [ ] Llenar formulario:
  - Código: `PLT-TEST-01`
  - Nombre: `Planta de Prueba`
  - Ubicación: `Santiago, Chile`
- [ ] Click "Crear Planta"
- [ ] **Esperado**: Alert "Planta creada exitosamente"
- [ ] **Verificar**: Planta aparece en tabla

### ✅ Test 3.3: Editar Planta
- [ ] Click botón "Editar" de la planta test
- [ ] Cambiar nombre a: `Planta de Prueba Editada`
- [ ] Click "Actualizar"
- [ ] **Esperado**: Alert "Planta actualizada exitosamente"
- [ ] **Verificar**: Nombre actualizado en tabla

### ✅ Test 3.4: Validación - Código Duplicado
- [ ] Click "Nueva Planta"
- [ ] Código: `PLT-TEST-01` (ya existe)
- [ ] Click "Crear Planta"
- [ ] **Esperado**: Error "Ya existe una planta con código..."

### ✅ Test 3.5: Eliminar Planta
- [ ] Click botón "Eliminar" de la planta test
- [ ] Confirmar
- [ ] **Esperado**: Alert "Planta eliminada exitosamente"

### ✅ Test 3.6: Restricción de Acceso
- [ ] Logout, login como inspector
- [ ] Intentar ir a http://localhost:5173/plantas
- [ ] **Esperado**: Pantalla "Acceso Denegado"

---

## 🚢 Fase 4: Gestión de Navieras (Supervisor/Admin)

### ✅ Test 4.1: Ver Lista de Navieras
- [ ] Login como supervisor
- [ ] Click en "Navieras"
- [ ] **Esperado**: Grid de tarjetas con navieras

### ✅ Test 4.2: Crear Naviera
- [ ] Click botón "Nueva Naviera"
- [ ] Llenar formulario:
  - Código: `TEST-NAV`
  - Nombre: `Naviera de Prueba`
- [ ] Click "Crear Naviera"
- [ ] **Esperado**: Alert "Naviera creada exitosamente"
- [ ] **Verificar**: Tarjeta aparece en grid

### ✅ Test 4.3: Editar Naviera
- [ ] En tarjeta de la naviera test, click "Editar"
- [ ] Cambiar nombre a: `Naviera Test Editada`
- [ ] Click "Actualizar"
- [ ] **Esperado**: Alert "Naviera actualizada exitosamente"

### ✅ Test 4.4: Eliminar Naviera
- [ ] En tarjeta, click "Eliminar"
- [ ] Confirmar
- [ ] **Esperado**: Alert "Naviera eliminada exitosamente"

### ✅ Test 4.5: Restricción de Acceso
- [ ] Logout, login como inspector
- [ ] Intentar ir a http://localhost:5173/navieras
- [ ] **Esperado**: Pantalla "Acceso Denegado"

---

## 📋 Fase 5: Flujo de Aprobación de Inspecciones

### ✅ Test 5.1: Crear Inspección como Inspector
- [ ] Login como inspector
- [ ] Click "Nueva Inspección"
- [ ] Llenar formulario completo
- [ ] Subir 2-3 fotos
- [ ] Agregar firma
- [ ] Guardar inspección
- [ ] **Esperado**: Inspección creada con estado "Pendiente"

### ✅ Test 5.2: Ver Inspección como Inspector
- [ ] Ir a "Inspecciones"
- [ ] Click en la inspección recién creada
- [ ] **Esperado**: Modal con todos los detalles
- [ ] **Verificar**: NO aparecen botones "Aprobar" / "Rechazar"

### ✅ Test 5.3: Aprobar Inspección como Supervisor
- [ ] Logout, login como supervisor
- [ ] Ir a "Inspecciones"
- [ ] Click en la inspección pendiente
- [ ] **Esperado**: Modal con botones "Aprobar" y "Rechazar" visibles
- [ ] Click botón "Aprobar"
- [ ] **Esperado**: Modal de confirmación se abre
- [ ] Agregar comentario: `Inspección aprobada, todo en orden`
- [ ] Click "Confirmar Aprobación"
- [ ] **Esperado**: Modal se cierra, lista se refresca
- [ ] **Verificar**: Estado cambió a "Aprobada" (verde)

### ✅ Test 5.4: Crear y Rechazar Inspección
- [ ] Login como inspector
- [ ] Crear nueva inspección (rápida, con lo mínimo)
- [ ] Logout, login como supervisor
- [ ] Ir a "Inspecciones"
- [ ] Click en nueva inspección pendiente
- [ ] Click botón "Rechazar"
- [ ] **Esperado**: Modal de rechazo se abre
- [ ] Intentar confirmar sin comentario
- [ ] **Esperado**: Botón deshabilitado
- [ ] Agregar comentario: `Fotos no tienen buena calidad, volver a inspeccionar`
- [ ] Click "Confirmar Rechazo"
- [ ] **Esperado**: Modal se cierra, lista se refresca
- [ ] **Verificar**: Estado cambió a "Rechazada" (rojo)

### ✅ Test 5.5: Ver Comentarios en Observaciones
- [ ] Abrir inspección rechazada
- [ ] Scroll a sección "Observaciones"
- [ ] **Verificar**: Comentario del rechazo aparece con formato:
  ```
  --- REJECTED por [Nombre Supervisor] ---
  [Comentario del rechazo]
  ```

### ✅ Test 5.6: Inspección Aprobada No Se Puede Cambiar
- [ ] Abrir inspección ya aprobada
- [ ] **Verificar**: Botones "Aprobar" / "Rechazar" NO aparecen
- [ ] **Razón**: Solo inspecciones pendientes pueden cambiar estado

---

## 🔐 Fase 6: Pruebas de Seguridad y Permisos

### ✅ Test 6.1: Inspector No Puede Aprobar
- [ ] Login como inspector
- [ ] Abrir DevTools (F12) → Consola
- [ ] Ejecutar:
  ```javascript
  fetch('http://localhost:8000/api/inspecciones/1/estado', {
    method: 'PATCH',
    headers: {
      'Authorization': 'Bearer ' + localStorage.getItem('auth_token'),
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ estado: 'approved', comentario: 'hack' })
  }).then(r => r.json()).then(console.log)
  ```
- [ ] **Esperado**: Error 403 "No tiene permisos para cambiar el estado"

### ✅ Test 6.2: Inspector No Puede Crear Usuarios
- [ ] Con sesión de inspector activa
- [ ] En DevTools, ejecutar:
  ```javascript
  fetch('http://localhost:8000/api/usuarios', {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer ' + localStorage.getItem('auth_token'),
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      nombre: 'Hack',
      correo: 'hack@test.com',
      rol: 'admin',
      password: 'hack123'
    })
  }).then(r => r.json()).then(console.log)
  ```
- [ ] **Esperado**: Error 403 "Se requiere rol: admin"

### ✅ Test 6.3: Supervisor No Puede Gestionar Usuarios
- [ ] Login como supervisor
- [ ] Intentar ir a http://localhost:5173/usuarios
- [ ] **Esperado**: Pantalla "Acceso Denegado"

---

## 🎨 Fase 7: Pruebas de UI/UX

### ✅ Test 7.1: Responsive Design
- [ ] Abrir DevTools (F12) → Toggle Device Toolbar
- [ ] Probar en diferentes tamaños:
  - [ ] Desktop (1920x1080)
  - [ ] Laptop (1366x768)
  - [ ] Tablet (768x1024)
  - [ ] Mobile (375x667)
- [ ] **Verificar**: Todas las páginas se adaptan correctamente

### ✅ Test 7.2: Estados de Loading
- [ ] Al cargar cualquier lista (usuarios, plantas, navieras)
- [ ] **Verificar**: Spinner de carga aparece mientras carga datos

### ✅ Test 7.3: Mensajes de Error
- [ ] Apagar backend (Ctrl+C en terminal backend)
- [ ] Intentar cargar cualquier página
- [ ] **Esperado**: Mensaje de error o redirect a login (si 401)
- [ ] Reiniciar backend

### ✅ Test 7.4: Navegación del Menú
- [ ] Click en cada ítem del menú
- [ ] **Verificar**: Ítem activo tiene fondo azul oscuro
- [ ] **Verificar**: URL cambia correctamente

### ✅ Test 7.5: Logout Funcional
- [ ] Click botón "Cerrar Sesión"
- [ ] **Esperado**: Confirmación "¿Está seguro que desea cerrar sesión?"
- [ ] Click "Aceptar"
- [ ] **Esperado**: Redirige a /login
- [ ] **Verificar**: localStorage.getItem('auth_token') es null

---

## 📊 Fase 8: Pruebas de Datos

### ✅ Test 8.1: Filtros de Inspecciones
- [ ] Ir a "Inspecciones"
- [ ] Usar filtro por estado (Pendiente/Aprobada/Rechazada)
- [ ] **Verificar**: Lista se filtra correctamente
- [ ] Usar búsqueda por número de contenedor
- [ ] **Verificar**: Búsqueda funciona

### ✅ Test 8.2: Paginación
- [ ] Si hay más de 20 inspecciones
- [ ] **Verificar**: Paginación aparece
- [ ] Click en página 2
- [ ] **Verificar**: Carga siguiente página

### ✅ Test 8.3: Validaciones de Formularios
- [ ] Crear inspección dejando campos vacíos
- [ ] **Esperado**: Mensajes de validación en campos requeridos
- [ ] Intentar submit
- [ ] **Esperado**: Form no se envía hasta completar campos

---

## ✅ Resumen de Pruebas

### Resultado Esperado
```
✅ Autenticación: ___ / 4 tests
✅ Gestión Usuarios: ___ / 7 tests
✅ Gestión Plantas: ___ / 6 tests
✅ Gestión Navieras: ___ / 5 tests
✅ Flujo Aprobación: ___ / 6 tests
✅ Seguridad: ___ / 3 tests
✅ UI/UX: ___ / 5 tests
✅ Datos: ___ / 3 tests

TOTAL: ___ / 39 tests pasados
```

---

## 🐛 Reporte de Bugs (si se encuentran)

| # | Descripción | Severidad | Página | Estado |
|---|-------------|-----------|--------|--------|
| 1 |             |           |        |        |
| 2 |             |           |        |        |

---

## 📝 Notas Adicionales

- **Navegadores probados**: Chrome, Firefox, Edge
- **Resoluciones probadas**: Desktop, Tablet, Mobile
- **Tiempo total de pruebas**: ~30-45 minutos

---

**Fecha de pruebas**: 14 de octubre de 2025  
**Sistema**: Inspección de Contenedores Frutícolas v2.1.0  
**Tester**: [Tu Nombre]
