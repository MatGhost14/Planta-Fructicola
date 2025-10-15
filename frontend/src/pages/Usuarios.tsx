/**
 * Página de gestión de usuarios
 * Solo accesible para Admin
 */
import React, { useState, useEffect } from 'react';
import { UserPlus, Edit, Trash2, Shield, Mail, User as UserIcon, RefreshCw } from 'lucide-react';
import axios from '../api/axios';
import { useToast } from '../components/ToastProvider';
import type { Usuario, UsuarioCreate, UsuarioUpdate } from '../types';

const Usuarios: React.FC = () => {
  const { showSuccess, showError, confirm } = useToast();
  const [usuarios, setUsuarios] = useState<Usuario[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingUser, setEditingUser] = useState<Usuario | null>(null);
  const [formData, setFormData] = useState<UsuarioCreate>({
    nombre: '',
    correo: '',
    rol: 'inspector',
    password: '',
  });

  useEffect(() => {
    cargarUsuarios();
  }, []);

  const cargarUsuarios = async () => {
    try {
      setLoading(true);
      const response = await axios.get<Usuario[]>('/usuarios');
      setUsuarios(response.data);
    } catch (error: any) {
      console.error('Error al cargar usuarios:', error);
      showError(error.response?.data?.detail || 'Error al cargar usuarios');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingUser) {
        // Actualizar
        const updateData: UsuarioUpdate = {
          nombre: formData.nombre,
          correo: formData.correo,
          rol: formData.rol,
          password: formData.password || undefined,
        };
        await axios.put(`/usuarios/${editingUser.id_usuario}`, updateData);
        showSuccess('Usuario actualizado exitosamente');
      } else {
        // Crear
        await axios.post('/usuarios', formData);
        showSuccess('Usuario creado exitosamente');
      }
      setShowModal(false);
      resetForm();
      cargarUsuarios();
    } catch (error: any) {
      showError(error.response?.data?.detail || 'Error al guardar usuario');
    }
  };

  const handleEdit = (usuario: Usuario) => {
    setEditingUser(usuario);
    setFormData({
      nombre: usuario.nombre,
      correo: usuario.correo,
      rol: usuario.rol,
      password: '',
    });
    setShowModal(true);
  };

  const handleDelete = async (id: number, nombre: string) => {
    const confirmed = await confirm(`¿Está seguro que desea eliminar al usuario "${nombre}"?`);
    if (!confirmed) return;
    try {
      await axios.delete(`/usuarios/${id}`);
      showSuccess('Usuario eliminado exitosamente');
      cargarUsuarios();
    } catch (error: any) {
      showError(error.response?.data?.detail || 'Error al eliminar usuario');
    }
  };

  const handleToggleEstado = async (usuario: Usuario) => {
    const nuevoEstado = usuario.estado === 'active' ? 'inactive' : 'active';
    try {
      await axios.patch(`/usuarios/${usuario.id_usuario}/estado`, { estado: nuevoEstado });
      cargarUsuarios();
    } catch (error: any) {
      showError(error.response?.data?.detail || 'Error al cambiar estado');
    }
  };

  const resetForm = () => {
    setEditingUser(null);
    setFormData({
      nombre: '',
      correo: '',
      rol: 'inspector',
      password: '',
    });
  };

  const getRolColor = (rol: string) => {
    switch (rol) {
      case 'admin':
        return 'bg-purple-100 text-purple-800';
      case 'supervisor':
        return 'bg-blue-100 text-blue-800';
      case 'inspector':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getRolTexto = (rol: string) => {
    switch (rol) {
      case 'admin':
        return 'Administrador';
      case 'supervisor':
        return 'Supervisor';
      case 'inspector':
        return 'Inspector';
      default:
        return rol;
    }
  };

  return (
    <div className="py-2">
      {/* Header */}
      <div className="mb-8">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">Gestión de Usuarios</h1>
            <p className="text-sm sm:text-base text-gray-600 mt-2">Administrar cuentas de acceso al sistema</p>
          </div>
          <button
            onClick={() => {
              resetForm();
              setShowModal(true);
            }}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <UserPlus className="w-5 h-5" />
            Nuevo Usuario
          </button>
        </div>
      </div>

      {/* Tabla */}
      {loading ? (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <p className="text-gray-600 mt-4">Cargando usuarios...</p>
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Usuario
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Rol
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Estado
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Último Acceso
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Acciones
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {usuarios.map((usuario) => (
                <tr key={usuario.id_usuario} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 h-10 w-10 bg-gray-200 rounded-full flex items-center justify-center">
                        <UserIcon className="w-5 h-5 text-gray-600" />
                      </div>
                      <div className="ml-4">
                        <div className="text-sm font-medium text-gray-900">{usuario.nombre}</div>
                        <div className="text-sm text-gray-500">{usuario.correo}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium ${getRolColor(usuario.rol)}`}>
                      <Shield className="w-3 h-3" />
                      {getRolTexto(usuario.rol)}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <button
                      onClick={() => handleToggleEstado(usuario)}
                      className={`inline-flex px-3 py-1 rounded-full text-xs font-medium ${
                        usuario.estado === 'active'
                          ? 'bg-green-100 text-green-800 hover:bg-green-200'
                          : 'bg-red-100 text-red-800 hover:bg-red-200'
                      } transition-colors`}
                    >
                      {usuario.estado === 'active' ? 'Activo' : 'Inactivo'}
                    </button>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {usuario.ultimo_acceso
                      ? new Date(usuario.ultimo_acceso).toLocaleDateString('es-ES')
                      : 'Nunca'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button
                      onClick={() => handleEdit(usuario)}
                      className="text-blue-600 hover:text-blue-900 mr-4"
                      title="Editar"
                    >
                      <Edit className="w-5 h-5" />
                    </button>
                    <button
                      onClick={() => handleDelete(usuario.id_usuario, usuario.nombre)}
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
                {editingUser ? 'Editar Usuario' : 'Nuevo Usuario'}
              </h3>
              <form onSubmit={handleSubmit}>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Nombre completo *
                    </label>
                    <input
                      type="text"
                      value={formData.nombre}
                      onChange={(e) => setFormData({ ...formData, nombre: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Correo electrónico *
                    </label>
                    <input
                      type="email"
                      value={formData.correo}
                      onChange={(e) => setFormData({ ...formData, correo: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Rol *
                    </label>
                    <select
                      value={formData.rol}
                      onChange={(e) => setFormData({ ...formData, rol: e.target.value as any })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      required
                    >
                      <option value="inspector">Inspector</option>
                      <option value="supervisor">Supervisor</option>
                      <option value="admin">Administrador</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Contraseña {editingUser ? '(dejar vacío para no cambiar)' : '*'}
                    </label>
                    <input
                      type="password"
                      value={formData.password}
                      onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      required={!editingUser}
                      minLength={6}
                      placeholder={editingUser ? 'Dejar vacío para no cambiar' : ''}
                    />
                    <p className="text-xs text-gray-500 mt-1">Mínimo 6 caracteres</p>
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
                    {editingUser ? 'Actualizar' : 'Crear Usuario'}
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

export default Usuarios;
