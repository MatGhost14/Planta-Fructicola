import axios from './axios';

interface EstadisticasGeneral {
  total_inspecciones: number;
  pendientes: number;
  aprobadas: number;
  rechazadas: number;
  total_usuarios: number;
  total_plantas: number;
  total_navieras: number;
}

interface InspeccionPorEstado {
  estado: string;
  cantidad: number;
  porcentaje: number;
}

interface InspeccionPorFecha {
  fecha: string;
  cantidad: number;
}

interface InspeccionPorPlanta {
  planta: string;
  cantidad: number;
}

interface InspeccionPorInspector {
  inspector: string;
  total: number;
  pendientes: number;
  aprobadas: number;
  rechazadas: number;
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
