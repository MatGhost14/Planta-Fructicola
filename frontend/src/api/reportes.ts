/**
 * Servicio API para reportes
 */
import axios from './axios';
import type { ConteoEstado, ResumenReporte } from '../types';

export const reportesApi = {
  /**
   * Obtener conteo de inspecciones por estado
   */
  conteoEstado: async (): Promise<ConteoEstado[]> => {
    const response = await axios.get<ConteoEstado[]>('/reportes/conteo-estado');
    return response.data;
  },

  /**
   * Obtener resumen de inspecciones
   */
  resumen: async (desde?: string, hasta?: string): Promise<ResumenReporte> => {
    const response = await axios.get<ResumenReporte>('/reportes/resumen', {
      params: { desde, hasta },
    });
    return response.data;
  },
};
