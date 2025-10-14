/**
 * Servicio API para navieras
 */
import axios from './axios';
import type { Naviera, NavieraCreate, NavieraUpdate, ApiMessage } from '../types';

export const navierasApi = {
  /**
   * Obtener todas las navieras
   */
  listar: async (): Promise<Naviera[]> => {
    const response = await axios.get<Naviera[]>('/navieras');
    return response.data;
  },

  /**
   * Crear nueva naviera
   */
  crear: async (data: NavieraCreate): Promise<Naviera> => {
    const response = await axios.post<Naviera>('/navieras', data);
    return response.data;
  },

  /**
   * Actualizar naviera
   */
  actualizar: async (id: number, data: NavieraUpdate): Promise<Naviera> => {
    const response = await axios.put<Naviera>(`/navieras/${id}`, data);
    return response.data;
  },

  /**
   * Eliminar naviera
   */
  eliminar: async (id: number): Promise<ApiMessage> => {
    const response = await axios.delete<ApiMessage>(`/navieras/${id}`);
    return response.data;
  },
};
