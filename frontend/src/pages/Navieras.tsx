/**
 * Página de gestión de navieras
 * Accesible para Supervisor y Admin
 */
import React, { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, Ship, Anchor } from 'lucide-react';
import axios from '../api/axios';
import type { Naviera, NavieraCreate, NavieraUpdate } from '../types';

const Navieras: React.FC = () => {
  const [navieras, setNavieras] = useState<Naviera[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingNaviera, setEditingNaviera] = useState<Naviera | null>(null);
  const [formData, setFormData] = useState<NavieraCreate>({
    codigo: '',
    nombre: '',
  });

  useEffect(() => {
    cargarNavieras();
  }, []);

  const cargarNavieras = async () => {
    try {
      setLoading(true);
      const response = await axios.get<Naviera[]>('/navieras');
      setNavieras(response.data);
    } catch (error: any) {
      console.error('Error al cargar navieras:', error);
      alert(error.response?.data?.detail || 'Error al cargar navieras');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingNaviera) {
        const updateData: NavieraUpdate = formData;
        await axios.put(`/navieras/${editingNaviera.id_navieras}`, updateData);
        alert('Naviera actualizada exitosamente');
      } else {
        await axios.post('/navieras', formData);
        alert('Naviera creada exitosamente');
      }
      setShowModal(false);
      resetForm();
      cargarNavieras();
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Error al guardar naviera');
    }
  };

  const handleEdit = (naviera: Naviera) => {
    setEditingNaviera(naviera);
    setFormData({
      codigo: naviera.codigo,
      nombre: naviera.nombre,
    });
    setShowModal(true);
  };

  const handleDelete = async (id: number, nombre: string) => {
    if (!confirm(`¿Está seguro que desea eliminar la naviera "${nombre}"?`)) return;
    try {
      await axios.delete(`/navieras/${id}`);
      alert('Naviera eliminada exitosamente');
      cargarNavieras();
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Error al eliminar naviera');
    }
  };

  const resetForm = () => {
    setEditingNaviera(null);
    setFormData({
      codigo: '',
      nombre: '',
    });
  };

  return (
    <div className="p-6">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Gestión de Navieras</h1>
            <p className="text-gray-600 mt-1">Administrar compañías navieras</p>
          </div>
          <button
            onClick={() => {
              resetForm();
              setShowModal(true);
            }}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Plus className="w-5 h-5" />
            Nueva Naviera
          </button>
        </div>
      </div>

      {/* Grid de tarjetas */}
      {loading ? (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <p className="text-gray-600 mt-4">Cargando navieras...</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {navieras.map((naviera) => (
            <div
              key={naviera.id_navieras}
              className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow p-6"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                    <Ship className="w-6 h-6 text-blue-600" />
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-gray-900">{naviera.nombre}</h3>
                    <p className="text-sm text-gray-500">{naviera.codigo}</p>
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-2 text-sm text-gray-500 mb-4">
                <Anchor className="w-4 h-4" />
                <span>Creada: {new Date(naviera.creado_en).toLocaleDateString('es-ES')}</span>
              </div>
              <div className="flex gap-2 pt-4 border-t">
                <button
                  onClick={() => handleEdit(naviera)}
                  className="flex-1 flex items-center justify-center gap-2 px-3 py-2 text-blue-600 border border-blue-600 rounded-lg hover:bg-blue-50 transition-colors"
                >
                  <Edit className="w-4 h-4" />
                  Editar
                </button>
                <button
                  onClick={() => handleDelete(naviera.id_navieras, naviera.nombre)}
                  className="flex-1 flex items-center justify-center gap-2 px-3 py-2 text-red-600 border border-red-600 rounded-lg hover:bg-red-50 transition-colors"
                >
                  <Trash2 className="w-4 h-4" />
                  Eliminar
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {navieras.length === 0 && !loading && (
        <div className="text-center py-12 bg-white rounded-lg">
          <Ship className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600 text-lg">No hay navieras registradas</p>
          <p className="text-gray-400 text-sm mt-2">Crea la primera naviera para comenzar</p>
        </div>
      )}

      {/* Modal de formulario */}
      {showModal && (
        <>
          <div className="fixed inset-0 bg-black bg-opacity-50 z-40" onClick={() => setShowModal(false)} />
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">
                {editingNaviera ? 'Editar Naviera' : 'Nueva Naviera'}
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
                      placeholder="Ej: MAERSK"
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
                      placeholder="Ej: Maersk Line"
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
                    {editingNaviera ? 'Actualizar' : 'Crear Naviera'}
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

export default Navieras;
