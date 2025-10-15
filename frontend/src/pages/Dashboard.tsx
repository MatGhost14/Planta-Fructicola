import React, { useEffect, useState } from 'react';
import { estadisticasApi, type DashboardData } from '../api';
import {
  PieChart, Pie, Cell, LineChart, Line, BarChart, Bar,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

const COLORS = ['#10b981', '#ef4444', '#f59e0b', '#3b82f6'];

const Dashboard: React.FC = () => {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [fechaDesde, setFechaDesde] = useState('');
  const [fechaHasta, setFechaHasta] = useState('');

  useEffect(() => {
    cargarDatos();
  }, []);

  const cargarDatos = async () => {
    try {
      setLoading(true);
      const params: any = {};
      if (fechaDesde) params.fecha_desde = fechaDesde;
      if (fechaHasta) params.fecha_hasta = fechaHasta;
      
      const data = await estadisticasApi.getDashboard(params);
      setDashboardData(data);
    } catch (error) {
      console.error('Error al cargar datos del dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFiltrar = (e: React.FormEvent) => {
    e.preventDefault();
    cargarDatos();
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Cargando dashboard...</div>
      </div>
    );
  }

  if (!dashboardData) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-red-500">Error al cargar datos del dashboard</div>
      </div>
    );
  }

  const { estadisticas_generales, por_estado, por_fecha, por_planta, por_inspector } = dashboardData;

  // Datos para gráfico de pastel (distribución por estado)
  const pieData = por_estado.map(item => ({
    name: item.estado === 'approved' ? 'Aprobadas' : 
          item.estado === 'rejected' ? 'Rechazadas' : 'Pendientes',
    value: item.total,
    porcentaje: item.porcentaje
  }));

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Dashboard Estadísticas</h1>
        
        {/* Filtros de fecha */}
        <form onSubmit={handleFiltrar} className="flex gap-3">
          <input
            type="date"
            value={fechaDesde}
            onChange={(e) => setFechaDesde(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg text-sm"
            placeholder="Desde"
          />
          <input
            type="date"
            value={fechaHasta}
            onChange={(e) => setFechaHasta(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg text-sm"
            placeholder="Hasta"
          />
          <button
            type="submit"
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-medium"
          >
            Filtrar
          </button>
          <button
            type="button"
            onClick={() => {
              setFechaDesde('');
              setFechaHasta('');
              setTimeout(cargarDatos, 100);
            }}
            className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 text-sm font-medium"
          >
            Limpiar
          </button>
        </form>
      </div>

      {/* Rango de fechas actual */}
      <div className="mb-6 text-sm text-gray-600">
        Período: {dashboardData.fecha_desde} a {dashboardData.fecha_hasta}
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow-card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Total Inspecciones</p>
              <p className="text-3xl font-bold text-gray-800">{estadisticas_generales.total_inspecciones}</p>
            </div>
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Pendientes</p>
              <p className="text-3xl font-bold text-yellow-600">{estadisticas_generales.total_pendientes}</p>
            </div>
            <div className="w-12 h-12 bg-yellow-100 rounded-full flex items-center justify-center">
              <svg className="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Aprobadas</p>
              <p className="text-3xl font-bold text-green-600">{estadisticas_generales.total_aprobadas}</p>
            </div>
            <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
              <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Rechazadas</p>
              <p className="text-3xl font-bold text-red-600">{estadisticas_generales.total_rechazadas}</p>
            </div>
            <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
              <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      {/* Gráficos */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Gráfico de Pastel - Distribución por Estado */}
        <div className="bg-white rounded-lg shadow-card p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Distribución por Estado</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, porcentaje }) => `${name}: ${porcentaje.toFixed(1)}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Gráfico de Línea - Tendencia en el Tiempo */}
        <div className="bg-white rounded-lg shadow-card p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Tendencia Temporal</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={por_fecha}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="fecha" 
                tick={{ fontSize: 12 }}
                angle={-45}
                textAnchor="end"
                height={80}
              />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="total" 
                stroke="#3b82f6" 
                strokeWidth={2}
                name="Inspecciones"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Gráfico de Barras - Top 10 Plantas */}
      <div className="bg-white rounded-lg shadow-card p-6 mb-8">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Top 10 Plantas por Volumen</h2>
        <ResponsiveContainer width="100%" height={350}>
          <BarChart data={por_planta}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="nombre_planta" 
              tick={{ fontSize: 12 }}
              angle={-45}
              textAnchor="end"
              height={120}
            />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="total" fill="#10b981" name="Inspecciones" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Tabla de Performance por Inspector */}
      <div className="bg-white rounded-lg shadow-card">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-800">Performance por Inspector</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Inspector
                </th>
                <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Total
                </th>
                <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Aprobadas
                </th>
                <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Rechazadas
                </th>
                <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Pendientes
                </th>
                <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Tasa Aprobación
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {por_inspector.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-6 py-8 text-center text-gray-500">
                    No hay datos de inspectores en este período
                  </td>
                </tr>
              ) : (
                por_inspector.map((inspector, index) => {
                  const tasaAprobacion = inspector.total_inspeccionadas > 0
                    ? (inspector.aprobadas / inspector.total_inspeccionadas * 100).toFixed(1)
                    : '0.0';
                  
                  return (
                    <tr key={index} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {inspector.nombre_completo}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-center text-gray-900">
                        {inspector.total_inspeccionadas}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-center">
                        <span className="text-green-600 font-semibold">{inspector.aprobadas}</span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-center">
                        <span className="text-red-600 font-semibold">{inspector.rechazadas}</span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-center">
                        <span className="text-yellow-600 font-semibold">{inspector.pendientes}</span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-center font-semibold text-blue-600">
                        {tasaAprobacion}%
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
