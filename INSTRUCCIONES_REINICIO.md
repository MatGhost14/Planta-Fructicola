# 🚀 INSTRUCCIONES DE REINICIO - Sistema de Inspección

## ⚠️ IMPORTANTE: Debes reiniciar ambos servidores para aplicar los cambios

---

## 📋 Cambios Aplicados

### ✅ Backend (Python/FastAPI)
1. **estadisticas.py** - Corregida lógica de fechas y queries SQL
2. **reportes_export.py** - Eliminados JOINs problemáticos (cambio anterior)

### ✅ Frontend (React/TypeScript)
1. **estadisticas.ts** - Interfaces actualizadas para coincidir con backend
2. **Dashboard.tsx** - Campos corregidos para mostrar datos correctamente
3. **index.css** - Orden de @import corregido (cambio anterior)

---

## 🔄 PASO 1: REINICIAR BACKEND

### Opción A: Si está en la terminal "python"

1. **Presiona `Ctrl + C`** en la terminal del backend para detenerlo
2. **Espera** hasta ver el mensaje "Shutdown complete"
3. **Ejecuta de nuevo:**

```powershell
cd "C:\Users\Jesus R\Desktop\Planta-\backend"
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Opción B: Si no encuentras la terminal

**Abre nueva terminal PowerShell y ejecuta:**

```powershell
# Ir al directorio del backend
cd "C:\Users\Jesus R\Desktop\Planta-\backend"

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Iniciar servidor
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**✅ Backend listo cuando veas:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process...
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## 🔄 PASO 2: VERIFICAR FRONTEND

El frontend con Vite debería recargar automáticamente los cambios. **Refresca el navegador** (F5 o Ctrl+R).

### Si necesitas reiniciar el frontend:

```powershell
# En otra terminal
cd "C:\Users\Jesus R\Desktop\Planta-\frontend"
npm run dev
```

**✅ Frontend listo cuando veas:**
```
  VITE v5.4.20  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

---

## ✅ PASO 3: VERIFICAR QUE FUNCIONA

### 1. Abrir la aplicación
🌐 **URL:** http://localhost:5173

### 2. Iniciar sesión
- **Usuario:** `admin@sistema.com` o `carlos.ruiz@example.com`
- **Contraseña:** `password123`

### 3. Ir al Dashboard
Deberías ver:
- ✅ **Total Inspecciones: 7**
- ✅ **Pendientes:** (número > 0)
- ✅ **Aprobadas:** (número > 0)
- ✅ **Rechazadas:** (número > 0)
- ✅ **Gráfico de pastel** con colores
- ✅ **Gráfico de línea** con tendencia
- ✅ **Gráfico de barras** por planta
- ✅ **Tabla de inspectores** con datos

### 4. Probar Exportación
Ve a **Reportes** → Haz clic en:
- ✅ **Exportar PDF** → Descarga `reporte_inspecciones_[timestamp].pdf` en **Descargas**
- ✅ **Exportar Excel** → Descarga `reporte_inspecciones_[timestamp].xlsx` en **Descargas**

---

## 🐛 Si algo no funciona

### Dashboard sigue vacío

**Abrir DevTools del navegador (F12):**
1. Ve a la pestaña **Console**
2. Busca errores en rojo
3. Ve a la pestaña **Network**
4. Busca la petición `/estadisticas/dashboard`
5. Haz clic en ella y ve a **Response**

**Envíame el contenido de Response para ayudarte**

### Error 500 en exportación

**Revisar terminal del backend:**
- Busca mensajes de error en rojo
- Debería mostrar el stack trace completo del error
- **Envíame el error completo**

### Gráficos no aparecen

1. **Verifica que recharts esté instalado:**
```powershell
cd "C:\Users\Jesus R\Desktop\Planta-\frontend"
npm list recharts
```

2. Si no está instalado:
```powershell
npm install recharts
```

---

## 📊 Verificar Datos en Base de Datos

Si después del reinicio el dashboard sigue vacío, verifica las fechas:

```sql
-- Ver inspecciones recientes
SELECT 
    id_inspeccion, 
    codigo, 
    estado, 
    DATE(inspeccionado_en) as fecha
FROM inspecciones
ORDER BY inspeccionado_en DESC
LIMIT 10;

-- Ver conteo por estado
SELECT 
    estado, 
    COUNT(*) as cantidad
FROM inspecciones
WHERE inspeccionado_en >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY estado;
```

**Si no hay inspecciones en los últimos 30 días:**
- Usa los filtros de fecha en el dashboard para ampliar el rango
- O ejecuta el script: `datos_prueba.sql` que crea 25 inspecciones de prueba

---

## 📁 Archivos Descargables

La exportación descarga automáticamente en tu carpeta **Descargas** con este formato:

```
📁 Descargas/
  ├── reporte_inspecciones_1729035600000.pdf
  ├── reporte_inspecciones_1729035601000.xlsx
  └── ...
```

**Nombre del archivo:** `reporte_inspecciones_[timestamp].[pdf|xlsx]`
- El timestamp asegura que cada descarga tenga un nombre único
- No se sobrescriben archivos anteriores

---

## 🎯 Checklist Final

Marca cuando completes cada paso:

- [ ] Backend reiniciado (puerto 8000)
- [ ] Frontend corriendo (puerto 5173)
- [ ] Página abierta en http://localhost:5173
- [ ] Sesión iniciada correctamente
- [ ] Dashboard muestra Total Inspecciones: 7
- [ ] Dashboard muestra números en tarjetas (no vacías)
- [ ] Gráfico de pastel visible
- [ ] Gráfico de línea visible
- [ ] Gráfico de barras visible
- [ ] Tabla de inspectores con datos
- [ ] Exportar PDF funciona
- [ ] Exportar Excel funciona

---

## 💡 Comandos Rápidos

### Ver estado de puertos
```powershell
netstat -ano | Select-String "8000|5173"
```

### Matar proceso en puerto (si está ocupado)
```powershell
# Para puerto 8000
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force

# Para puerto 5173
Get-Process -Id (Get-NetTCPConnection -LocalPort 5173).OwningProcess | Stop-Process -Force
```

### Ver logs del backend en tiempo real
Los logs aparecen automáticamente en la terminal donde corre uvicorn.
Busca líneas como:
```
INFO:     127.0.0.1:XXXXX - "GET /api/estadisticas/dashboard HTTP/1.1" 200 OK
```

---

**¿Todo listo?** Si el dashboard y la exportación funcionan correctamente, ¡el problema está resuelto! 🎉

**¿Algún error?** Envíame:
1. Capturas de pantalla de la consola del navegador (F12)
2. Mensajes de error de la terminal del backend
3. Descripción de qué no está funcionando
