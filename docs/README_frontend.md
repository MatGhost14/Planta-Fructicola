# Frontend - Sistema de Inspección de Contenedores

## 📋 Descripción

Frontend desarrollado en **React + TypeScript + Vite** para el sistema de inspección de contenedores frutícolas. Proporciona una interfaz moderna y responsive para la gestión completa del sistema.

## 🏗️ Arquitectura

```
frontend/
├── src/
│   ├── api/            # Servicios de API
│   ├── components/     # Componentes reutilizables
│   ├── contexts/       # Contextos de React
│   ├── pages/          # Páginas principales
│   ├── store/          # Estado global (Zustand)
│   ├── types/          # Definiciones TypeScript
│   └── utils/          # Utilidades
├── public/             # Archivos estáticos
└── dist/               # Build de producción
```

## 🚀 Tecnologías

- **React 18** - Biblioteca de UI
- **TypeScript** - Tipado estático
- **Vite** - Build tool moderno
- **Tailwind CSS** - Framework de CSS
- **React Router** - Enrutamiento
- **Axios** - Cliente HTTP
- **Zustand** - Estado global
- **React Hook Form** - Manejo de formularios

## 📦 Instalación

### Prerrequisitos

- Node.js 16+
- npm 8+ o yarn 1.22+

### Configuración

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd Planta-/frontend
   ```

2. **Instalar dependencias**
   ```bash
   npm install
   # o
   yarn install
   ```

3. **Configurar variables de entorno**
   ```bash
   # Crear archivo .env.local
   cp .env.example .env.local
   # Editar .env.local con tus configuraciones
   ```

## ⚙️ Configuración

### Variables de Entorno

Crear archivo `.env.local` en la raíz del frontend:

```env
# API Backend
VITE_API_URL=http://localhost:8000/api
VITE_API_TIMEOUT=30000

# Aplicación
VITE_APP_NAME=Sistema de Inspección de Contenedores
VITE_APP_VERSION=2.1.0

# Desarrollo
VITE_DEV_MODE=true
VITE_DEBUG=false
```

## 🚀 Ejecución

### Desarrollo

```bash
# Iniciar servidor de desarrollo
npm run dev

# Con puerto específico
npm run dev -- --port 3000
```

### Producción

```bash
# Build para producción
npm run build

# Preview del build
npm run preview
```

## 🎨 Diseño y UI

### Sistema de Diseño

- **Colores**: Paleta azul/índigo con acentos
- **Tipografía**: Inter (sistema)
- **Espaciado**: Sistema de 4px (4, 8, 12, 16, 24, 32...)
- **Componentes**: Diseño consistente y reutilizable

### Responsive Design

- **Mobile First**: Diseño optimizado para móviles
- **Breakpoints**: 
  - `sm`: 640px
  - `md`: 768px
  - `lg`: 1024px
  - `xl`: 1280px

### Tema

El sistema soporta tema claro/oscuro con persistencia en localStorage.

## 🔐 Autenticación

### Flujo de Autenticación

1. **Login**: Formulario con validación
2. **Token Storage**: JWT en localStorage
3. **Protected Routes**: Rutas protegidas por rol
4. **Auto-logout**: Expiración automática de sesión

### Roles y Permisos

- **Inspector**: Crear inspecciones, ver propias
- **Supervisor**: Gestionar planta, aprobar inspecciones
- **Admin**: Acceso completo al sistema

## 📱 Páginas Principales

### Login
- Formulario de autenticación
- Validación en tiempo real
- Credenciales de prueba (desarrollo)

### Dashboard
- Estadísticas generales
- Gráficos de inspecciones
- Accesos rápidos

### Inspecciones
- Lista de inspecciones
- Filtros y búsqueda
- Estados (pendiente, aprobado, rechazado)

### Nueva Inspección
- Formulario paso a paso
- Cámara integrada
- Firma digital
- Validaciones

### Reportes
- Exportación PDF
- Filtros por fecha/planta
- Estadísticas detalladas

## 🧩 Componentes

### Componentes Principales

- **Layout**: Estructura principal con sidebar
- **ProtectedRoute**: Protección de rutas
- **ToastContainer**: Notificaciones
- **FirmaCanvas**: Canvas para firmas
- **CamaraPreview**: Preview de cámara

### Componentes de Formulario

- Inputs con validación
- Selects con búsqueda
- Date pickers
- File uploads

## 🔄 Estado Global

### Zustand Store

```typescript
interface Store {
  theme: 'light' | 'dark';
  setTheme: (theme: 'light' | 'dark') => void;
  addToast: (message: string, type: ToastType) => void;
  removeToast: (id: string) => void;
}
```

### Contextos

- **AuthContext**: Autenticación y usuario
- **ToastProvider**: Notificaciones globales

## 🌐 API Integration

### Servicios de API

```typescript
// Ejemplo de uso
import { plantasApi } from '@/api/plantas';

