/**
 * Store global con Zustand
 */
import { create } from 'zustand';
import type { ToastMessage } from '../types';

interface AppState {
  // Toasts
  toasts: ToastMessage[];
  addToast: (mensaje: string, tipo?: ToastMessage['tipo']) => void;
  removeToast: (id: string) => void;
  
  // Usuario actual (mock)
  usuarioActual: {
    id_usuario: number;
    nombre: string;
    correo: string;
    rol: string;
  };
}

export const useStore = create<AppState>((set) => ({
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
  
  // Usuario actual (mock - en producción vendría de auth)
  usuarioActual: {
    id_usuario: 1,
    nombre: 'Juan Díaz',
    correo: 'juan.diaz@empresa.com',
    rol: 'inspector',
  },
}));
