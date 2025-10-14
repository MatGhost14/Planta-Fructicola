/**
 * Servicio API para inspecciones
 */
import axios from './axios';
import type {
  Inspeccion,
  InspeccionDetalle,
  InspeccionCreate,
  InspeccionUpdate,
  InspeccionCreated,
  InspeccionesPaginadas,
  FiltrosInspeccion,
  FotoInspeccion,
  ApiMessage,
} from '../types';

export const inspeccionesApi = {
  /**
   * Listar inspecciones con filtros y paginación
   */
  listar: async (filtros: FiltrosInspeccion = {}): Promise<InspeccionesPaginadas> => {
    const response = await axios.get<InspeccionesPaginadas>('/inspecciones', {
      params: filtros,
    });
    return response.data;
  },

  /**
   * Obtener detalle de una inspección
   */
  obtener: async (id: number): Promise<InspeccionDetalle> => {
    const response = await axios.get<InspeccionDetalle>(`/inspecciones/${id}`);
    return response.data;
  },

  /**
   * Crear nueva inspección (sin fotos)
   */
  crear: async (data: InspeccionCreate): Promise<InspeccionCreated> => {
    const response = await axios.post<InspeccionCreated>('/inspecciones', data);
    return response.data;
  },

  /**
   * Actualizar inspección
   */
  actualizar: async (id: number, data: InspeccionUpdate): Promise<Inspeccion> => {
    const response = await axios.put<Inspeccion>(`/inspecciones/${id}`, data);
    return response.data;
  },

  /**
   * Eliminar inspección
   */
  eliminar: async (id: number): Promise<ApiMessage> => {
    const response = await axios.delete<ApiMessage>(`/inspecciones/${id}`);
    return response.data;
  },

  /**
   * Subir fotos para una inspección
   */
  subirFotos: async (id: number, archivos: File[]): Promise<FotoInspeccion[]> => {
    const formData = new FormData();
    archivos.forEach((archivo) => {
      formData.append('archivos', archivo);
    });

    const response = await axios.post<FotoInspeccion[]>(
      `/inspecciones/${id}/fotos`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  },

  /**
   * Eliminar una foto específica
   */
  eliminarFoto: async (idInspeccion: number, idFoto: number): Promise<ApiMessage> => {
    const response = await axios.delete<ApiMessage>(
      `/inspecciones/${idInspeccion}/fotos/${idFoto}`
    );
    return response.data;
  },

  /**
   * Subir firma digital
   */
  subirFirma: async (id: number, archivo: File): Promise<Inspeccion> => {
    const formData = new FormData();
    formData.append('archivo', archivo);

    const response = await axios.post<Inspeccion>(
      `/inspecciones/${id}/firma`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  },
};
