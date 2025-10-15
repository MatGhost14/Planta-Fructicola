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
        // Aplicar clase al documento
        if (theme === 'dark') {
          document.documentElement.classList.add('dark');
        } else {
          document.documentElement.classList.remove('dark');
        }
      },
      toggleTheme: () => {
        set((state) => {
          const newTheme = state.theme === 'light' ? 'dark' : 'light';
          // Aplicar clase al documento
          if (newTheme === 'dark') {
            document.documentElement.classList.add('dark');
          } else {
            document.documentElement.classList.remove('dark');
          }
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
    }
  )
);
