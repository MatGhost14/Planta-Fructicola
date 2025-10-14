# 📚 Tutorial Completo - Sistema de Inspección de Contenedores

Guía paso a paso para usar el sistema desde la instalación hasta la creación de inspecciones.

---

## 📋 Tabla de Contenidos

1. [Instalación Inicial](#1-instalación-inicial)
2. [Primer Login](#2-primer-login)
3. [Navegación por Roles](#3-navegación-por-roles)
4. [Crear una Inspección](#4-crear-una-inspección)
5. [Ver Detalles de Inspección](#5-ver-detalles-de-inspección)
6. [Aprobar/Rechazar (Supervisor)](#6-aprobarrechazar-supervisor)
7. [Gestión de Usuarios (Admin)](#7-gestión-de-usuarios-admin)
8. [Tips y Trucos](#8-tips-y-trucos)

---

## 1. Instalación Inicial

### Paso 1.1: Verificar Requisitos

```powershell
# Verificar Python
python --version
# Debe mostrar: Python 3.10 o superior

# Verificar Node.js
node --version
# Debe mostrar: v18.0 o superior

# Verificar MySQL (XAMPP)
# Abrir XAMPP Control Panel y verificar que MySQL esté corriendo
```

### Paso 1.2: Instalar el Sistema

```powershell
# Navegar a la carpeta del proyecto
cd "C:\Users\TuUsuario\Desktop\Planta-"

# Ejecutar script de instalación
.\install.ps1

# Configurar base de datos
.\setup-database.ps1
```

### Paso 1.3: Iniciar Servicios

```powershell
# Iniciar backend y frontend automáticamente
.\start-dev.ps1
```

Verás dos terminales:
- **Terminal 1**: Backend FastAPI (puerto 8000)
- **Terminal 2**: Frontend React (puerto 5173)

---

## 2. Primer Login

### Paso 2.1: Acceder al Sistema

1. Abre tu navegador
2. Ve a: **http://localhost:5173**
3. Serás redirigido automáticamente a `/login`

### Paso 2.2: Credenciales de Prueba

El sistema viene con 3 usuarios pre-configurados:

**Inspector:**
```
Email: inspector@empresa.com
Password: password123
```

**Supervisor:**
```
Email: supervisor@empresa.com
Password: password123
```

**Admin:**
```
Email: admin@empresa.com
Password: password123
```

### Paso 2.3: Iniciar Sesión

1. Ingresa el email
2. Ingresa la contraseña
3. Click en "Iniciar Sesión"
4. Serás redirigido al Dashboard

### Paso 2.4: Cerrar Sesión

1. Click en tu nombre en la barra superior
2. Selecciona "Cerrar Sesión"
3. O presiona F12 → Console → `localStorage.clear()` → Reload

---

## 3. Navegación por Roles

### 3.1 Vista de Inspector

Cuando inicias sesión como **Inspector**, verás:

#### Dashboard
- ✅ KPIs de **tus inspecciones** solamente
- ✅ Lista de tus últimas inspecciones
- ❌ No ves inspecciones de otros

#### Módulo Inspecciones
- ✅ Ver lista de tus inspecciones
- ✅ Crear nueva inspección
- ✅ Ver detalle de tus inspecciones
- ✅ Editar tus inspecciones (sin cambiar estado)
- ❌ No puedes eliminar
- ❌ No puedes aprobar/rechazar

#### Botones Visibles
```
✅ Nueva Inspección
✅ Ver Detalles
✅ Editar (solo propias)
❌ Eliminar
❌ Aprobar/Rechazar
```

### 3.2 Vista de Supervisor

Cuando inicias sesión como **Supervisor**, verás:

#### Dashboard
- ✅ KPIs de **todas las inspecciones**
- ✅ Gráficos y estadísticas completas
- ✅ Filtros avanzados

#### Módulo Inspecciones
- ✅ Ver **todas** las inspecciones
- ✅ Crear inspecciones para cualquier inspector
- ✅ Editar cualquier inspección
- ✅ Cambiar estados (aprobar/rechazar)
- ✅ Eliminar inspecciones
- ✅ Gestionar plantas y navieras

#### Botones Visibles
```
✅ Nueva Inspección
✅ Ver Detalles
✅ Editar
✅ Eliminar
✅ Aprobar
✅ Rechazar
```

### 3.3 Vista de Admin

El **Admin** tiene acceso completo:

- ✅ Todo lo del Supervisor
- ✅ Gestión de usuarios
- ✅ Auditoría del sistema
- ✅ Configuración global
- ✅ Reportes avanzados

---

## 4. Crear una Inspección

### Paso 4.1: Ir al Módulo Inspecciones

1. Click en "Inspecciones" en el menú lateral
2. Click en el botón "Nueva Inspección" (azul, esquina superior derecha)

### Paso 4.2: Completar el Formulario

```
📦 Número de Contenedor: TCLU1234567
🏭 Planta: Selecciona de la lista
🚢 Naviera: Selecciona de la lista
🌡️ Temperatura: -18.5 (opcional)
📝 Observaciones: "Contenedor en perfecto estado"
👤 Inspector: (Auto-asignado si eres inspector)
📅 Fecha de Inspección: (Automática o selecciona)
```

### Paso 4.3: Guardar

1. Click en "Guardar" o "Crear Inspección"
2. El sistema creará la inspección con estado "Pending"
3. Recibirás un código único (ej: INS-2024-001)
4. Serás redirigido a la página de subir fotos

### Paso 4.4: Subir Fotos

1. Click en "Subir Fotos" o arrastra archivos
2. Selecciona múltiples fotos desde tu dispositivo
3. Formatos permitidos: JPG, PNG
4. Tamaño máximo: 5MB por foto
5. Click en "Subir Todas"

### Paso 4.5: Agregar Firma Digital

1. Dibuja tu firma con el mouse o dedo (touch)
2. Click en "Limpiar" si quieres rehacer
3. Click en "Guardar Firma"
4. La firma se almacena automáticamente

---

## 5. Ver Detalles de Inspección

### Paso 5.1: Acceder al Detalle

**Opción 1: Desde la lista**
1. Ve a "Inspecciones"
2. Click en "Ver Detalles" en cualquier fila

**Opción 2: Desde el Dashboard**
1. Click en el código de inspección (ej: INS-2024-001)

### Paso 5.2: Modal de Detalle

El modal muestra:

```
┌────────────────────────────────────────┐
│ Inspección INS-2024-001                │
│ Contenedor: TCLU1234567                │
│ ┌────────────┐                         │
│ │  📍 Planta │ Planta Central          │
│ └────────────┘                         │
│ ┌────────────┐                         │
│ │  🚢 Naviera│ Maersk Line             │
│ └────────────┘                         │
│ ┌────────────┐                         │
│ │  👤 Inspector │ Juan Pérez          │
│ └────────────┘                         │
│ ┌────────────┐                         │
│ │  🌡️ Temp   │ -18.5°C                │
│ └────────────┘                         │
│                                        │
│ 📸 Fotografías (4)                     │
│ [🖼️] [🖼️] [🖼️] [🖼️]                │
│                                        │
│ ✍️ Firma Digital                       │
│ [Imagen de firma]                      │
│                                        │
│ 📝 Observaciones                       │
│ Contenedor en perfecto estado         │
└────────────────────────────────────────┘
```

### Paso 5.3: Ver Foto Ampliada

1. Click en cualquier foto
2. Se abre en modo lightbox (pantalla completa)
3. Click en "X" o fuera de la imagen para cerrar

---

## 6. Aprobar/Rechazar (Supervisor)

### Paso 6.1: Revisar Inspección

1. Login como **Supervisor**
2. Ve a "Inspecciones"
3. Filtra por estado "Pendiente"
4. Click en "Ver Detalles"

### Paso 6.2: Aprobar

```
✅ Si todo está correcto:
1. Click en "Aprobar"
2. (Opcional) Agrega comentario
3. Confirma la acción
4. Estado cambia a "Aprobada" (verde)
```

### Paso 6.3: Rechazar

```
❌ Si hay problemas:
1. Click en "Rechazar"
2. OBLIGATORIO: Agrega razón del rechazo
3. Ejemplo: "Fotos borrosas, repetir inspección"
4. Confirma la acción
5. Estado cambia a "Rechazada" (rojo)
```

### Paso 6.4: Notificación al Inspector

El inspector recibirá:
- ✉️ Notificación en el sistema
- 📧 Email (si configurado)
- 📱 Push notification (si configurado)

---

## 7. Gestión de Usuarios (Admin)

### Paso 7.1: Acceder a Usuarios

1. Login como **Admin**
2. Click en "Administración"
3. Click en "Usuarios"

### Paso 7.2: Crear Nuevo Usuario

```
1. Click en "Nuevo Usuario"
2. Completa el formulario:
   - Nombre: Juan Pérez
   - Email: juan.perez@empresa.com
   - Rol: Inspector / Supervisor / Admin
   - Estado: Activo
   - Password: (Temporal, usuario debe cambiar)
3. Click en "Crear"
```

### Paso 7.3: Editar Usuario

1. Click en el ícono de editar (lápiz)
2. Modifica los campos necesarios
3. Click en "Guardar Cambios"

### Paso 7.4: Desactivar Usuario

1. Click en el ícono de estado
2. Selecciona "Inactivo"
3. El usuario no podrá iniciar sesión

### Paso 7.5: Cambiar Rol

```
⚠️ CUIDADO al cambiar roles:
- Inspector → Supervisor: Obtiene más permisos
- Supervisor → Inspector: Pierde permisos
- Cualquiera → Admin: Acceso total
```

---

## 8. Tips y Trucos

### 8.1 Atajos de Teclado

```
Ctrl + K         → Abrir búsqueda rápida
Ctrl + N         → Nueva inspección
Ctrl + S         → Guardar cambios
Esc              → Cerrar modales
```

### 8.2 Filtros Rápidos

**En Inspecciones:**
```
Estado:
- Click en badge "Pendiente" → Filtra pendientes
- Click en badge "Aprobada" → Filtra aprobadas
- Click en badge "Rechazada" → Filtra rechazadas
```

**Búsqueda:**
```
Busca por:
- Número de contenedor: TCLU1234567
- Código: INS-2024-001
- Planta: Central
- Inspector: Juan Pérez
```

### 8.3 Exportar Datos

1. Ve a "Reportes"
2. Selecciona filtros (fechas, estado, planta)
3. Click en "Exportar CSV"
4. Descarga automática

### 8.4 Modo Offline

```
⚠️ Funcionalidad limitada sin conexión:
✅ Ver inspecciones cacheadas
❌ Crear nuevas inspecciones
❌ Subir fotos
❌ Cambiar estados
```

### 8.5 Cambiar Contraseña

1. Click en tu nombre (esquina superior derecha)
2. "Mi Perfil"
3. "Cambiar Contraseña"
4. Ingresa:
   - Contraseña actual
   - Nueva contraseña
   - Confirmar nueva contraseña
5. Mínimo 8 caracteres

### 8.6 Solución de Problemas Comunes

**"Se queda cargando"**
```
1. Verifica que backend esté corriendo (puerto 8000)
2. Abre F12 → Console → Busca errores
3. Recarga la página (Ctrl + R)
```

**"No puedo subir fotos"**
```
1. Verifica formato: Solo JPG, PNG
2. Verifica tamaño: Máximo 5MB
3. Verifica permisos: Solo dueño de inspección
```

**"No veo mis inspecciones"**
```
1. Verifica tu rol (Inspector solo ve propias)
2. Verifica filtros activos
3. Limpia filtros con "Limpiar Filtros"
```

**"Token expirado"**
```
1. Cierra sesión
2. Vuelve a ingresar
3. Token dura 8 horas
```

### 8.7 Mejores Prácticas

**Para Inspectores:**
- ✅ Toma fotos claras y bien iluminadas
- ✅ Incluye fotos de todos los ángulos
- ✅ Completa observaciones detalladas
- ✅ Firma antes de enviar

**Para Supervisores:**
- ✅ Revisa todas las fotos antes de aprobar
- ✅ Da feedback específico al rechazar
- ✅ Revisa inspecciones pendientes diariamente
- ✅ Usa reportes para identificar tendencias

**Para Admins:**
- ✅ Revisa auditoría semanalmente
- ✅ Cambia contraseñas periódicamente
- ✅ Mantén usuarios actualizados
- ✅ Haz respaldos de BD regularmente

---

## 9. Preguntas Frecuentes

**¿Puedo usar el sistema desde mi celular?**
Sí, es completamente responsive. Funciona en cualquier dispositivo con navegador moderno.

**¿Las fotos se guardan en la base de datos?**
No, se guardan en el filesystem (carpeta `capturas/`) por eficiencia.

**¿Cuántas fotos puedo subir por inspección?**
No hay límite, pero se recomienda entre 4-8 fotos relevantes.

**¿Puedo editar una inspección aprobada?**
Solo Admin puede editar inspecciones aprobadas.

**¿Cómo recupero mi contraseña?**
Contacta al administrador del sistema.

**¿El sistema guarda historial de cambios?**
Sí, en la tabla `bitacora_auditoria`. Visible para Admin.

---

## 📞 Soporte

Si tienes problemas o dudas:

1. **Revisa este tutorial**
2. **Consulta el README.md**
3. **Revisa IMPLEMENTACION-COMPLETADA.md**
4. **Contacta al equipo de desarrollo**

---

**¡Disfruta usando el sistema! 🚀**

**Última actualización:** 14 de octubre de 2025
