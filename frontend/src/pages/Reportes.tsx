import React, { useState, useEffect } from 'react';
import { reportesApi } from '../api';
import type { ConteoEstado, ResumenReporte } from '../types';
import { textoEstado } from '../utils';

const Reportes: React.FC = () => {
  const [resumen, setResumen] = useState<ResumenReporte | null>(null);
  const [conteo, setConteo] = useState<ConteoEstado[]>([]);
  const [loading, setLoading] = useState(true);
  const [fechaDesde, setFechaDesde] = useState('');
  const [fechaHasta, setFechaHasta] = useState('');

  useEffect(() => {
    cargarDatos();
  }, []);

  const cargarDatos = async () => {
    try {
      setLoading(true);
      
      const [resumenData, conteoData] = await Promise.all([
        reportesApi.resumen(fechaDesde || undefined, fechaHasta || undefined),
        reportesApi.conteoEstado()
      ]);
      
      setResumen(resumenData);
      setConteo(conteoData);
    } catch (error) {
      console.error('Error al cargar reportes:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFiltrar = () => {
    cargarDatos();
  };

  const calcularPorcentaje = (valor: number, total: number): number => {
    return total > 0 ? Math.round((valor / total) * 100) : 0;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Cargando...</div>
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Reportes y Estadísticas</h1>

      {/* Filtros de Fecha */}
      <div className="bg-white rounded-lg shadow-card p-6 mb-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">Filtros</h2>
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Desde
            </label>
            <input
              type="date"
              value={fechaDesde}
              onChange={(e) => setFechaDesde(e.target.value)}
              className="input-field"
            />
          </div>
          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Hasta
            </label>
            <input
              type="date"
              value={fechaHasta}
              onChange={(e) => setFechaHasta(e.target.value)}
              className="input-field"
            />
          </div>
          <div className="flex items-end">
            <button onClick={handleFiltrar} className="btn-primary">
              Aplicar Filtros
            </button>
          </div>
        </div>
      </div>

      {/* Resumen General */}
      {resumen && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-card p-6">
            <h3 className="text-sm font-medium text-gray-500 mb-2">Total Inspecciones</h3>
            <p className="text-3xl font-bold text-gray-800">{resumen.total_inspecciones}</p>
          </div>
          <div className="bg-white rounded-lg shadow-card p-6">
            <h3 className="text-sm font-medium text-gray-500 mb-2">Aprobadas</h3>
            <p className="text-3xl font-bold text-green-600">{resumen.aprobadas}</p>
            <p className="text-sm text-gray-500 mt-1">
              {calcularPorcentaje(resumen.aprobadas, resumen.total_inspecciones)}%
            </p>
          </div>
          <div className="bg-white rounded-lg shadow-card p-6">
            <h3 className="text-sm font-medium text-gray-500 mb-2">Pendientes</h3>
            <p className="text-3xl font-bold text-yellow-600">{resumen.pendientes}</p>
            <p className="text-sm text-gray-500 mt-1">
              {calcularPorcentaje(resumen.pendientes, resumen.total_inspecciones)}%
            </p>
          </div>
          <div className="bg-white rounded-lg shadow-card p-6">
            <h3 className="text-sm font-medium text-gray-500 mb-2">Rechazadas</h3>
            <p className="text-3xl font-bold text-red-600">{resumen.rechazadas}</p>
            <p className="text-sm text-gray-500 mt-1">
              {calcularPorcentaje(resumen.rechazadas, resumen.total_inspecciones)}%
            </p>
          </div>
        </div>
      )}

      {/* Gráfico de Barras */}
      <div className="bg-white rounded-lg shadow-card p-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-6">Distribución por Estado</h2>
        <div className="space-y-4">
          {conteo.map((item) => {
            const total = conteo.reduce((sum, c) => sum + c.total, 0);
            const porcentaje = calcularPorcentaje(item.total, total);
            
            return (
              <div key={item.estado}>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-700">
                    {textoEstado(item.estado)}
                  </span>
                  <span className="text-sm text-gray-500">
                    {item.total} ({porcentaje}%)
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div
                    className={`h-3 rounded-full ${
                      item.estado === 'approved' ? 'bg-green-600' :
                      item.estado === 'pending' ? 'bg-yellow-600' :
                      'bg-red-600'
                    }`}
                    style={{ width: `${porcentaje}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default Reportes;
