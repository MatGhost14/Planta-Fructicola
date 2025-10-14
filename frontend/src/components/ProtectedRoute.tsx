/**
 * Componente para proteger rutas según autenticación y roles
 */
import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

interface ProtectedRouteProps {
  requireRole?: 'inspector' | 'supervisor' | 'admin' | Array<'inspector' | 'supervisor' | 'admin'>;
  children?: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ requireRole, children }) => {
  const { isAuthenticated, user, loading } = useAuth();

  // Mostrar loading mientras se verifica autenticación
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Cargando...</p>
        </div>
      </div>
    );
  }

  // Si no está autenticado, redirigir al login
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // Si se requiere un rol específico, verificar
  if (requireRole && user) {
    const allowedRoles = Array.isArray(requireRole) ? requireRole : [requireRole];
    
    // Verificar si el rol del usuario está en la lista de roles permitidos
    if (!allowedRoles.includes(user.rol as any)) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
          <div className="text-center p-8 bg-white rounded-lg shadow-lg max-w-md">
            <svg className="mx-auto h-12 w-12 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <h2 className="mt-4 text-xl font-semibold text-gray-900">Acceso Denegado</h2>
            <p className="mt-2 text-gray-600">
              No tienes permisos para acceder a esta sección.
            </p>
            <p className="mt-1 text-sm text-gray-500">
              Se requiere rol: <span className="font-semibold">{allowedRoles.join(' o ')}</span>
            </p>
            <button
              onClick={() => window.history.back()}
              className="mt-6 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Volver
            </button>
          </div>
        </div>
      );
    }
  }

  // Si pasa todas las verificaciones, renderizar el contenido
  return children ? <>{children}</> : <Outlet />;
};

export default ProtectedRoute;
