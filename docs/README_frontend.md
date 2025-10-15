# 🎨 Frontend - Sistema de Inspección de Contenedores

## 📋 Índice

- [Descripción General](#descripción-general)
- [Tecnologías](#tecnologías)
- [Arquitectura](#arquitectura)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Componentes Principales](#componentes-principales)
- [Gestión de Estado](#gestión-de-estado)
- [Rutas y Navegación](#rutas-y-navegación)
- [Estilos y Diseño](#estilos-y-diseño)
- [Funcionalidades](#funcionalidades)
- [Instalación y Configuración](#instalación-y-configuración)
- [Build y Despliegue](#build-y-despliegue)

---

## 📝 Descripción General

El frontend del Sistema de Inspección de Contenedores es una **Single Page Application (SPA)** construida con **React + TypeScript** que proporciona una interfaz moderna, responsive e intuitiva para:

- ✅ Gestión completa de inspecciones de contenedores
- ✅ Captura de fotografías en tiempo real con cámara web
- ✅ Firma digital de inspectores
- ✅ Dashboard con estadísticas y gráficos en tiempo real
- ✅ Sistema de reportes con filtros avanzados
- ✅ Tema oscuro/claro personalizable
- ✅ Diseño responsive (móvil, tablet, desktop)

---

## 🚀 Tecnologías

### Core
- **React 18.3.1** - Librería de UI con hooks
- **TypeScript 5.5.3** - Tipado estático para JavaScript
- **Vite 5.4.20** - Build tool ultra-rápido

### Routing y Estado
- **React Router DOM 6.27** - Enrutamiento declarativo
- **Zustand 4.5.5** - Gestión de estado global ligera
- **zustand-persist** - Persistencia en localStorage

### UI y Estilos
- **Tailwind CSS 3.4.17** - Framework CSS utility-first
- **Lucide React** - Iconos modernos y consistentes
- **Chart.js 4.4.7** + **react-chartjs-2** - Gráficos interactivos

### Utilidades
- **Axios 1.7.9** - Cliente HTTP
- **date-fns** - Manejo de fechas
- **react-hot-toast** - Notificaciones elegantes
- **html2canvas** - Captura de screenshots
- **jspdf** - Generación de PDFs

### Desarrollo
- **ESLint** - Linter de código
- **PostCSS** - Procesamiento de CSS
- **Autoprefixer** - Prefijos CSS automáticos

---

## 🏗️ Arquitectura

El frontend sigue una arquitectura **basada en componentes** con separación clara de responsabilidades:

```
┌─────────────────────────────────────┐
│      Presentation Layer (Pages)     │ ← Páginas/Vistas
├─────────────────────────────────────┤
│    Component Layer (Components)     │ ← Componentes reutilizables
├─────────────────────────────────────┤
│      State Management (Store)       │ ← Estado global (Zustand)
├─────────────────────────────────────┤
│      Business Logic (Services)      │ ← Lógica de negocio
├─────────────────────────────────────┤
│      Data Layer (API Client)        │ ← Comunicación con backend
└─────────────────────────────────────┘
```

### Patrones de Diseño Implementados

1. **Component-Based Architecture**: Todo es un componente reutilizable
2. **Container/Presentational Pattern**: Separación entre lógica y presentación
3. **Custom Hooks Pattern**: Lógica compartida en hooks personalizados
4. **Context API**: Autenticación y temas globales
5. **Atomic Design**: Organización de componentes (átomos → moléculas → organismos)

---

## 📁 Estructura del Proyecto

```
frontend/
├── public/                    # Archivos estáticos
│   ├── vite.svg              # Favicon
│   └── assets/               # Imágenes, logos
│
├── src/                      # Código fuente
│   ├── api/                  # Cliente API y endpoints
│   │   ├── client.ts        # Axios instance configurada
│   │   ├── auth.ts          # Endpoints de autenticación
│   │   ├── inspecciones.ts  # Endpoints de inspecciones
│   │   ├── plantas.ts       # Endpoints de plantas
│   │   ├── navieras.ts      # Endpoints de navieras
│   │   ├── usuarios.ts      # Endpoints de usuarios
│   │   └── reportes.ts      # Endpoints de reportes
│   │
│   ├── components/           # Componentes reutilizables
│   │   ├── Layout.tsx       # Layout principal con sidebar
│   │   ├── ProtectedRoute.tsx # HOC para rutas protegidas
│   │   ├── CamaraPreview.tsx  # Componente de cámara web
│   │   ├── FirmaCanvas.tsx    # Canvas de firma digital
│   │   ├── InspeccionModal.tsx # Modal de detalles
│   │   ├── ToastProvider.tsx   # Provider de notificaciones
│   │   └── ToastContainer.tsx  # Contenedor de toasts
│   │
│   ├── contexts/             # Contexts de React
│   │   └── AuthContext.tsx  # Contexto de autenticación
│   │
│   ├── pages/                # Páginas/Vistas principales
│   │   ├── Login.tsx        # Página de login
│   │   ├── Dashboard.tsx    # Dashboard con estadísticas
│   │   ├── InspeccionNueva.tsx # Formulario de inspección
│   │   ├── Inspecciones.tsx    # Lista de inspecciones
│   │   ├── Reportes.tsx        # Página de reportes
│   │   ├── Usuarios.tsx        # Gestión de usuarios (admin)
│   │   ├── Plantas.tsx         # Gestión de plantas
│   │   ├── Navieras.tsx        # Gestión de navieras
│   │   ├── Configuracion.tsx   # Configuración de usuario
│   │   └── Admin.tsx           # Panel de administración
│   │
│   ├── store/                # Estado global (Zustand)
│   │   └── index.ts         # Store principal con tema y usuario
│   │
│   ├── types/                # Definiciones de TypeScript
│   │   ├── index.ts         # Tipos generales
│   │   ├── inspeccion.ts    # Tipos de inspecciones
│   │   ├── usuario.ts       # Tipos de usuarios
│   │   └── api.ts           # Tipos de respuestas API
│   │
│   ├── utils/                # Utilidades y helpers
│   │   ├── validators.ts    # Validadores de formularios
│   │   ├── formatters.ts    # Formateadores de datos
│   │   └── constants.ts     # Constantes de la app
│   │
│   ├── App.tsx               # Componente raíz
│   ├── main.tsx              # Punto de entrada
│   └── index.css             # Estilos globales
│
├── .env                      # Variables de entorno (gitignored)
├── .env.example             # Plantilla de variables
├── index.html               # HTML base
├── package.json             # Dependencias y scripts
├── tsconfig.json            # Configuración de TypeScript
├── tailwind.config.js       # Configuración de Tailwind
├── vite.config.ts           # Configuración de Vite
├── postcss.config.js        # Configuración de PostCSS
└── README.md                # Documentación del frontend
```

---

## 🧩 Componentes Principales

### 1. Layout (`components/Layout.tsx`)

Componente wrapper que proporciona la estructura base de todas las páginas:

**Características:**
- ✅ Sidebar lateral con menú de navegación
- ✅ Header responsive para móviles
- ✅ Sistema de roles (inspector, supervisor, admin)
- ✅ Botón de cerrar sesión
- ✅ Avatar de usuario
- ✅ Menú desplegable en móvil

**Props:**
```typescript
// No recibe props, usa <Outlet /> de React Router
```

**Uso:**
```tsx
<Layout>
  {/* Páginas se renderizan aquí vía React Router */}
</Layout>
```

---

### 2. CamaraPreview (`components/CamaraPreview.tsx`)

Componente para capturar fotos con la cámara web del dispositivo.

**Características:**
- ✅ Acceso a cámara web con getUserMedia API
- ✅ Vista previa en tiempo real
- ✅ Captura de foto con botón
- ✅ Flip horizontal para selfie mode
- ✅ Manejo de permisos
- ✅ Vista previa de foto capturada
- ✅ Opción de re-tomar foto

**Props:**
```typescript
interface CamaraPreviewProps {
  onCapture: (imageBlob: Blob) => void;
  onClose: () => void;
}
```

**Uso:**
```tsx
<CamaraPreview
  onCapture={(blob) => handleFotoCapturada(blob)}
  onClose={() => setCameraOpen(false)}
/>
```

**Tecnología:**
- `navigator.mediaDevices.getUserMedia()` - Acceso a cámara
- `<video>` + `<canvas>` - Captura de frames
- Blob API - Conversión de imagen

---

### 3. FirmaCanvas (`components/FirmaCanvas.tsx`)

Canvas interactivo para firma digital del inspector.

**Características:**
- ✅ Dibujo con mouse o touch
- ✅ Botón limpiar
- ✅ Botón guardar
- ✅ Responsive (se adapta al tamaño)
- ✅ Línea punteada como guía
- ✅ Export a imagen base64

**Props:**
```typescript
interface FirmaCanvasProps {
  onSave: (firmaBas64: string) => void;
  onCancel: () => void;
}
```

**Uso:**
```tsx
<FirmaCanvas
  onSave={(firma) => handleFirmaGuardada(firma)}
  onCancel={() => setShowFirmaCanvas(false)}
/>
```

**Tecnología:**
- HTML5 Canvas API
- Touch events + Mouse events
- `canvas.toDataURL()` - Export

---

### 4. InspeccionModal (`components/InspeccionModal.tsx`)

Modal para visualizar detalles completos de una inspección.

**Características:**
- ✅ Información completa de inspección
- ✅ Galería de fotos con lightbox
- ✅ Visualización de firma
- ✅ Badges de estado (pendiente/aprobada/rechazada)
- ✅ Formato de fechas legibles
- ✅ Botón de cerrar con overlay

**Props:**
```typescript
interface InspeccionModalProps {
  inspeccion: Inspeccion;
  onClose: () => void;
}
```

**Uso:**
```tsx
{selectedInspeccion && (
  <InspeccionModal
    inspeccion={selectedInspeccion}
    onClose={() => setSelectedInspeccion(null)}
  />
)}
```

---

### 5. ToastProvider (`components/ToastProvider.tsx`)

Sistema de notificaciones toast personalizado.

**Características:**
- ✅ Notificaciones success, error, info, warning
- ✅ Animaciones suaves de entrada/salida
- ✅ Auto-dismiss configurable
- ✅ Stack de múltiples toasts
- ✅ Confirmaciones con botones
- ✅ Posicionamiento fijo top-right

**API:**
```typescript
const { showSuccess, showError, showInfo, confirm } = useToast();

// Notificaciones simples
showSuccess("Inspección creada correctamente");
showError("Error al subir foto");

// Confirmaciones
const confirmed = await confirm("¿Está seguro de eliminar?");
if (confirmed) {
  // Acción de confirmación
}
```

**Uso:**
```tsx
// En App.tsx
<ToastProvider>
  <RouterProvider router={router} />
</ToastProvider>

// En cualquier componente
const { showSuccess } = useToast();
```

---

### 6. ProtectedRoute (`components/ProtectedRoute.tsx`)

Higher-Order Component para proteger rutas que requieren autenticación.

**Características:**
- ✅ Verifica si usuario está autenticado
- ✅ Redirección a /login si no autenticado
- ✅ Preserva ruta destino para redirect post-login
- ✅ Integración con AuthContext

**Uso:**
```tsx
<Route element={<ProtectedRoute />}>
  <Route path="/dashboard" element={<Dashboard />} />
  <Route path="/inspecciones" element={<Inspecciones />} />
</Route>
```

---

## 📄 Páginas Principales

### 1. Login (`pages/Login.tsx`)

Página de autenticación de usuarios.

**Características:**
- ✅ Formulario de email y contraseña
- ✅ Validación de campos
- ✅ Mensajes de error claros
- ✅ Credenciales de prueba visibles
- ✅ Diseño moderno con gradientes
- ✅ Responsive para móviles

**Estados:**
```typescript
const [correo, setCorreo] = useState("");
const [password, setPassword] = useState("");
const [error, setError] = useState("");
const [isLoading, setIsLoading] = useState(false);
```

**Flujo:**
1. Usuario ingresa credenciales
2. Click en "Iniciar Sesión"
3. POST a `/auth/login`
4. Si éxito: Guardar token + Redirect a /dashboard
5. Si error: Mostrar mensaje de error

---

### 2. Dashboard (`pages/Dashboard.tsx`)

Panel principal con estadísticas e indicadores.

**Características:**
- ✅ KPIs destacados (total, pendientes, aprobadas, rechazadas)
- ✅ Filtros de fecha (desde/hasta)
- ✅ Gráfico de distribución por estado (dona)
- ✅ Gráfico de tendencia temporal (línea)
- ✅ Tabla de últimas inspecciones
- ✅ Actualización en tiempo real
- ✅ Exportar a Excel
- ✅ Modo oscuro completo

**Gráficos:**
```typescript
import { Doughnut, Line } from 'react-chartjs-2';

// Distribución por estado
<Doughnut
  data={{
    labels: ['Aprobadas', 'Pendientes', 'Rechazadas'],
    datasets: [{
      data: [aprobadas, pendientes, rechazadas],
      backgroundColor: ['#10b981', '#f59e0b', '#ef4444']
    }]
  }}
/>

// Tendencia temporal
<Line
  data={{
    labels: fechas,
    datasets: [{
      label: 'Inspecciones',
      data: valores,
      borderColor: '#3b82f6'
    }]
  }}
/>
```

---

### 3. InspeccionNueva (`pages/InspeccionNueva.tsx`)

Formulario para crear nueva inspección.

**Características:**
- ✅ Formulario multi-sección
- ✅ Selección de planta y naviera
- ✅ Campo de temperatura
- ✅ Área de observaciones
- ✅ Captura de múltiples fotos con cámara
- ✅ Preview de fotos antes de enviar
- ✅ Firma digital del inspector
- ✅ Validación de campos requeridos
- ✅ Guardar borrador
- ✅ Botón cancelar

**Flujo:**
1. Inspector llena datos básicos
2. Captura fotos con `<CamaraPreview />`
3. Firma en `<FirmaCanvas />`
4. Click en "Guardar Inspección"
5. POST a `/inspecciones` (datos)
6. POST a `/fotos/upload` (cada foto)
7. POST a `/firmas` (firma)
8. Redirect a /inspecciones

**Estados:**
```typescript
const [numeroContenedor, setNumeroContenedor] = useState("");
const [idPlanta, setIdPlanta] = useState<number | null>(null);
const [idNaviera, setIdNaviera] = useState<number | null>(null);
const [temperatura, setTemperatura] = useState("");
const [observaciones, setObservaciones] = useState("");
const [fotos, setFotos] = useState<Blob[]>([]);
const [firma, setFirma] = useState<string | null>(null);
const [showCamera, setShowCamera] = useState(false);
const [showFirma, setShowFirma] = useState(false);
```

---

### 4. Inspecciones (`pages/Inspecciones.tsx`)

Lista de todas las inspecciones con filtros.

**Características:**
- ✅ Tabla responsive con paginación
- ✅ Filtros: fecha, estado, planta, naviera
- ✅ Búsqueda por número de contenedor
- ✅ Indicadores de estado visuales (badges)
- ✅ Click en fila → Abre modal de detalles
- ✅ Botones de acción (ver, editar, eliminar)
- ✅ Exportar lista filtrada
- ✅ Loading states

**Tabla:**
```tsx
<table>
  <thead>
    <tr>
      <th>Contenedor</th>
      <th>Planta</th>
      <th>Naviera</th>
      <th>Fecha</th>
      <th>Estado</th>
      <th>Acciones</th>
    </tr>
  </thead>
  <tbody>
    {inspecciones.map((insp) => (
      <tr key={insp.id_inspeccion} onClick={() => openModal(insp)}>
        <td>{insp.numero_contenedor}</td>
        <td>{insp.planta.nombre}</td>
        <td>{insp.naviera.nombre}</td>
        <td>{format(insp.fecha_inspeccion)}</td>
        <td><Badge estado={insp.estado} /></td>
        <td><Actions inspeccion={insp} /></td>
      </tr>
    ))}
  </tbody>
</table>
```

---

### 5. Reportes (`pages/Reportes.tsx`)

Generación de reportes con filtros avanzados.

**Características:**
- ✅ Filtros múltiples (fecha, estado, planta, naviera, inspector)
- ✅ Vista previa de datos
- ✅ Exportar a Excel
- ✅ Exportar a PDF
- ✅ Gráficos personalizados
- ✅ Resumen estadístico
- ✅ Impresión directa

**Exportación:**
```typescript
import * as XLSX from 'xlsx';
import jsPDF from 'jspdf';

// Exportar a Excel
const exportToExcel = () => {
  const ws = XLSX.utils.json_to_sheet(data);
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, 'Reporte');
  XLSX.writeFile(wb, 'reporte-inspecciones.xlsx');
};

// Exportar a PDF
const exportToPDF = () => {
  const doc = new jsPDF();
  doc.text('Reporte de Inspecciones', 10, 10);
  // ... agregar contenido
  doc.save('reporte.pdf');
};
```

---

### 6. Configuracion (`pages/Configuracion.tsx`)

Configuración de usuario y preferencias.

**Características:**
- ✅ Selector de tema (Claro/Oscuro) con preview
- ✅ Información de perfil (solo lectura)
- ✅ Toggles de notificaciones
- ✅ Información del sistema
- ✅ Cambios guardados automáticamente en localStorage

**Selector de Tema:**
```tsx
const { theme, setTheme } = useStore();

<button
  onClick={() => setTheme('light')}
  className={theme === 'light' ? 'active' : ''}
>
  ☀️ Tema Claro
</button>

<button
  onClick={() => setTheme('dark')}
  className={theme === 'dark' ? 'active' : ''}
>
  🌙 Tema Oscuro
</button>
```

---

### 7. Usuarios (`pages/Usuarios.tsx`)

Gestión de usuarios (solo admin).

**Características:**
- ✅ Lista de usuarios con roles
- ✅ Crear nuevo usuario
- ✅ Editar usuario existente
- ✅ Eliminar usuario (con confirmación)
- ✅ Cambiar rol
- ✅ Activar/desactivar usuario
- ✅ Búsqueda y filtros
- ✅ Modal de formulario

---

### 8. Plantas y Navieras (`pages/Plantas.tsx`, `pages/Navieras.tsx`)

Gestión de plantas frutícolas y navieras (admin/supervisor).

**Características:**
- ✅ CRUD completo (Create, Read, Update, Delete)
- ✅ Cards visuales con información
- ✅ Modal de creación/edición
- ✅ Activar/desactivar
- ✅ Validación de campos

---

## 🎨 Gestión de Estado

### Zustand Store (`store/index.ts`)

Store global ligero para estado compartido.

**Estado Global:**
```typescript
interface AppState {
  // Tema
  theme: 'light' | 'dark';
  setTheme: (theme: 'light' | 'dark') => void;
  toggleTheme: () => void;
  
  // Usuario
  usuarioActual: Usuario | null;
  setUsuarioActual: (usuario: Usuario | null) => void;
  
  // Toasts
  toasts: Toast[];
  addToast: (toast: Omit<Toast, 'id'>) => void;
  removeToast: (id: string) => void;
}
```

**Persistencia:**
```typescript
import { persist } from 'zustand/middleware';

export const useStore = create(
  persist(
    (set) => ({
      theme: 'light',
      setTheme: (theme) => set({ theme }),
      // ... más estado
    }),
    {
      name: 'planta-storage', // localStorage key
      partialize: (state) => ({ theme: state.theme }), // Solo persistir tema
    }
  )
);
```

**Uso en Componentes:**
```tsx
import { useStore } from '../store';

function MiComponente() {
  const { theme, setTheme } = useStore();
  
  return (
    <button onClick={() => setTheme('dark')}>
      Cambiar a oscuro
    </button>
  );
}
```

---

### AuthContext (`contexts/AuthContext.tsx`)

Context para autenticación global.

**API:**
```typescript
interface AuthContextType {
  user: Usuario | null;
  login: (correo: string, password: string) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
}

const { user, login, logout, isLoading } = useAuth();
```

**Almacenamiento:**
- Token JWT → `localStorage.getItem('token')`
- Usuario → `localStorage.getItem('user')`

**Auto-login:**
```typescript
useEffect(() => {
  const token = localStorage.getItem('token');
  if (token) {
    // Validar token y auto-login
    validateToken(token).then(setUser);
  }
}, []);
```

---

## 🎨 Estilos y Diseño

### Tailwind CSS

El proyecto usa **Tailwind CSS** con configuración personalizada:

```javascript
// tailwind.config.js
module.exports = {
  darkMode: 'class', // Activar dark mode con clase .dark
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        montserrat: ['Montserrat', 'sans-serif'],
      },
    },
  },
};
```

### Dark Mode

El sistema soporta tema oscuro/claro con persistencia:

**Aplicación del tema:**
```typescript
// App.tsx
const { theme } = useStore();

useEffect(() => {
  if (theme === 'dark') {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
}, [theme]);
```

**Clases de Tailwind:**
```tsx
<div className="bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100">
  Contenido que cambia con el tema
</div>
```

### Colores del Sistema

**Light Theme:**
```css
Background: bg-gray-100 (#F3F4F6)
Cards: bg-white (#FFFFFF)
Text: text-gray-800 (#1F2937)
Primary: bg-blue-500 (#3B82F6)
Success: bg-green-500 (#10B981)
Warning: bg-yellow-500 (#F59E0B)
Danger: bg-red-500 (#EF4444)
```

**Dark Theme:**
```css
Background: bg-gray-900 (#111827)
Cards: bg-gray-800 (#1F2937)
Text: text-gray-100 (#F3F4F6)
Primary: bg-blue-600 (#2563EB)
Success: bg-green-600 (#059669)
Warning: bg-yellow-600 (#D97706)
Danger: bg-red-600 (#DC2626)
```

### Responsive Design

Breakpoints de Tailwind:
- `sm`: 640px (móvil grande)
- `md`: 768px (tablet)
- `lg`: 1024px (laptop)
- `xl`: 1280px (desktop)
- `2xl`: 1536px (desktop grande)

**Ejemplo:**
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
  {/* 1 columna en móvil, 2 en tablet, 3 en desktop */}
</div>
```

---

## 🚀 Funcionalidades Principales

### 1. Cámara Web

**Tecnología:** `navigator.mediaDevices.getUserMedia()`

**Implementación:**
```typescript
const startCamera = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: 'user' },
      audio: false
    });
    
    if (videoRef.current) {
      videoRef.current.srcObject = stream;
    }
  } catch (error) {
    console.error('Error al acceder a la cámara:', error);
  }
};
```

**Captura de foto:**
```typescript
const takePicture = () => {
  const video = videoRef.current;
  const canvas = canvasRef.current;
  
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0);
  
  canvas.toBlob((blob) => {
    onCapture(blob);
  }, 'image/jpeg', 0.95);
};
```

---

### 2. Firma Digital

**Tecnología:** HTML5 Canvas API

**Implementación:**
```typescript
const handleMouseDown = (e: React.MouseEvent) => {
  setIsDrawing(true);
  const rect = canvasRef.current!.getBoundingClientRect();
  setLastPosition({
    x: e.clientX - rect.left,
    y: e.clientY - rect.top
  });
};

const handleMouseMove = (e: React.MouseEvent) => {
  if (!isDrawing) return;
  
  const canvas = canvasRef.current!;
  const ctx = canvas.getContext('2d')!;
  const rect = canvas.getBoundingClientRect();
  
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;
  
  ctx.beginPath();
  ctx.moveTo(lastPosition.x, lastPosition.y);
  ctx.lineTo(x, y);
  ctx.strokeStyle = '#000';
  ctx.lineWidth = 2;
  ctx.lineCap = 'round';
  ctx.stroke();
  
  setLastPosition({ x, y });
};

const saveFirma = () => {
  const canvas = canvasRef.current!;
  const firmaBase64 = canvas.toDataURL('image/png');
  onSave(firmaBase64);
};
```

---

### 3. Gráficos Interactivos

**Tecnología:** Chart.js + react-chartjs-2

**Configuración:**
```typescript
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

const chartData = {
  labels: ['Aprobadas', 'Pendientes', 'Rechazadas'],
  datasets: [{
    data: [220, 12, 15],
    backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
    borderWidth: 0
  }]
};

const options = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        color: theme === 'dark' ? '#F3F4F6' : '#1F2937'
      }
    }
  }
};

