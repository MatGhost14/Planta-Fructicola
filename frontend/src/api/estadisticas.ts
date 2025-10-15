import axios from './axios';

interface EstadisticasGeneral {
  total_inspecciones: number;
  total_aprobadas: number;
  total_rechazadas: number;
  total_pendientes: number;
  promedio_tiempo_respuesta?: number;
}

interface InspeccionPorEstado {
  estado: string;
  total: number;
  porcentaje: number;
}

interface InspeccionPorFecha {
  fecha: string;
  total: number;
}

interface InspeccionPorPlanta {
  nombre_planta: string;
  total: number;
}

interface InspeccionPorInspector {
  nombre_completo: string;
  total_inspeccionadas: number;
  aprobadas: number;
  rechazadas: number;
  pendientes: number;
}

export interface DashboardData {
  fecha_desde: string;
  fecha_hasta: string;
  estadisticas_generales: EstadisticasGeneral;
  por_estado: InspeccionPorEstado[];
  por_fecha: InspeccionPorFecha[];
  por_planta: InspeccionPorPlanta[];
  por_inspector: InspeccionPorInspector[];
}

export const estadisticasApi = {
  async getDashboard(params?: {
    fecha_desde?: string;
    fecha_hasta?: string;
  }): Promise<DashboardData> {
    const response = await axios.get('/estadisticas/dashboard', { params });
    return response.data;
  }
};