const plantas = await plantasApi.getAll();
```

### Manejo de Errores

- Interceptores de Axios
- Retry automático
- Mensajes de error amigables

## 📱 PWA Features

### Service Worker

- Caché de recursos estáticos
- Funcionamiento offline básico
- Actualizaciones automáticas

### Manifest

- Iconos de aplicación
- Colores del tema
- Configuración de pantalla

## 🧪 Testing

```bash
# Ejecutar pruebas
npm run test

# Con cobertura
npm run test:coverage

# Pruebas E2E
npm run test:e2e
```

## 🚀 Build y Despliegue

### Build de Producción

```bash
# Build optimizado
npm run build

# Análisis del bundle
npm run build:analyze
```

### Variables de Producción

```env
VITE_API_URL=https://api.tudominio.com/api
VITE_DEV_MODE=false
```

## 📱 Responsive Design

### Breakpoints

```css
/* Mobile First */
.container {
  @apply px-4 py-2;
}

/* Tablet */
@media (min-width: 768px) {
  .container {
    @apply px-6 py-4;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    @apply px-8 py-6;
  }
}
```

## 🎨 Styling

### Tailwind CSS

- **Utility-first**: Clases utilitarias
- **Custom Components**: Componentes personalizados
- **Dark Mode**: Soporte nativo
- **Responsive**: Mobile-first approach

### Estructura de Clases

```css
/* Componente de botón */
.btn {
  @apply px-4 py-2 rounded-lg font-medium transition-colors;
}

.btn-primary {
  @apply bg-blue-600 text-white hover:bg-blue-700;
}
```

## 🔧 Scripts Disponibles

```bash
# Desarrollo
npm run dev          # Servidor de desarrollo
npm run dev:host     # Servidor con acceso externo

# Build
npm run build        # Build de producción
npm run preview      # Preview del build

# Testing
npm run test         # Pruebas unitarias
npm run test:watch   # Pruebas en modo watch
npm run test:coverage # Pruebas con cobertura

# Linting
npm run lint         # ESLint
npm run lint:fix     # ESLint con auto-fix
npm run type-check   # Verificación de tipos
```

## 📦 Dependencias Principales

### Core
- `react` - Biblioteca principal
- `react-dom` - DOM renderer
- `react-router-dom` - Enrutamiento

### UI/UX
- `tailwindcss` - Framework CSS
- `@headlessui/react` - Componentes accesibles
- `@heroicons/react` - Iconos

### Estado y Datos
- `zustand` - Estado global
- `axios` - Cliente HTTP
- `react-hook-form` - Formularios

### Utilidades
- `date-fns` - Manipulación de fechas
- `clsx` - Utilidad para clases CSS
- `react-hot-toast` - Notificaciones

## 🐛 Debugging

### Herramientas de Desarrollo

- **React DevTools**: Extensión del navegador
- **Redux DevTools**: Para estado global
- **Network Tab**: Monitoreo de API calls

### Console Logs

```typescript
// Desarrollo
if (import.meta.env.DEV) {
  console.log('Debug info:', data);
}
```

## 🚀 Optimizaciones

### Performance

- **Code Splitting**: Carga lazy de componentes
- **Bundle Analysis**: Análisis del bundle
- **Image Optimization**: Optimización de imágenes
- **Caching**: Estrategias de caché

### SEO

- **Meta Tags**: Configuración dinámica
- **Sitemap**: Generación automática
- **Structured Data**: Datos estructurados

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