<Doughnut data={chartData} options={options} />
```

---

### 4. Exportación a Excel

**Tecnología:** xlsx (SheetJS)

**Implementación:**
```typescript
import * as XLSX from 'xlsx';

const exportToExcel = () => {
  // Preparar datos
  const data = inspecciones.map((insp) => ({
    'Contenedor': insp.numero_contenedor,
    'Planta': insp.planta.nombre,
    'Naviera': insp.naviera.nombre,
    'Temperatura': insp.temperatura,
    'Estado': insp.estado,
    'Fecha': format(insp.fecha_inspeccion, 'dd/MM/yyyy')
  }));
  
  // Crear hoja
  const ws = XLSX.utils.json_to_sheet(data);
  
  // Ajustar anchos de columna
  ws['!cols'] = [
    { wch: 15 }, // Contenedor
    { wch: 20 }, // Planta
    { wch: 20 }, // Naviera
    { wch: 12 }, // Temperatura
    { wch: 12 }, // Estado
    { wch: 12 }  // Fecha
  ];
  
  // Crear libro
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, 'Inspecciones');
  
  // Descargar
  XLSX.writeFile(wb, `inspecciones-${format(new Date(), 'yyyy-MM-dd')}.xlsx`);
};
```

---

## 🛠️ Instalación y Configuración

### 1. Requisitos Previos

- Node.js 18 o superior
- npm o yarn
- Backend corriendo en http://localhost:8000

### 2. Clonar Repositorio

```bash
git clone <repo-url>
cd frontend
```

### 3. Instalar Dependencias

```bash
npm install
```

### 4. Configurar Variables de Entorno

Crear archivo `.env` en la raíz:

```env
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Inspección de Contenedores
```

### 5. Iniciar Servidor de Desarrollo

```bash
npm run dev
```

La aplicación estará disponible en: **http://localhost:5173**

---

## 📦 Build y Despliegue

### Build de Producción

```bash
npm run build
```

Genera archivos optimizados en `dist/`:
- HTML minificado
- CSS con PurgeCSS (solo clases usadas)
- JavaScript con tree-shaking y code-splitting
- Assets optimizados

### Preview del Build

```bash
npm run preview
```

### Análisis del Bundle

```bash
npm run build -- --report
```

### Optimizaciones Aplicadas

- ✅ **Code Splitting**: Lazy loading de rutas
- ✅ **Tree Shaking**: Eliminación de código no usado
- ✅ **Minificación**: HTML, CSS, JS comprimidos
- ✅ **Asset Optimization**: Imágenes y fonts optimizados
- ✅ **Caching**: Hashes en archivos para cache busting
- ✅ **Lazy Loading**: Componentes cargados bajo demanda

---

## 🧪 Testing (Opcional)

El proyecto puede extenderse con:

```bash
# Instalar dependencias de testing
npm install -D @testing-library/react @testing-library/jest-dom vitest

