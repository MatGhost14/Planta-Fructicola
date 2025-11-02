/**
 * Servicio API para reportes
 */
import axios from './axios';
import type { ConteoEstado, ResumenReporte } from '../types';

// ===== Tipos para PDF =====

export interface ReporteCreate {
  id_inspeccion: number;
}

export interface Reporte {
  id_reporte: number;
  uuid_reporte: string;
  id_inspeccion: number;
  pdf_ruta: string;
  hash_global: string | null;
  creado_en: string;
}

export interface ReporteCreated {
  id_reporte: number;
  uuid_reporte: string;
  pdf_ruta: string;
  mensaje: string;
}

// ===== API de Reportes =====

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
  resumen: async (
    desde?: string, 
    hasta?: string,
    idPlanta?: number,
    idNavieras?: number,
    idInspector?: number
  ): Promise<ResumenReporte> => {
    const response = await axios.get<ResumenReporte>('/reportes/resumen', {
      params: { 
        desde, 
        hasta,
        id_planta: idPlanta,
        id_navieras: idNavieras,
        id_inspector: idInspector
      },
    });
    return response.data;
  },

  // ===== PDF =====

  /**
   * Generar PDF de inspección (solo ADMIN)
   */
  generarPdf: async (data: ReporteCreate): Promise<ReporteCreated> => {
    const response = await axios.post<ReporteCreated>('/reportes/pdf/generar', data);
    return response.data;
  },

  /**
   * Obtener información de un reporte
   */
  obtenerReporte: async (idReporte: number): Promise<Reporte> => {
    const response = await axios.get<Reporte>(`/reportes/pdf/${idReporte}`);
    return response.data;
  },

  /**
   * Descargar PDF
   */
  descargarPdf: async (idReporte: number): Promise<void> => {
    try {
      // Usar la instancia Axios (agrega Authorization automáticamente desde 'auth_token')
      const response = await axios.get(`/reportes/pdf/${idReporte}/descargar`, {
        responseType: 'blob',
      });

      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `reporte_${idReporte}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error al descargar PDF:', error);
      throw error;
    }
  },

  /**
   * Listar reportes de una inspección
   */
  listarReportesInspeccion: async (idInspeccion: number): Promise<Reporte[]> => {
    const response = await axios.get<Reporte[]>(`/reportes/inspeccion/${idInspeccion}/pdfs`);
    return response.data;
  },
};

