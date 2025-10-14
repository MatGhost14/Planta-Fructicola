/**
 * Servicio API para preferencias
 */
import axios from './axios';
import type { PreferenciaUsuario, PreferenciaUsuarioUpdate } from '../types';

export const preferenciasApi = {
  /**
   * Obtener preferencias de un usuario
   */
  obtener: async (idUsuario: number): Promise<PreferenciaUsuario> => {
    const response = await axios.get<PreferenciaUsuario>(`/preferencias/${idUsuario}`);
    return response.data;
  },

  /**
   * Actualizar preferencias de un usuario
   */
  actualizar: async (
    idUsuario: number,
    data: PreferenciaUsuarioUpdate
  ): Promise<PreferenciaUsuario> => {
    const response = await axios.put<PreferenciaUsuario>(
      `/preferencias/${idUsuario}`,
      data
    );
    return response.data;
  },
};