# Ejecutar tests
npm run test
```

---

## 🌐 Despliegue en Producción

### Deploy en Nginx (VPS)

Ver el archivo `instruccion_despliegue-produccion.md` para instrucciones detalladas.

**Resumen:**
1. Build de producción: `npm run build`
2. Copiar carpeta `dist/` al servidor
3. Configurar Nginx para servir archivos estáticos
4. Configurar HTTPS con Let's Encrypt
5. Configurar variables de entorno de producción

### Deploy en Vercel/Netlify

```bash
# Vercel
npm install -g vercel
vercel --prod

# Netlify
npm install -g netlify-cli
netlify deploy --prod --dir=dist
```

---

## 📊 Estructura de Rutas

```
/                          → Redirect a /login o /dashboard
/login                     → Página de login (pública)

Rutas Protegidas:
/dashboard                 → Dashboard principal
/inspeccion-nueva          → Formulario nueva inspección
/inspecciones              → Lista de inspecciones
/reportes                  → Generación de reportes
/plantas                   → Gestión de plantas (supervisor+)
/navieras                  → Gestión de navieras (supervisor+)
/usuarios                  → Gestión de usuarios (admin)
/configuracion             → Configuración de usuario
/admin                     → Panel de administración (admin)
```

---

## 🎯 Mejores Prácticas Implementadas

1. **TypeScript**: Tipado estático para prevenir errores
2. **Component Composition**: Componentes pequeños y reutilizables
3. **Custom Hooks**: Lógica compartida extraída
4. **Error Boundaries**: Manejo de errores en componentes
5. **Lazy Loading**: Carga diferida de componentes pesados
6. **Memoization**: `useMemo` y `useCallback` para optimizar
7. **Accesibilidad**: ARIA labels, keyboard navigation
8. **SEO**: Meta tags, títulos dinámicos
9. **Progressive Enhancement**: Funciona sin JavaScript básico
10. **Mobile First**: Diseño responsive desde móvil

---

## 📚 Referencias Adicionales

- [React Documentation](https://react.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Zustand Documentation](https://zustand-demo.pmnd.rs/)
- [React Router Documentation](https://reactrouter.com/)
- [Chart.js Documentation](https://www.chartjs.org/docs/)

---

## 🐛 Troubleshooting

### Problema: Cámara no funciona

**Solución:**
- Verificar permisos del navegador
- Usar HTTPS (getUserMedia requiere contexto seguro)
- Verificar que el dispositivo tenga cámara

### Problema: Dark mode no cambia

**Solución:**
- Limpiar localStorage: `localStorage.clear()`
- Recargar página: `Ctrl + Shift + R`
- Verificar que Tailwind esté configurado con `darkMode: 'class'`

### Problema: Build falla

**Solución:**
```bash
# Limpiar cache y reinstalar
rm -rf node_modules dist .vite
npm install
npm run build
```

---

**Última actualización:** Octubre 2025  
**Versión del Frontend:** 1.0.0
