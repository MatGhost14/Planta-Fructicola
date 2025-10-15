import React, { useState, useEffect } from 'react';
import { reportesApi, axios } from '../api';
import { useToast } from '../components/ToastProvider';
import type { ConteoEstado, ResumenReporte } from '../types';
import { textoEstado } from '../utils';

const Reportes: React.FC = () => {
  const { showError, showSuccess } = useToast();
  const [resumen, setResumen] = useState<ResumenReporte | null>(null);
  const [conteo, setConteo] = useState<ConteoEstado[]>([]);
  const [loading, setLoading] = useState(true);
  const [fechaDesde, setFechaDesde] = useState('');
  const [fechaHasta, setFechaHasta] = useState('');
  const [exportando, setExportando] = useState(false);

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

  const exportarPDF = async () => {
    try {
      setExportando(true);
      
      const params = new URLSearchParams();
      if (fechaDesde) params.append('fecha_desde', fechaDesde);
      if (fechaHasta) params.append('fecha_hasta', fechaHasta);
      
      const response = await axios.get(`/reportes/export/pdf?${params.toString()}`, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `reporte_inspecciones_${new Date().getTime()}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      showSuccess('Reporte PDF generado exitosamente');
    } catch (error) {
      console.error('Error al exportar PDF:', error);
      showError('Error al generar el reporte PDF');
    } finally {
      setExportando(false);
    }
  };

  const exportarExcel = async () => {
    try {
      setExportando(true);
      
      const params = new URLSearchParams();
      if (fechaDesde) params.append('fecha_desde', fechaDesde);
      if (fechaHasta) params.append('fecha_hasta', fechaHasta);
      
      const response = await axios.get(`/reportes/export/excel?${params.toString()}`, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `reporte_inspecciones_${new Date().getTime()}.xlsx`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      showSuccess('Reporte Excel generado exitosamente');
    } catch (error) {
      console.error('Error al exportar Excel:', error);
      showError('Error al generar el reporte Excel');
    } finally {
      setExportando(false);
    }
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
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Reportes y Estadísticas</h1>
        
        {/* Botones de exportación */}
        <div className="flex gap-3">
          <button
            onClick={exportarPDF}
            disabled={exportando}
            className="flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
            </svg>
            {exportando ? 'Generando...' : 'Exportar PDF'}
          </button>
          
          <button
            onClick={exportarExcel}
            disabled={exportando}
            className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            {exportando ? 'Generando...' : 'Exportar Excel'}
          </button>
        </div>
      </div>

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
          <div className="flex items-end gap-3">
            <button onClick={handleFiltrar} className="btn-primary">
              Aplicar Filtros
            </button>
            <button 
              onClick={() => {
                setFechaDesde('');
                setFechaHasta('');
                setTimeout(cargarDatos, 100);
              }} 
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
            >
              Limpiar
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

      {/* Información de ayuda */}
      <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-start gap-3">
          <svg className="w-5 h-5 text-blue-600 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
          </svg>
          <div className="text-sm text-blue-800">
            <p className="font-semibold mb-1">Acerca de los reportes:</p>
            <ul className="list-disc list-inside space-y-1">
              <li>Los reportes incluyen todas las inspecciones según tu rol (Inspector, Supervisor o Admin)</li>
              <li>Los filtros de fecha son opcionales - si no los usas, se incluyen todas las inspecciones</li>
              <li>El PDF incluye resumen estadístico y tabla detallada (máximo 100 registros)</li>
              <li>El Excel incluye dos hojas: "Resumen" y "Detalle" (máximo 5000 registros)</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Reportes;
