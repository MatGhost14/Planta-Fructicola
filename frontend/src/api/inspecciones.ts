/**
 * Servicio API para inspecciones
 */
import axios from "./axios";
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
} from "../types";

export const inspeccionesApi = {
  /**
   * Listar inspecciones con filtros y paginación
   */
  listar: async (
    filtros: FiltrosInspeccion = {}
  ): Promise<InspeccionesPaginadas> => {
    const response = await axios.get<InspeccionesPaginadas>("/inspecciones", {
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
    const response = await axios.post<InspeccionCreated>("/inspecciones", data);
    return response.data;
  },

  /**
   * Actualizar inspección
   */
  actualizar: async (
    id: number,
    data: InspeccionUpdate
  ): Promise<Inspeccion> => {
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
  subirFotos: async (
    id: number,
    archivos: File[]
  ): Promise<FotoInspeccion[]> => {
    const formData = new FormData();
    archivos.forEach((archivo) => {
      formData.append("archivos", archivo);
    });

    const response = await axios.post<FotoInspeccion[]>(
      `/inspecciones/${id}/fotos`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );
    return response.data;
  },

  /**
   * Eliminar una foto específica
   */
  eliminarFoto: async (
    idInspeccion: number,
    idFoto: number
  ): Promise<ApiMessage> => {
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
    formData.append("archivo", archivo);

    const response = await axios.post<Inspeccion>(
      `/inspecciones/${id}/firma`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );
    return response.data;
  },

  /**
   * Cambiar estado de inspección (aprobar/rechazar)
   */
  cambiarEstado: async (
    id: number,
    estado: "approved" | "rejected",
    comentario?: string
  ): Promise<InspeccionDetalle> => {
    const response = await axios.patch<InspeccionDetalle>(
      `/inspecciones/${id}/estado`,
      { estado, comentario }
    );
    return response.data;
  },

  /**
   * Exportar inspecciones a CSV con filtros
   */
  exportarCSV: async (filtros: FiltrosInspeccion = {}): Promise<void> => {
    const params = new URLSearchParams();

    if (filtros.q) params.append("q", filtros.q);
    if (filtros.planta) params.append("planta", filtros.planta.toString());
    if (filtros.naviera) params.append("naviera", filtros.naviera.toString());
    if (filtros.estado) params.append("estado", filtros.estado);
    if (filtros.fecha_desde) params.append("fecha_desde", filtros.fecha_desde);
    if (filtros.fecha_hasta) params.append("fecha_hasta", filtros.fecha_hasta);
    if (filtros.inspector)
      params.append("inspector", filtros.inspector.toString());
    if (filtros.order_by) params.append("order_by", filtros.order_by);
    if (filtros.order_dir) params.append("order_dir", filtros.order_dir);

    const response = await axios.get(
      `/inspecciones/export/csv?${params.toString()}`,
      {
        responseType: "blob",
      }
    );

    // Intentar usar el nombre de archivo del encabezado Content-Disposition
    let filename = `inspecciones_${new Date().getTime()}.csv`;
    const dispo = response.headers?.["content-disposition"] as
      | string
      | undefined;
    if (dispo) {
      const match = /filename\*=UTF-8''([^;]+)|filename=([^;]+)/i.exec(dispo);
      const raw = match?.[1] || match?.[2];
      if (raw) {
        try {
          // Quitar comillas y decodificar
          const cleaned = raw.replace(/\"/g, "").replace(/^\"|\"$/g, "");
          filename = decodeURIComponent(cleaned);
        } catch {
          filename = raw.replace(/\"/g, "").replace(/^\"|\"$/g, "");
        }
      }
    }

    // Crear enlace de descarga
    const blob = new Blob([response.data], { type: "text/csv;charset=utf-8" });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  },
};
