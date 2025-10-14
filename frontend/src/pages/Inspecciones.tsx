import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { inspeccionesApi } from '../api';
import type { Inspeccion, FiltrosInspeccion } from '../types';
import { formatearFecha, claseEstado, textoEstado } from '../utils';

const Inspecciones: React.FC = () => {
  const [inspecciones, setInspecciones] = useState<Inspeccion[]>([]);
  const [loading, setLoading] = useState(true);
  const [filtros, setFiltros] = useState<FiltrosInspeccion>({});
  const [busqueda, setBusqueda] = useState('');

  useEffect(() => {
    cargarInspecciones();
  }, [filtros]);

  const cargarInspecciones = async () => {
    try {
      setLoading(true);
      const data = await inspeccionesApi.listar(filtros);
      setInspecciones(data.items);
    } catch (error) {
      console.error('Error al cargar inspecciones:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleBuscar = () => {
    setFiltros({
      ...filtros,
      q: busqueda || undefined
    });
  };

  const handleFiltroEstado = (estado?: string) => {
    setFiltros({
      ...filtros,
      estado: estado as any
    });
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Inspecciones</h1>
        <Link to="/inspeccion-nueva" className="btn-primary">
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          Nueva Inspección
        </Link>
      </div>

      {/* Filtros */}
      <div className="bg-white rounded-lg shadow-card p-6 mb-6">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <input
              type="text"
              value={busqueda}
              onChange={(e) => setBusqueda(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleBuscar()}
              placeholder="Buscar por número de contenedor..."
              className="input-field"
            />
          </div>
          <button onClick={handleBuscar} className="btn-primary">
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            Buscar
          </button>
        </div>

        <div className="flex gap-2 mt-4">
          <button
            onClick={() => handleFiltroEstado(undefined)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              !filtros.estado ? 'bg-gray-800 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Todas
          </button>
          <button
            onClick={() => handleFiltroEstado('pending')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              filtros.estado === 'pending' ? 'bg-yellow-600 text-white' : 'bg-yellow-100 text-yellow-700 hover:bg-yellow-200'
            }`}
          >
            Pendientes
          </button>
          <button
            onClick={() => handleFiltroEstado('approved')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              filtros.estado === 'approved' ? 'bg-green-600 text-white' : 'bg-green-100 text-green-700 hover:bg-green-200'
            }`}
          >
            Aprobadas
          </button>
          <button
            onClick={() => handleFiltroEstado('rejected')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              filtros.estado === 'rejected' ? 'bg-red-600 text-white' : 'bg-red-100 text-red-700 hover:bg-red-200'
            }`}
          >
            Rechazadas
          </button>
        </div>
      </div>

      {/* Tabla */}
      <div className="bg-white rounded-lg shadow-card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Código
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Contenedor
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Fecha
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Temperatura
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Estado
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Acciones
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {loading ? (
                <tr>
                  <td colSpan={6} className="px-6 py-8 text-center text-gray-500">
                    Cargando...
                  </td>
                </tr>
              ) : inspecciones.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-6 py-8 text-center text-gray-500">
                    No se encontraron inspecciones
                  </td>
                </tr>
              ) : (
                inspecciones.map((inspeccion) => (
                  <tr key={inspeccion.id_inspeccion} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {inspeccion.codigo}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {inspeccion.numero_contenedor}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {formatearFecha(inspeccion.inspeccionado_en)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {inspeccion.temperatura_c ? `${inspeccion.temperatura_c}°C` : '-'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${claseEstado(inspeccion.estado)}`}>
                        {textoEstado(inspeccion.estado)}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <button className="text-blue-600 hover:text-blue-900">
                        Ver detalles
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Inspecciones;
