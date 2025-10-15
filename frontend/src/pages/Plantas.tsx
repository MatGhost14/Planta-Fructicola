/**
 * Página de gestión de plantas
 * Accesible para Supervisor y Admin
 */
import React, { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, MapPin, Building } from 'lucide-react';
import axios from '../api/axios';
import { useToast } from '../components/ToastProvider';
import type { Planta, PlantaCreate, PlantaUpdate } from '../types';

const Plantas: React.FC = () => {
  const { showSuccess, showError, confirm } = useToast();
  const [plantas, setPlantas] = useState<Planta[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingPlanta, setEditingPlanta] = useState<Planta | null>(null);
  const [formData, setFormData] = useState<PlantaCreate>({
    codigo: '',
    nombre: '',
    ubicacion: '',
  });

  useEffect(() => {
    cargarPlantas();
  }, []);

  const cargarPlantas = async () => {
    try {
      setLoading(true);
      const response = await axios.get<Planta[]>('/plantas');
      setPlantas(response.data);
    } catch (error: any) {
      console.error('Error al cargar plantas:', error);
      showError(error.response?.data?.detail || 'Error al cargar plantas');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingPlanta) {
        const updateData: PlantaUpdate = formData;
        await axios.put(`/plantas/${editingPlanta.id_planta}`, updateData);
        showSuccess('Planta actualizada exitosamente');
      } else {
        await axios.post('/plantas', formData);
        showSuccess('Planta creada exitosamente');
      }
      setShowModal(false);
      resetForm();
      cargarPlantas();
    } catch (error: any) {
      showError(error.response?.data?.detail || 'Error al guardar planta');
    }
  };

  const handleEdit = (planta: Planta) => {
    setEditingPlanta(planta);
    setFormData({
      codigo: planta.codigo,
      nombre: planta.nombre,
      ubicacion: planta.ubicacion || '',
    });
    setShowModal(true);
  };

  const handleDelete = async (id: number, nombre: string) => {
    const confirmed = await confirm(`¿Está seguro que desea eliminar la planta "${nombre}"?`);
    if (!confirmed) return;
    try {
      await axios.delete(`/plantas/${id}`);
      showSuccess('Planta eliminada exitosamente');
      cargarPlantas();
    } catch (error: any) {
      showError(error.response?.data?.detail || 'Error al eliminar planta');
    }
  };

  const resetForm = () => {
    setEditingPlanta(null);
    setFormData({
      codigo: '',
      nombre: '',
      ubicacion: '',
    });
  };

  return (
    <div className="py-2">
      {/* Header */}
      <div className="mb-8">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">Gestión de Plantas</h1>
            <p className="text-sm sm:text-base text-gray-600 mt-2">Administrar ubicaciones de inspección</p>
          </div>
          <button
            onClick={() => {
              resetForm();
              setShowModal(true);
            }}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Plus className="w-5 h-5" />
            Nueva Planta
          </button>
        </div>
      </div>

      {/* Tabla */}
      {loading ? (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <p className="text-gray-600 mt-4">Cargando plantas...</p>
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Código
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Nombre
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Ubicación
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Creada
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Acciones
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {plantas.map((planta) => (
                <tr key={planta.id_planta} className="hover:bg-gray-50 dark:bg-gray-700">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 h-10 w-10 bg-blue-100 rounded-full flex items-center justify-center">
                        <Building className="w-5 h-5 text-blue-600" />
                      </div>
                      <div className="ml-4">
                        <div className="text-sm font-medium text-gray-900">{planta.codigo}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">{planta.nombre}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center text-sm text-gray-500">
                      <MapPin className="w-4 h-4 mr-1" />
                      {planta.ubicacion || 'No especificada'}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(planta.creado_en).toLocaleDateString('es-ES')}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button
                      onClick={() => handleEdit(planta)}
                      className="text-blue-600 hover:text-blue-900 mr-4"
                      title="Editar"
                    >
                      <Edit className="w-5 h-5" />
                    </button>
                    <button
                      onClick={() => handleDelete(planta.id_planta, planta.nombre)}
                      className="text-red-600 hover:text-red-900"
                      title="Eliminar"
                    >
                      <Trash2 className="w-5 h-5" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Modal de formulario */}
      {showModal && (
        <>
          <div className="fixed inset-0 bg-black bg-opacity-50 z-40" onClick={() => setShowModal(false)} />
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">
                {editingPlanta ? 'Editar Planta' : 'Nueva Planta'}
              </h3>
              <form onSubmit={handleSubmit}>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Código *
                    </label>
                    <input
                      type="text"
                      value={formData.codigo}
                      onChange={(e) => setFormData({ ...formData, codigo: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      required
                      maxLength={50}
                      placeholder="Ej: PLT-01"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Nombre *
                    </label>
                    <input
                      type="text"
                      value={formData.nombre}
                      onChange={(e) => setFormData({ ...formData, nombre: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      required
                      maxLength={120}
                      placeholder="Ej: Planta Central"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Ubicación
                    </label>
                    <input
                      type="text"
                      value={formData.ubicacion}
                      onChange={(e) => setFormData({ ...formData, ubicacion: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      maxLength={191}
                      placeholder="Ej: Valparaíso, Chile"
                    />
                  </div>
                </div>
                <div className="flex justify-end gap-3 mt-6">
                  <button
                    type="button"
                    onClick={() => {
                      setShowModal(false);
                      resetForm();
                    }}
                    className="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                  >
                    Cancelar
                  </button>
                  <button
                    type="submit"
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    {editingPlanta ? 'Actualizar' : 'Crear Planta'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default Plantas;
