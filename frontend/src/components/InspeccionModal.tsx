/**
 * Modal de detalle de inspección
 * Muestra toda la información de la inspección incluyendo fotos y firma
 */
import React, { useState } from 'react';
import { X, Image as ImageIcon, FileText, MapPin, Ship, Thermometer, Calendar, User, CheckCircle, XCircle, Clock, ThumbsUp, ThumbsDown } from 'lucide-react';
import type { InspeccionDetalle } from '../types';
import { inspeccionesApi } from '../api/inspecciones';
import { useAuth } from '../contexts/AuthContext';
import { useToast } from './ToastProvider';

interface InspeccionModalProps {
  inspeccion: InspeccionDetalle | null;
  isOpen: boolean;
  onClose: () => void;
  onUpdate?: () => void;
}

const InspeccionModal: React.FC<InspeccionModalProps> = ({ inspeccion, isOpen, onClose, onUpdate }) => {
  const [selectedPhoto, setSelectedPhoto] = useState<string | null>(null);
  const [showApprovalModal, setShowApprovalModal] = useState(false);
  const [showRejectionModal, setShowRejectionModal] = useState(false);
  const [comentario, setComentario] = useState('');
  const [loading, setLoading] = useState(false);
  const { user } = useAuth();
  const { showSuccess, showError, showWarning } = useToast();

  if (!isOpen || !inspeccion) return null;

  const canChangeStatus = user && (user.rol === 'supervisor' || user.rol === 'admin') && inspeccion.estado === 'pending';

  const handleAprobar = async () => {
    setLoading(true);
    try {
      await inspeccionesApi.cambiarEstado(inspeccion.id_inspeccion, 'approved', comentario || undefined);
      setShowApprovalModal(false);
      setComentario('');
      showSuccess('Inspección aprobada exitosamente');
      if (onUpdate) onUpdate();
      onClose();
    } catch (error: any) {
      showError(error.response?.data?.detail || 'Error al aprobar la inspección');
    } finally {
      setLoading(false);
    }
  };

  const handleRechazar = async () => {
    if (!comentario.trim()) {
      showWarning('Debe proporcionar un comentario al rechazar');
      return;
    }
    setLoading(true);
    try {
      await inspeccionesApi.cambiarEstado(inspeccion.id_inspeccion, 'rejected', comentario);
      setShowRejectionModal(false);
      setComentario('');
      showSuccess('Inspección rechazada');
      if (onUpdate) onUpdate();
      onClose();
    } catch (error: any) {
      showError(error.response?.data?.detail || 'Error al rechazar la inspección');
    } finally {
      setLoading(false);
    }
  };

  const getEstadoColor = (estado: string) => {
    switch (estado) {
      case 'approved':
        return 'bg-green-100 text-green-800';
      case 'rejected':
        return 'bg-red-100 text-red-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getEstadoTexto = (estado: string) => {
    switch (estado) {
      case 'approved':
        return 'Aprobada';
      case 'rejected':
        return 'Rechazada';
      case 'pending':
        return 'Pendiente';
      default:
        return estado;
    }
  };

  const getEstadoIcon = (estado: string) => {
    switch (estado) {
      case 'approved':
        return <CheckCircle className="w-5 h-5" />;
      case 'rejected':
        return <XCircle className="w-5 h-5" />;
      case 'pending':
        return <Clock className="w-5 h-5" />;
      default:
        return null;
    }
  };

  return (
    <>
      {/* Overlay */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 z-40 transition-opacity"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 overflow-y-auto">
        <div
          className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="sticky top-0 bg-white border-b px-6 py-4 flex items-center justify-between z-10">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">
                Inspección {inspeccion.codigo}
              </h2>
              <p className="text-sm text-gray-500 mt-1">
                Contenedor: {inspeccion.numero_contenedor}
              </p>
            </div>
            <div className="flex items-center gap-3">
              <span
                className={`inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium ${getEstadoColor(
                  inspeccion.estado
                )}`}
              >
                {getEstadoIcon(inspeccion.estado)}
                {getEstadoTexto(inspeccion.estado)}
              </span>
              <button
                onClick={onClose}
                className="p-2 hover:bg-gray-100 rounded-full transition-colors"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
          </div>

          {/* Content */}
          <div className="p-6 space-y-6">
            {/* Información General */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="flex items-start gap-3 p-4 bg-gray-50 rounded-lg">
                <MapPin className="w-5 h-5 text-blue-600 mt-0.5" />
                <div>
                  <p className="text-sm font-medium text-gray-500">Planta</p>
                  <p className="text-base font-semibold text-gray-900">
                    {inspeccion.planta.nombre}
                  </p>
                  {inspeccion.planta.ubicacion && (
                    <p className="text-sm text-gray-600">{inspeccion.planta.ubicacion}</p>
                  )}
                </div>
              </div>

              <div className="flex items-start gap-3 p-4 bg-gray-50 rounded-lg">
                <Ship className="w-5 h-5 text-blue-600 mt-0.5" />
                <div>
                  <p className="text-sm font-medium text-gray-500">Naviera</p>
                  <p className="text-base font-semibold text-gray-900">
                    {inspeccion.naviera.nombre}
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3 p-4 bg-gray-50 rounded-lg">
                <User className="w-5 h-5 text-blue-600 mt-0.5" />
                <div>
                  <p className="text-sm font-medium text-gray-500">Inspector</p>
                  <p className="text-base font-semibold text-gray-900">
                    {inspeccion.inspector.nombre}
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3 p-4 bg-gray-50 rounded-lg">
                <Calendar className="w-5 h-5 text-blue-600 mt-0.5" />
                <div>
                  <p className="text-sm font-medium text-gray-500">Fecha de Inspección</p>
                  <p className="text-base font-semibold text-gray-900">
                    {new Date(inspeccion.inspeccionado_en).toLocaleDateString('es-ES', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit',
                    })}
                  </p>
                </div>
              </div>
            </div>

            {/* Temperatura */}
            {inspeccion.temperatura_c !== null && inspeccion.temperatura_c !== undefined && (
              <div className="flex items-start gap-3 p-4 bg-blue-50 rounded-lg">
                <Thermometer className="w-5 h-5 text-blue-600 mt-0.5" />
                <div>
                  <p className="text-sm font-medium text-gray-500">Temperatura</p>
                  <p className="text-2xl font-bold text-blue-900">
                    {inspeccion.temperatura_c}°C
                  </p>
                </div>
              </div>
            )}

            {/* Observaciones */}
            {inspeccion.observaciones && (
              <div className="p-4 bg-gray-50 rounded-lg">
                <div className="flex items-start gap-3">
                  <FileText className="w-5 h-5 text-gray-600 mt-0.5" />
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-500 mb-2">Observaciones</p>
                    <p className="text-gray-700 whitespace-pre-wrap">
                      {inspeccion.observaciones}
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Fotos */}
            {inspeccion.fotos && inspeccion.fotos.length > 0 && (
              <div>
                <div className="flex items-center gap-2 mb-4">
                  <ImageIcon className="w-5 h-5 text-gray-600" />
                  <h3 className="text-lg font-semibold text-gray-900">
                    Fotografías ({inspeccion.fotos.length})
                  </h3>
                </div>
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                  {inspeccion.fotos.map((foto) => (
                    <div
                      key={foto.id_foto}
                      className="relative aspect-square rounded-lg overflow-hidden cursor-pointer group"
                      onClick={() => setSelectedPhoto(foto.foto_path)}
                    >
                      <img
                        src={foto.foto_path}
                        alt={`Foto de inspección ${inspeccion.codigo}`}
                        className="w-full h-full object-cover transition-transform group-hover:scale-110"
                      />
                      <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-opacity flex items-center justify-center">
                        <ImageIcon className="w-8 h-8 text-white opacity-0 group-hover:opacity-100 transition-opacity" />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Firma */}
            {inspeccion.firma_path && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Firma Digital</h3>
                <div className="border-2 border-gray-200 rounded-lg p-4 bg-white inline-block">
                  <img
                    src={inspeccion.firma_path}
                    alt="Firma del inspector"
                    className="max-w-sm max-h-32"
                  />
                </div>
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="sticky bottom-0 bg-gray-50 border-t px-6 py-4 flex justify-between items-center gap-3">
            {/* Botones de aprobación/rechazo (solo para supervisor/admin) */}
            {canChangeStatus && (
              <div className="flex gap-3">
                <button
                  onClick={() => setShowApprovalModal(true)}
                  disabled={loading}
                  className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <ThumbsUp className="w-4 h-4" />
                  Aprobar
                </button>
                <button
                  onClick={() => setShowRejectionModal(true)}
                  disabled={loading}
                  className="flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <ThumbsDown className="w-4 h-4" />
                  Rechazar
                </button>
              </div>
            )}
            <div className="flex-1"></div>
            <button
              onClick={onClose}
              className="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Cerrar
            </button>
          </div>
        </div>
      </div>

      {/* Lightbox para fotos */}
      {selectedPhoto && (
        <div
          className="fixed inset-0 bg-black bg-opacity-90 z-[60] flex items-center justify-center p-4"
          onClick={() => setSelectedPhoto(null)}
        >
          <button
            onClick={() => setSelectedPhoto(null)}
            className="absolute top-4 right-4 p-2 text-white hover:bg-white hover:bg-opacity-20 rounded-full transition-colors"
          >
            <X className="w-8 h-8" />
          </button>
          <img
            src={selectedPhoto}
            alt="Vista ampliada"
            className="max-w-full max-h-full object-contain"
            onClick={(e) => e.stopPropagation()}
          />
        </div>
      )}

      {/* Modal de aprobación */}
      {showApprovalModal && (
        <>
          <div className="fixed inset-0 bg-black bg-opacity-50 z-[70]" onClick={() => setShowApprovalModal(false)} />
          <div className="fixed inset-0 z-[80] flex items-center justify-center p-4">
            <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center">
                  <CheckCircle className="w-6 h-6 text-green-600" />
                </div>
                <h3 className="text-xl font-bold text-gray-900">Aprobar Inspección</h3>
              </div>
              <p className="text-gray-600 mb-4">
                ¿Está seguro que desea aprobar la inspección <strong>{inspeccion.codigo}</strong>?
              </p>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Comentario (opcional)
                </label>
                <textarea
                  value={comentario}
                  onChange={(e) => setComentario(e.target.value)}
                  placeholder="Agregar un comentario sobre la aprobación..."
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  rows={3}
                />
              </div>
              <div className="flex justify-end gap-3">
                <button
                  onClick={() => setShowApprovalModal(false)}
                  disabled={loading}
                  className="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50"
                >
                  Cancelar
                </button>
                <button
                  onClick={handleAprobar}
                  disabled={loading}
                  className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50"
                >
                  {loading ? 'Aprobando...' : 'Confirmar Aprobación'}
                </button>
              </div>
            </div>
          </div>
        </>
      )}

      {/* Modal de rechazo */}
      {showRejectionModal && (
        <>
          <div className="fixed inset-0 bg-black bg-opacity-50 z-[70]" onClick={() => setShowRejectionModal(false)} />
          <div className="fixed inset-0 z-[80] flex items-center justify-center p-4">
            <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-12 h-12 rounded-full bg-red-100 flex items-center justify-center">
                  <XCircle className="w-6 h-6 text-red-600" />
                </div>
                <h3 className="text-xl font-bold text-gray-900">Rechazar Inspección</h3>
              </div>
              <p className="text-gray-600 mb-4">
                ¿Está seguro que desea rechazar la inspección <strong>{inspeccion.codigo}</strong>?
              </p>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Motivo del rechazo <span className="text-red-500">*</span>
                </label>
                <textarea
                  value={comentario}
                  onChange={(e) => setComentario(e.target.value)}
                  placeholder="Explique el motivo del rechazo..."
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  rows={4}
                  required
                />
                <p className="text-sm text-gray-500 mt-1">Este comentario será visible para el inspector</p>
              </div>
              <div className="flex justify-end gap-3">
                <button
                  onClick={() => {
                    setShowRejectionModal(false);
                    setComentario('');
                  }}
                  disabled={loading}
                  className="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50"
                >
                  Cancelar
                </button>
                <button
                  onClick={handleRechazar}
                  disabled={loading || !comentario.trim()}
                  className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? 'Rechazando...' : 'Confirmar Rechazo'}
                </button>
              </div>
            </div>
          </div>
        </>
      )}
    </>
  );
};

export default InspeccionModal;
