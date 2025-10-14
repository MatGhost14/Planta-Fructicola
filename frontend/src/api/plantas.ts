/**
 * Servicio API para plantas
 */
import axios from './axios';
import type { Planta, PlantaCreate, PlantaUpdate, ApiMessage } from '../types';

export const plantasApi = {
  /**
   * Obtener todas las plantas
   */
  listar: async (): Promise<Planta[]> => {
    const response = await axios.get<Planta[]>('/plantas');
    return response.data;
  },

  /**
   * Crear nueva planta
   */
  crear: async (data: PlantaCreate): Promise<Planta> => {
    const response = await axios.post<Planta>('/plantas', data);
    return response.data;
  },

  /**
   * Actualizar planta
   */
  actualizar: async (id: number, data: PlantaUpdate): Promise<Planta> => {
    const response = await axios.put<Planta>(`/plantas/${id}`, data);
    return response.data;
  },

  /**
   * Eliminar planta
   */
  eliminar: async (id: number): Promise<ApiMessage> => {
    const response = await axios.delete<ApiMessage>(`/plantas/${id}`);
    return response.data;
  },
};
