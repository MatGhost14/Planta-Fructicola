/**
 * Tipos TypeScript para el sistema de inspecciones
 * Alineados con schemas Pydantic del backend
 */

export type RolUsuario = "inspector" | "supervisor" | "admin";
export type EstadoUsuario = "active" | "inactive";
export type EstadoInspeccion = "pending" | "approved" | "rejected";

// ===== USUARIOS =====

export interface Usuario {
  id_usuario: number;
  nombre: string;
  correo: string;
  rol: RolUsuario;
  estado: EstadoUsuario;
  ultimo_acceso?: string;
  creado_en: string;
  actualizado_en: string;
}

export interface UsuarioCreate {
  nombre: string;
  correo: string;
  rol?: RolUsuario;
  password?: string;
}

export interface UsuarioUpdate {
  nombre?: string;
  correo?: string;
  rol?: RolUsuario;
  password?: string;
}

// ===== PLANTAS =====

export interface Planta {
  id_planta: number;
  codigo: string;
  nombre: string;
  ubicacion?: string;
  creado_en: string;
  actualizado_en: string;
}

export interface PlantaCreate {
  codigo: string;
  nombre: string;
  ubicacion?: string;
}

export interface PlantaUpdate {
  codigo?: string;
  nombre?: string;
  ubicacion?: string;
}

// ===== NAVIERAS =====

export interface Naviera {
  id_navieras: number;
  codigo: string;
  nombre: string;
  creado_en: string;
  actualizado_en: string;
}

export interface NavieraCreate {
  codigo: string;
  nombre: string;
}

export interface NavieraUpdate {
  codigo?: string;
  nombre?: string;
}

// ===== FOTOS =====

export interface FotoInspeccion {
  id_foto: number;
  id_inspeccion: number;
  foto_path: string;
  mime_type: string;
  hash_hex?: string;
  orden: number;
  tomada_en?: string;
  creado_en: string;
}

// ===== INSPECCIONES =====

export interface Inspeccion {
  id_inspeccion: number;
  codigo: string;
  numero_contenedor: string;
  id_planta: number;
  id_navieras: number;
  temperatura_c?: number;
  observaciones?: string;
  firma_path?: string;
  id_inspector: number;
  estado: EstadoInspeccion;
  inspeccionado_en: string;
  creado_en: string;
  actualizado_en: string;
}

export interface InspeccionDetalle extends Inspeccion {
  planta: Planta;
  naviera: Naviera;
  inspector: Usuario;
  fotos: FotoInspeccion[];
}

export interface InspeccionCreate {
  numero_contenedor: string;
  id_planta: number;
  id_navieras: number;
  temperatura_c?: number;
  observaciones?: string;
  id_inspector: number;
  inspeccionado_en?: string;
}

export interface InspeccionUpdate {
  numero_contenedor?: string;
  id_planta?: number;
  id_navieras?: number;
  temperatura_c?: number;
  observaciones?: string;
  estado?: EstadoInspeccion;
}

export interface InspeccionCreated {
  id_inspeccion: number;
  codigo: string;
  mensaje: string;
}

// ===== PREFERENCIAS =====

export interface PreferenciaUsuario {
  id_usuario: number;
  auto_sync: boolean;
  notificaciones: boolean;
  geolocalizacion: boolean;
  actualizado_en: string;
}

export interface PreferenciaUsuarioUpdate {
  auto_sync?: boolean;
  notificaciones?: boolean;
  geolocalizacion?: boolean;
}

// ===== REPORTES =====

export interface ConteoEstado {
  estado: EstadoInspeccion;
  total: number;
}

export interface ResumenReporte {
  total_inspecciones: number;
  aprobadas: number;
  pendientes: number;
  rechazadas: number;
  tasa_aprobacion: number;
  periodo_desde?: string;
  periodo_hasta?: string;
}

// ===== PAGINACIÓN =====

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface InspeccionesPaginadas extends PaginatedResponse<Inspeccion> {}

// ===== FILTROS =====

export interface FiltrosInspeccion {
  q?: string;
  planta?: number;
  naviera?: number;
  estado?: EstadoInspeccion;
  fecha_desde?: string;
  fecha_hasta?: string;
  inspector?: number;
  order_by?: string;
  order_dir?: "asc" | "desc";
  page?: number;
  page_size?: number;
}

// ===== MENSAJES Y ERRORES =====

export interface ApiMessage {
  mensaje: string;
}

export interface ApiError {
  detail: string;
}

// ===== TIPOS LOCALES (Frontend) =====

export interface FotoCapturada {
  id: string;
  data: string; // Data URL
  timestamp: string;
}
