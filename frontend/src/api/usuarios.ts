/**
 * Servicio API para usuarios
 */
import axios from './axios';
import type { Usuario, UsuarioCreate, UsuarioUpdate, ApiMessage } from '../types';

export const usuariosApi = {
  /**
   * Obtener todos los usuarios
   */
  listar: async (includeInactive = false): Promise<Usuario[]> => {
    const response = await axios.get<Usuario[]>('/usuarios', {
      params: { include_inactive: includeInactive },
    });
    return response.data;
  },

  /**
   * Crear nuevo usuario
   */
  crear: async (data: UsuarioCreate): Promise<Usuario> => {
    const response = await axios.post<Usuario>('/usuarios', data);
    return response.data;
  },

  /**
   * Actualizar usuario
   */
  actualizar: async (id: number, data: UsuarioUpdate): Promise<Usuario> => {
    const response = await axios.put<Usuario>(`/usuarios/${id}`, data);
    return response.data;
  },

  /**
   * Cambiar estado de usuario
   */
  cambiarEstado: async (id: number, estado: 'active' | 'inactive'): Promise<Usuario> => {
    const response = await axios.patch<Usuario>(`/usuarios/${id}/estado`, { estado });
    return response.data;
  },

  /**
   * Eliminar usuario
   */
  eliminar: async (id: number): Promise<ApiMessage> => {
    const response = await axios.delete<ApiMessage>(`/usuarios/${id}`);
    return response.data;
  },
};
