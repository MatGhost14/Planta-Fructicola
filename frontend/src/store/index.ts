/**
 * Store global con Zustand
 */
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { ToastMessage } from '../types';

type Theme = 'light' | 'dark';

interface AppState {
  // Toasts
  toasts: ToastMessage[];
  addToast: (mensaje: string, tipo?: ToastMessage['tipo']) => void;
  removeToast: (id: string) => void;
  
  // Tema
  theme: Theme;
  setTheme: (theme: Theme) => void;
  toggleTheme: () => void;
  
  // Usuario actual (mock)
  usuarioActual: {
    id_usuario: number;
    nombre: string;
    correo: string;
    rol: string;
  };
}

export const useStore = create<AppState>()(
  persist(
    (set) => ({
      // Toasts
      toasts: [],
      addToast: (mensaje, tipo = 'exito') => {
        const id = `toast-${Date.now()}`;
        set((state) => ({
          toasts: [...state.toasts, { id, mensaje, tipo }],
        }));
        
        // Auto-remover después de 3 segundos
        setTimeout(() => {
          set((state) => ({
            toasts: state.toasts.filter((t) => t.id !== id),
          }));
        }, 3000);
      },
      removeToast: (id) =>
        set((state) => ({
          toasts: state.toasts.filter((t) => t.id !== id),
        })),
      
      // Tema
      theme: 'light',
      setTheme: (theme) => {
        set({ theme });
        // Aplicar clase al documento inmediatamente
        const html = document.documentElement;
        
        // Limpiar todas las clases de tema primero
        html.classList.remove('dark', 'light');
        
        // Aplicar la nueva clase y atributo
        if (theme === 'dark') {
          html.classList.add('dark');
          html.setAttribute('data-theme', 'dark');
        } else {
          html.classList.add('light');
          html.setAttribute('data-theme', 'light');
        }
        
        // Forzar actualización del DOM
        void html.offsetHeight;
        
        console.log('✅ setTheme llamado con:', theme);
        console.log('   - classList:', html.className);
        console.log('   - Tiene dark?:', html.classList.contains('dark'));
        console.log('   - data-theme:', html.getAttribute('data-theme'));
      },
      toggleTheme: () => {
        set((state) => {
          const newTheme = state.theme === 'light' ? 'dark' : 'light';
          // Aplicar clase al documento inmediatamente
          const html = document.documentElement;
          
          // Limpiar todas las clases de tema primero
          html.classList.remove('dark', 'light');
          
          // Aplicar la nueva clase
          if (newTheme === 'dark') {
            html.classList.add('dark');
          } else {
            html.classList.add('light');
          }
          
          // Forzar actualización del DOM
          void html.offsetHeight;
          
          console.log('✅ Tema toggled a:', newTheme, '| Clase dark:', html.classList.contains('dark'));
          return { theme: newTheme };
        });
      },
      
      // Usuario actual (mock - en producción vendría de auth)
      usuarioActual: {
        id_usuario: 1,
        nombre: 'Juan Díaz',
        correo: 'juan.diaz@empresa.com',
        rol: 'inspector',
      },
    }),
    {
      name: 'planta-storage',
      partialize: (state) => ({ theme: state.theme }),
      onRehydrateStorage: () => (state) => {
        // Aplicar tema inmediatamente después de cargar desde localStorage
        const html = document.documentElement;
        const savedTheme = state?.theme || 'light';
        
        // Limpiar todas las clases de tema primero
        html.classList.remove('dark', 'light');
        
        // Aplicar el tema guardado
        if (savedTheme === 'dark') {
          html.classList.add('dark');
        } else {
          html.classList.add('light');
        }
        
        // Forzar actualización del DOM
        void html.offsetHeight;
        
        console.log('🔄 Tema rehidratado:', savedTheme, '| Clase dark:', html.classList.contains('dark'));
      },
    }
  )
);
