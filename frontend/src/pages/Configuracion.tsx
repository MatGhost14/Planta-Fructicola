import React from 'react';
import { useStore } from '../store';
import { useToast } from '../components/ToastProvider';

const Configuracion: React.FC = () => {
  const { theme, setTheme, usuarioActual } = useStore();
  const { showSuccess } = useToast();

  const handleThemeChange = (newTheme: 'light' | 'dark') => {
    console.log('Cambiando tema a:', newTheme);
    setTheme(newTheme);
    console.log('Clase dark en HTML:', document.documentElement.classList.contains('dark'));
    showSuccess(`Tema ${newTheme === 'dark' ? 'oscuro' : 'claro'} activado`);
  };

  return (
    <div className="py-2">
      {/* Header */}
      <div className="mb-8">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-gray-800 dark:text-gray-100">
              ⚙️ Configuración
            </h1>
            <p className="text-sm sm:text-base text-gray-600 dark:text-gray-400 mt-2">
              Personaliza tu experiencia en el sistema
            </p>
          </div>
        </div>
      </div>

      {/* Contenido */}
      <div className="space-y-6">
        {/* Perfil de Usuario */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-card p-5 sm:p-6">
          <h2 className="text-lg sm:text-xl font-semibold text-gray-800 dark:text-gray-100 mb-5 sm:mb-6">
            👤 Perfil de Usuario
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Nombre
              </label>
              <input
                type="text"
                value={usuarioActual.nombre}
                disabled
                className="input-field bg-gray-50 dark:bg-gray-700 dark:text-gray-300 dark:border-gray-600 cursor-not-allowed"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Correo Electrónico
              </label>
              <input
                type="email"
                value={usuarioActual.correo}
                disabled
                className="input-field bg-gray-50 dark:bg-gray-700 dark:text-gray-300 dark:border-gray-600 cursor-not-allowed"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Rol
              </label>
              <input
                type="text"
                value={usuarioActual.rol.charAt(0).toUpperCase() + usuarioActual.rol.slice(1)}
                disabled
                className="input-field bg-gray-50 dark:bg-gray-700 dark:text-gray-300 dark:border-gray-600 cursor-not-allowed"
              />
            </div>
          </div>
        </div>

        {/* Apariencia */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-card p-5 sm:p-6">
          <h2 className="text-lg sm:text-xl font-semibold text-gray-800 dark:text-gray-100 mb-5 sm:mb-6">
            🎨 Apariencia
          </h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                Tema de la Interfaz
              </label>
              <p className="text-xs text-gray-500 dark:text-gray-400 mb-4">
                Selecciona el tema que prefieras para la aplicación
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {/* Tema Claro */}
              <button
                onClick={() => handleThemeChange('light')}
                className={`relative p-6 rounded-xl border-2 transition-all duration-200 ${
                  theme === 'light'
                    ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                    : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
                }`}
              >
                {/* Check Badge */}
                {theme === 'light' && (
                  <div className="absolute top-3 right-3 w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center">
                    <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                )}

                {/* Icono y Preview */}
                <div className="flex items-center gap-4 mb-3">
                  <div className="w-12 h-12 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-full flex items-center justify-center text-white shadow-lg">
                    <svg className="w-7 h-7" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="text-left flex-1">
                    <h3 className="font-semibold text-gray-900 dark:text-gray-100">Tema Claro</h3>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">Interfaz luminosa</p>
                  </div>
                </div>

                {/* Miniatura */}
                <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-2 space-y-1.5 shadow-sm">
                  <div className="h-2 bg-blue-500 rounded w-1/3"></div>
                  <div className="h-2 bg-gray-200 rounded w-full"></div>
                  <div className="h-2 bg-gray-200 rounded w-2/3"></div>
                </div>
              </button>

              {/* Tema Oscuro */}
              <button
                onClick={() => handleThemeChange('dark')}
                className={`relative p-6 rounded-xl border-2 transition-all duration-200 ${
                  theme === 'dark'
                    ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                    : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
                }`}
              >
                {/* Check Badge */}
                {theme === 'dark' && (
                  <div className="absolute top-3 right-3 w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center">
                    <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                )}

                {/* Icono y Preview */}
                <div className="flex items-center gap-4 mb-3">
                  <div className="w-12 h-12 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-full flex items-center justify-center text-white shadow-lg">
                    <svg className="w-7 h-7" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
                    </svg>
                  </div>
                  <div className="text-left flex-1">
                    <h3 className="font-semibold text-gray-900 dark:text-gray-100">Tema Oscuro</h3>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">Interfaz nocturna</p>
                  </div>
                </div>

                {/* Miniatura */}
                <div className="bg-gray-800 border border-gray-700 rounded-lg p-2 space-y-1.5 shadow-sm">
                  <div className="h-2 bg-blue-500 rounded w-1/3"></div>
                  <div className="h-2 bg-gray-700 rounded w-full"></div>
                  <div className="h-2 bg-gray-700 rounded w-2/3"></div>
                </div>
              </button>
            </div>
          </div>

          {/* Beneficios del Tema Oscuro */}
          {theme === 'dark' && (
            <div className="mt-6 p-4 bg-indigo-50 dark:bg-indigo-900/20 border border-indigo-200 dark:border-indigo-800 rounded-lg">
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0">
                  <svg className="w-5 h-5 text-indigo-600 dark:text-indigo-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="flex-1">
                  <h4 className="text-sm font-medium text-indigo-900 dark:text-indigo-300 mb-1">
                    Modo Nocturno Activado
                  </h4>
                  <p className="text-xs text-indigo-700 dark:text-indigo-400">
                    Reduce la fatiga visual en ambientes con poca luz y ahorra energía en pantallas OLED.
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Notificaciones */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-card p-5 sm:p-6">
          <h2 className="text-lg sm:text-xl font-semibold text-gray-800 dark:text-gray-100 mb-5 sm:mb-6">
            🔔 Notificaciones
          </h2>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
              <div className="flex-1">
                <h3 className="font-medium text-gray-900 dark:text-gray-100">Notificaciones de Éxito</h3>
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                  Mostrar mensajes cuando las acciones se completen exitosamente
                </p>
              </div>
              <div className="ml-4">
                <label className="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" className="sr-only peer" defaultChecked />
                  <div className="w-11 h-6 bg-gray-300 dark:bg-gray-600 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                </label>
              </div>
            </div>

            <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
              <div className="flex-1">
                <h3 className="font-medium text-gray-900 dark:text-gray-100">Notificaciones de Error</h3>
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                  Alertas cuando ocurran problemas o errores
                </p>
              </div>
              <div className="ml-4">
                <label className="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" className="sr-only peer" defaultChecked />
                  <div className="w-11 h-6 bg-gray-300 dark:bg-gray-600 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                </label>
              </div>
            </div>
          </div>
        </div>

        {/* Información del Sistema */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-card p-5 sm:p-6">
          <h2 className="text-lg sm:text-xl font-semibold text-gray-800 dark:text-gray-100 mb-5 sm:mb-6">
            ℹ️ Información del Sistema
          </h2>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
              <p className="text-sm text-gray-500 dark:text-gray-400">Versión</p>
              <p className="text-lg font-semibold text-gray-900 dark:text-gray-100 mt-1">1.0.0</p>
            </div>
            <div className="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
              <p className="text-sm text-gray-500 dark:text-gray-400">Última Actualización</p>
              <p className="text-lg font-semibold text-gray-900 dark:text-gray-100 mt-1">Octubre 2025</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Configuracion;
