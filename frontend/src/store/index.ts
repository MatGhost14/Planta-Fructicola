/**
 * Store global con Zustand
 */
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

type Theme = 'light' | 'dark';

interface AppState {
  // Tema
  theme: Theme;
  setTheme: (theme: Theme) => void;
  toggleTheme: () => void;
}

export const useStore = create<AppState>()(
  persist(
    (set) => ({
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
