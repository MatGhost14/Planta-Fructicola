/**
 * Servicio de autenticación
 */
import axios from './axios';

export interface LoginCredentials {
  correo: string;
  password: string;
}

export interface TokenData {
  id_usuario: number;
  correo: string;
  rol: 'inspector' | 'supervisor' | 'admin';
  nombre: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  usuario: TokenData;
  expires_in: number;
}

export interface SessionInfo {
  id_usuario: number;
  nombre: string;
  correo: string;
  rol: 'inspector' | 'supervisor' | 'admin';
  estado: 'active' | 'inactive';
  ultimo_acceso: string | null;
  permisos: Record<string, string[]>;
}

export interface PasswordChange {
  password_actual: string;
  password_nueva: string;
}

class AuthService {
  private TOKEN_KEY = 'auth_token';
  private USER_KEY = 'auth_user';

  /**
   * Login de usuario
   */
  async login(credentials: LoginCredentials): Promise<LoginResponse> {
    const response = await axios.post<LoginResponse>('/auth/login', credentials);
    
    // Guardar token y usuario en localStorage
    this.setToken(response.data.access_token);
    this.setUser(response.data.usuario);
    
    // Configurar header de autorización
    axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access_token}`;
    
    return response.data;
  }

  /**
   * Logout de usuario
   */
  async logout(): Promise<void> {
    try {
      await axios.post('/auth/logout');
    } catch (error) {
      console.error('Error en logout:', error);
    } finally {
      this.clearAuth();
    }
  }

  /**
   * Obtener información de sesión actual
   */
  async getSessionInfo(): Promise<SessionInfo> {
    const response = await axios.get<SessionInfo>('/auth/me');
    return response.data;
  }

  /**
   * Cambiar contraseña
   */
  async changePassword(data: PasswordChange): Promise<void> {
    await axios.post('/auth/change-password', data);
  }

  /**
   * Renovar token
   */
  async refreshToken(): Promise<LoginResponse> {
    const response = await axios.post<LoginResponse>('/auth/refresh');
    
    // Actualizar token
    this.setToken(response.data.access_token);
    this.setUser(response.data.usuario);
    
    axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access_token}`;
    
    return response.data;
  }

  /**
   * Guardar token
   */
  setToken(token: string): void {
    localStorage.setItem(this.TOKEN_KEY, token);
  }

  /**
   * Obtener token
   */
  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  /**
   * Guardar usuario
   */
  setUser(user: TokenData): void {
    localStorage.setItem(this.USER_KEY, JSON.stringify(user));
  }

  /**
   * Obtener usuario
   */
  getUser(): TokenData | null {
    const userStr = localStorage.getItem(this.USER_KEY);
    if (!userStr) return null;
    
    try {
      return JSON.parse(userStr);
    } catch {
      return null;
    }
  }

  /**
   * Verificar si está autenticado
   */
  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  /**
   * Limpiar datos de autenticación
   */
  clearAuth(): void {
    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem(this.USER_KEY);
    delete axios.defaults.headers.common['Authorization'];
  }

  /**
   * Inicializar autenticación desde localStorage
   */
  initializeAuth(): void {
    const token = this.getToken();
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    }
  }

  /**
   * Verificar permisos
   */
  hasPermission(rol: string, module: string, action: string): boolean {
    // Admin tiene todos los permisos
    if (rol === 'admin') return true;
    
    // Definir permisos por rol
    const permissions: Record<string, Record<string, string[]>> = {
      inspector: {
        inspecciones: ['read_own', 'create', 'update_own'],
        fotos: ['upload', 'view_own'],
        firmas: ['create'],
        reportes: ['view_own'],
        preferencias: ['read', 'update']
      },
      supervisor: {
        inspecciones: ['read_all_planta', 'create', 'update', 'approve', 'reject'],
        fotos: ['view_all_planta'],
        firmas: ['view_all_planta'],
        reportes: ['view_planta'],
        plantas: ['read', 'update'],
        navieras: ['read', 'create', 'update'],
        usuarios: ['read_planta'],
        bitacora: ['read_planta'],
        preferencias: ['read', 'update']
      }
    };
    
    const rolePermissions = permissions[rol];
    if (!rolePermissions) return false;
    
    const modulePermissions = rolePermissions[module];
    if (!modulePermissions) return false;
    
    return modulePermissions.includes(action) || modulePermissions.includes('full_access');
  }

  /**
   * Verificar si tiene un rol específico
   */
  hasRole(requiredRole: 'inspector' | 'supervisor' | 'admin'): boolean {
    const user = this.getUser();
    if (!user) return false;
    
    const roleHierarchy = {
      inspector: 1,
      supervisor: 2,
      admin: 3
    };
    
    return roleHierarchy[user.rol] >= roleHierarchy[requiredRole];
  }
}

export const authService = new AuthService();
export default authService;
