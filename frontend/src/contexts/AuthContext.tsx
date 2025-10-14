/**
 * Context de Autenticación
 */
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import authService, { LoginCredentials, TokenData, SessionInfo } from '../api/auth';
import { useStore } from '../store';

interface AuthContextType {
  user: TokenData | null;
  sessionInfo: SessionInfo | null;
  loading: boolean;
  isAuthenticated: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => Promise<void>;
  refreshSession: () => Promise<void>;
  hasPermission: (module: string, action: string) => boolean;
  hasRole: (role: 'inspector' | 'supervisor' | 'admin') => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe ser usado dentro de un AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<TokenData | null>(null);
  const [sessionInfo, setSessionInfo] = useState<SessionInfo | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const addToast = useStore((state) => state.addToast);

  // Inicializar autenticación al cargar
  useEffect(() => {
    initializeAuth();
  }, []);

  const initializeAuth = async () => {
    try {
      authService.initializeAuth();
      const token = authService.getToken();
      const storedUser = authService.getUser();

      if (token && storedUser) {
        setUser(storedUser);
        
        // Obtener información de sesión actualizada
        try {
          const session = await authService.getSessionInfo();
          setSessionInfo(session);
        } catch (error) {
          // Si falla, limpiar autenticación
          authService.clearAuth();
          setUser(null);
        }
      }
    } catch (error) {
      console.error('Error inicializando autenticación:', error);
    } finally {
      setLoading(false);
    }
  };

  const login = async (credentials: LoginCredentials) => {
    try {
      const response = await authService.login(credentials);
      setUser(response.usuario);
      
      // Obtener información de sesión
      const session = await authService.getSessionInfo();
      setSessionInfo(session);
      
      addToast(`¡Bienvenido ${response.usuario.nombre}!`, 'exito');
      
      // Redirigir según rol
      navigate('/dashboard');
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Error al iniciar sesión';
      addToast(message, 'error');
      throw error;
    }
  };

  const logout = async () => {
    try {
      await authService.logout();
      setUser(null);
      setSessionInfo(null);
      addToast('Sesión cerrada', 'info');
      navigate('/login');
    } catch (error) {
      console.error('Error en logout:', error);
      // Limpiar de todas formas
      authService.clearAuth();
      setUser(null);
      setSessionInfo(null);
      navigate('/login');
    }
  };

  const refreshSession = async () => {
    try {
      const session = await authService.getSessionInfo();
      setSessionInfo(session);
      
      // Actualizar usuario también
      const storedUser = authService.getUser();
      if (storedUser) {
        setUser(storedUser);
      }
    } catch (error) {
      console.error('Error refrescando sesión:', error);
      // Si falla, cerrar sesión
      await logout();
    }
  };

  const hasPermission = (module: string, action: string): boolean => {
    if (!user) return false;
    return authService.hasPermission(user.rol, module, action);
  };

  const hasRole = (role: 'inspector' | 'supervisor' | 'admin'): boolean => {
    return authService.hasRole(role);
  };

  const value: AuthContextType = {
    user,
    sessionInfo,
    loading,
    isAuthenticated: !!user,
    login,
    logout,
    refreshSession,
    hasPermission,
    hasRole
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthContext;
