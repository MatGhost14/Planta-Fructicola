/**
 * Utilidades generales
 */
import { format } from 'date-fns';
import { es } from 'date-fns/locale';

/**
 * Formatea fecha con formato español
 */
export const formatearFecha = (fecha: string | Date, formato = 'dd/MM/yyyy HH:mm'): string => {
  try {
    const date = typeof fecha === 'string' ? new Date(fecha) : fecha;
    return format(date, formato, { locale: es });
  } catch {
    return '-';
  }
};

/**
 * Obtiene clase CSS para badge de estado
 */
export const claseEstado = (estado: string): string => {
  const clases = {
    pending: 'bg-orange-100 text-orange-800',
    approved: 'bg-green-100 text-green-800',
    rejected: 'bg-red-100 text-red-800',
  };
  return clases[estado as keyof typeof clases] || 'bg-gray-100 text-gray-800';
};

/**
 * Obtiene texto legible para estado
 */
export const textoEstado = (estado: string): string => {
  const textos = {
    pending: 'Pendiente',
    approved: 'Aprobada',
    rejected: 'Rechazada',
  };
  return textos[estado as keyof typeof textos] || estado;
};

/**
 * Obtiene clase CSS para badge de rol
 */
export const claseRol = (rol: string): string => {
  const clases = {
    inspector: 'bg-blue-100 text-blue-800',
    supervisor: 'bg-purple-100 text-purple-800',
    admin: 'bg-red-100 text-red-800',
  };
  return clases[rol as keyof typeof clases] || 'bg-gray-100 text-gray-800';
};

/**
 * Obtiene texto legible para rol
 */
export const textoRol = (rol: string): string => {
  const textos = {
    inspector: 'Inspector',
    supervisor: 'Supervisor',
    admin: 'Administrador',
  };
  return textos[rol as keyof typeof textos] || rol;
};

/**
 * Obtiene nombre de planta por código
 */
export const nombrePlanta = (codigo: string): string => {
  const nombres = {
    norte: 'Planta Norte',
    sur: 'Planta Sur',
    este: 'Planta Este',
    oeste: 'Planta Oeste',
  };
  return nombres[codigo as keyof typeof nombres] || codigo;
};

/**
 * Convierte DataURL a Blob
 */
export const dataURLtoBlob = (dataURL: string): Blob => {
  const arr = dataURL.split(',');
  const mime = arr[0].match(/:(.*?);/)?.[1] || 'image/jpeg';
  const bstr = atob(arr[1]);
  let n = bstr.length;
  const u8arr = new Uint8Array(n);
  while (n--) {
    u8arr[n] = bstr.charCodeAt(n);
  }
  return new Blob([u8arr], { type: mime });
};

/**
 * Convierte Blob a File
 */
export const blobToFile = (blob: Blob, fileName: string): File => {
  return new File([blob], fileName, { type: blob.type });
};

/**
 * Genera CSV de inspecciones
 */
export const generarCSV = (data: any[]): string => {
  const headers = ['Contenedor', 'Planta', 'Naviera', 'Temperatura', 'Inspector', 'Estado', 'Fecha'];
  const filas = data.map((i) => [
    i.numero_contenedor,
    i.planta?.nombre || '-',
    i.naviera?.nombre || '-',
    i.temperatura_c || '-',
    i.inspector?.nombre || '-',
    textoEstado(i.estado),
    formatearFecha(i.inspeccionado_en),
  ]);

  return [headers, ...filas]
    .map((fila) =>
      fila.map((campo) => `"${String(campo).replace(/"/g, '""')}"`).join(',')
    )
    .join('\n');
};

/**
 * Descarga archivo
 */
export const descargarArchivo = (contenido: string, nombre: string, tipo: string): void => {
  const blob = new Blob([contenido], { type: tipo });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = nombre;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
};
