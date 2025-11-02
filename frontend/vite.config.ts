import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  // Cargar variables de entorno de Vite (.env, .env.local, etc.)
  // Usar '.' como directorio base en lugar de process.cwd()
  const env = loadEnv(mode, '.', '')
  // Prioridad: VITE_API_URL (archivo .env o variable de entorno de Vite) -> fallback 8001 (backend local típico)
  const apiTarget = env.VITE_API_URL || 'http://localhost:8001'

  return {
    plugins: [react()],
    server: {
      host: '0.0.0.0',
      port: 5173,
      watch: {
        usePolling: true,
      },
      proxy: {
        '/api': {
          target: apiTarget,
          changeOrigin: true,
        },
        '/capturas': {
          target: apiTarget,
          changeOrigin: true,
        },
      },
    },
  }
})
