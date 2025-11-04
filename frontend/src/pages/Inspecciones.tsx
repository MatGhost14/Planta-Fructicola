import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import {
  inspeccionesApi,
  reportesApi,
  plantasApi,
  navierasApi,
  usuariosApi,
} from "../api";
import type {
  Inspeccion,
  InspeccionDetalle,
  FiltrosInspeccion,
  Planta,
  Naviera,
  Usuario,
} from "../types";
import { formatearFecha, claseEstado, textoEstado } from "../utils";
import InspeccionModal from "../components/InspeccionModal";
import { useAuth } from "../contexts/AuthContext";
import { useToast } from "../components/ToastProvider";

const Inspecciones: React.FC = () => {
  const [inspecciones, setInspecciones] = useState<Inspeccion[]>([]);
  const [loading, setLoading] = useState(true);
  const [generandoPdf, setGenerandoPdf] = useState<number | null>(null);
  const [filtros, setFiltros] = useState<FiltrosInspeccion>({});
  const [busqueda, setBusqueda] = useState("");
  const [fechaDesde, setFechaDesde] = useState("");
  const [fechaHasta, setFechaHasta] = useState("");
  const [selectedInspeccion, setSelectedInspeccion] =
    useState<InspeccionDetalle | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const { user } = useAuth();
  const { showSuccess, showError, showInfo } = useToast();

  // Listas para filtros
  const [plantas, setPlantas] = useState<Planta[]>([]);
  const [navieras, setNavieras] = useState<Naviera[]>([]);
  const [inspectores, setInspectores] = useState<Usuario[]>([]);

  useEffect(() => {
    cargarInspecciones();
  }, [filtros]);

  useEffect(() => {
    // Cargar opciones para los selectores (una vez)
    const cargarOpciones = async () => {
      try {
        const [plantasData, navierasData] = await Promise.all([
          plantasApi.listar(),
          navierasApi.listar(),
        ]);
        setPlantas(plantasData);
        setNavieras(navierasData);

        // Cargar inspectores sólo si el rol lo permite (admin/supervisor)
        if (user?.rol === "admin" || user?.rol === "supervisor") {
          const insp = await usuariosApi.listarInspectores(false);
          setInspectores(insp.filter((u) => u.rol === "inspector"));
        } else {
          setInspectores([]);
        }
      } catch (error) {
        console.error("Error al cargar opciones de filtros:", error);
      }
    };
    cargarOpciones();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user?.rol]);

  const cargarInspecciones = async () => {
    try {
      setLoading(true);
      const data = await inspeccionesApi.listar(filtros);
      setInspecciones(data.items);
    } catch (error) {
      console.error("Error al cargar inspecciones:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleVerDetalle = async (inspeccion: Inspeccion) => {
    try {
      // Obtener datos completos de la inspección
      const detalleCompleto = await inspeccionesApi.obtener(
        inspeccion.id_inspeccion
      );
      setSelectedInspeccion(detalleCompleto);
      setModalOpen(true);
    } catch (error) {
      console.error("Error al cargar detalle:", error);
    }
  };

  const handleBuscar = () => {
    setFiltros({
      ...filtros,
      q: busqueda || undefined,
    });
  };

  const handleFiltroEstado = (estado?: string) => {
    // Los chips de estado sobreescriben y reinician el resto
    setBusqueda("");
    setFechaDesde("");
    setFechaHasta("");
    setFiltros(estado ? { estado: estado as any } : {});
  };

  const handleGenerarPdf = async (inspeccion: Inspeccion) => {
    try {
      setGenerandoPdf(inspeccion.id_inspeccion);
      showInfo("Generando PDF, por favor espere...");

      const resultado = await reportesApi.generarPdf({
        id_inspeccion: inspeccion.id_inspeccion,
      });

      showSuccess(resultado.mensaje || "PDF generado exitosamente");

      // Descargar automáticamente
      reportesApi.descargarPdf(resultado.id_reporte);
    } catch (error: any) {
      console.error("Error al generar PDF:", error);
      const mensaje = error.response?.data?.detail || "Error al generar el PDF";
      showError(mensaje);
    } finally {
      setGenerandoPdf(null);
    }
  };

  const aplicarFiltrosAvanzados = () => {
    setFiltros({
      ...filtros,
      fecha_desde: fechaDesde || undefined,
      fecha_hasta: fechaHasta || undefined,
    });
  };

  const limpiarFiltros = () => {
    setFechaDesde("");
    setFechaHasta("");
    setBusqueda("");
    // Mantener estado si está activo; de lo contrario reset total
    setFiltros((prev) => (prev.estado ? { estado: prev.estado } : {}));
  };

  // Verificar si el usuario puede generar PDFs (admin o inspector)
  const puedeGenerarPdf = user?.rol === "admin" || user?.rol === "inspector";

  return (
    <div className="py-2">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-8">
        <h1 className="text-2xl sm:text-3xl font-bold text-gray-800 dark:text-gray-100">
          Inspecciones
        </h1>
        <Link to="/inspeccion-nueva" className="btn-primary">
          <svg
            className="w-5 h-5 mr-2"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 4v16m8-8H4"
            />
          </svg>
          Nueva Inspección
        </Link>
      </div>

      {/* Filtros */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-card p-6 mb-6">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <input
              type="text"
              value={busqueda}
              onChange={(e) => setBusqueda(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && handleBuscar()}
              placeholder="Buscar por número de contenedor..."
              className="input-field"
            />
          </div>
          <button onClick={handleBuscar} className="btn-primary">
            <svg
              className="w-5 h-5 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
            Buscar
          </button>
        </div>

        {/* Filtros avanzados */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mt-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Planta
            </label>
            <select
              value={filtros.planta || ""}
              onChange={(e) =>
                setFiltros({
                  ...filtros,
                  planta: e.target.value ? Number(e.target.value) : undefined,
                })
              }
              className="input-field"
            >
              <option value="">Todas</option>
              {plantas.map((p) => (
                <option key={p.id_planta} value={p.id_planta}>
                  {p.nombre}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Naviera
            </label>
            <select
              value={filtros.naviera || ""}
              onChange={(e) =>
                setFiltros({
                  ...filtros,
                  naviera: e.target.value ? Number(e.target.value) : undefined,
                })
              }
              className="input-field"
            >
              <option value="">Todas</option>
              {navieras.map((n) => (
                <option key={n.id_navieras} value={n.id_navieras}>
                  {n.nombre}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Desde
            </label>
            <input
              type="date"
              value={fechaDesde}
              onChange={(e) => setFechaDesde(e.target.value)}
              className="input-field"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Hasta
            </label>
            <input
              type="date"
              value={fechaHasta}
              onChange={(e) => setFechaHasta(e.target.value)}
              className="input-field"
            />
          </div>
          {(user?.rol === "admin" || user?.rol === "supervisor") && (
            <div className="md:col-span-2 lg:col-span-1">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Inspector
              </label>
              <select
                value={filtros.inspector || ""}
                onChange={(e) =>
                  setFiltros({
                    ...filtros,
                    inspector: e.target.value
                      ? Number(e.target.value)
                      : undefined,
                  })
                }
                className="input-field"
              >
                <option value="">Todos</option>
                {inspectores.map((i) => (
                  <option key={i.id_usuario} value={i.id_usuario}>
                    {i.nombre}
                  </option>
                ))}
              </select>
            </div>
          )}
        </div>

        <div className="flex gap-2 mt-4">
          <button
            onClick={() => handleFiltroEstado(undefined)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              !filtros.estado
                ? "bg-gray-800 text-white"
                : "bg-gray-200 text-gray-700 hover:bg-gray-300"
            }`}
          >
            Todas
          </button>
          <button
            onClick={() => handleFiltroEstado("pending")}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              filtros.estado === "pending"
                ? "bg-yellow-600 text-white"
                : "bg-yellow-100 text-yellow-700 hover:bg-yellow-200"
            }`}
          >
            Pendientes
          </button>
          <button
            onClick={() => handleFiltroEstado("approved")}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              filtros.estado === "approved"
                ? "bg-green-600 text-white"
                : "bg-green-100 text-green-700 hover:bg-green-200"
            }`}
          >
            Aprobadas
          </button>
          <button
            onClick={() => handleFiltroEstado("rejected")}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              filtros.estado === "rejected"
                ? "bg-red-600 text-white"
                : "bg-red-100 text-red-700 hover:bg-red-200"
            }`}
          >
            Rechazadas
          </button>
          <div className="ml-auto flex gap-2">
            <button onClick={aplicarFiltrosAvanzados} className="btn-primary">
              Aplicar filtros
            </button>
            <button
              onClick={limpiarFiltros}
              className="px-4 py-2 bg-gray-200 text-gray-700 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600 rounded-lg hover:bg-gray-300"
            >
              Limpiar
            </button>
          </div>
        </div>
      </div>

      {/* Tabla */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Código
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Contenedor
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Fecha
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Temperatura
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Estado
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Acciones
                </th>
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              {loading ? (
                <tr>
                  <td
                    colSpan={6}
                    className="px-6 py-8 text-center text-gray-500"
                  >
                    Cargando...
                  </td>
                </tr>
              ) : inspecciones.length === 0 ? (
                <tr>
                  <td
                    colSpan={6}
                    className="px-6 py-8 text-center text-gray-500"
                  >
                    No se encontraron inspecciones
                  </td>
                </tr>
              ) : (
                inspecciones.map((inspeccion) => (
                  <tr
                    key={inspeccion.id_inspeccion}
                    className="hover:bg-gray-50 dark:bg-gray-700"
                  >
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-gray-100">
                      {inspeccion.codigo}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100">
                      {inspeccion.numero_contenedor}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {formatearFecha(inspeccion.inspeccionado_en)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {inspeccion.temperatura_c
                        ? `${inspeccion.temperatura_c}°C`
                        : "-"}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${claseEstado(
                          inspeccion.estado
                        )}`}
                      >
                        {textoEstado(inspeccion.estado)}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => handleVerDetalle(inspeccion)}
                          className="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300"
                          title="Ver detalles"
                        >
                          Ver detalles
                        </button>

                        {puedeGenerarPdf && (
                          <>
                            <span className="text-gray-300">|</span>
                            <button
                              onClick={() => handleGenerarPdf(inspeccion)}
                              disabled={
                                generandoPdf === inspeccion.id_inspeccion
                              }
                              className={`flex items-center gap-1 ${
                                generandoPdf === inspeccion.id_inspeccion
                                  ? "text-gray-400 cursor-not-allowed"
                                  : "text-red-600 hover:text-red-900 dark:text-red-400 dark:hover:text-red-300"
                              }`}
                              title="Generar PDF"
                            >
                              {generandoPdf === inspeccion.id_inspeccion ? (
                                <>
                                  <svg
                                    className="animate-spin h-4 w-4"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                  >
                                    <circle
                                      className="opacity-25"
                                      cx="12"
                                      cy="12"
                                      r="10"
                                      stroke="currentColor"
                                      strokeWidth="4"
                                    />
                                    <path
                                      className="opacity-75"
                                      fill="currentColor"
                                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                                    />
                                  </svg>
                                  Generando...
                                </>
                              ) : (
                                <>
                                  <svg
                                    className="w-4 h-4"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                  >
                                    <path
                                      strokeLinecap="round"
                                      strokeLinejoin="round"
                                      strokeWidth={2}
                                      d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"
                                    />
                                  </svg>
                                  PDF
                                </>
                              )}
                            </button>
                          </>
                        )}
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal de detalle */}
      <InspeccionModal
        inspeccion={selectedInspeccion}
        isOpen={modalOpen}
        onClose={() => {
          setModalOpen(false);
          setSelectedInspeccion(null);
        }}
        onUpdate={cargarInspecciones}
      />
    </div>
  );
};

export default Inspecciones;
