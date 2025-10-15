import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { inspeccionesApi, plantasApi, navierasApi } from '../api';
import { useStore } from '../store';
import { useToast } from '../components/ToastProvider';
import CamaraPreview from '../components/CamaraPreview';
import FirmaCanvas from '../components/FirmaCanvas';
import { dataURLtoBlob, blobToFile } from '../utils';
import type { Planta, Naviera } from '../types';

const InspeccionNueva: React.FC = () => {
  const navigate = useNavigate();
  const { usuarioActual } = useStore();
  const { showSuccess, showError, showWarning } = useToast();
  
  const [plantas, setPlantas] = useState<Planta[]>([]);
  const [navieras, setNavieras] = useState<Naviera[]>([]);
  const [loading, setLoading] = useState(false);
  const [mostrarCamara, setMostrarCamara] = useState(false);
  const [mostrarFirma, setMostrarFirma] = useState(false);
  
  const [fotos, setFotos] = useState<string[]>([]);
  const [firma, setFirma] = useState<string>('');
  
  const [formData, setFormData] = useState({
    numero_contenedor: '',
    id_planta: '',
    id_navieras: '',
    temperatura_c: '',
    observaciones: ''
  });

  useEffect(() => {
    cargarCatalogos();
  }, []);

  const cargarCatalogos = async () => {
    try {
      const [plantasData, navierasData] = await Promise.all([
        plantasApi.listar(),
        navierasApi.listar()
      ]);
      setPlantas(plantasData);
      setNavieras(navierasData);
    } catch (error) {
      console.error('Error al cargar catálogos:', error);
      showError('Error al cargar catálogos');
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleCapturarFoto = (imageDataUrl: string) => {
    setFotos([...fotos, imageDataUrl]);
    showSuccess('Foto capturada correctamente');
  };

  const handleEliminarFoto = (index: number) => {
    setFotos(fotos.filter((_, i) => i !== index));
  };

  const handleGuardarFirma = (imageDataUrl: string) => {
    setFirma(imageDataUrl);
    setMostrarFirma(false);
    showSuccess('Firma guardada correctamente');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (fotos.length === 0) {
      showWarning('Debes capturar al menos una foto');
      return;
    }

    if (!firma) {
      showWarning('Debes agregar la firma');
      return;
    }

    try {
      setLoading(true);

      // 1. Crear inspección
      const inspeccionData = {
        numero_contenedor: formData.numero_contenedor,
        id_planta: parseInt(formData.id_planta),
        id_navieras: parseInt(formData.id_navieras),
        temperatura_c: formData.temperatura_c ? parseFloat(formData.temperatura_c) : undefined,
        observaciones: formData.observaciones || undefined,
        id_inspector: usuarioActual.id_usuario
      };

      const inspeccionCreada = await inspeccionesApi.crear(inspeccionData);

      // 2. Subir fotos
      const fotosFiles = fotos.map((dataUrl, index) => {
        const blob = dataURLtoBlob(dataUrl);
        return blobToFile(blob, `foto-${index + 1}.jpg`);
      });
      await inspeccionesApi.subirFotos(inspeccionCreada.id_inspeccion, fotosFiles);

      // 3. Subir firma
      const firmaBlob = dataURLtoBlob(firma);
      const firmaFile = blobToFile(firmaBlob, 'firma.png');
      await inspeccionesApi.subirFirma(inspeccionCreada.id_inspeccion, firmaFile);

      showSuccess(`Inspección ${inspeccionCreada.codigo} creada exitosamente`);
      navigate('/inspecciones');
    } catch (error: any) {
      console.error('Error al crear inspección:', error);
      showError(error.response?.data?.detail || 'Error al crear inspección');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="py-2">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-2xl sm:text-3xl font-bold text-gray-800">Nueva Inspección</h1>
        <button
          onClick={() => navigate('/inspecciones')}
          className="btn-secondary"
        >
          Cancelar
        </button>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6 sm:space-y-8">
        {/* Datos del Contenedor */}
        <div className="bg-white rounded-lg shadow-card p-5 sm:p-6">
          <h2 className="text-lg sm:text-xl font-semibold text-gray-800 mb-5 sm:mb-6">📦 Datos del Contenedor</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Número de Contenedor *
              </label>
              <input
                type="text"
                name="numero_contenedor"
                value={formData.numero_contenedor}
                onChange={handleInputChange}
                required
                className="input-field"
                placeholder="Ej: ABCD1234567"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Planta *
              </label>
              <select
                name="id_planta"
                value={formData.id_planta}
                onChange={handleInputChange}
                required
                className="input-field"
              >
                <option value="">Seleccionar planta</option>
                {plantas.map(planta => (
                  <option key={planta.id_planta} value={planta.id_planta}>
                    {planta.nombre}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Naviera *
              </label>
              <select
                name="id_navieras"
                value={formData.id_navieras}
                onChange={handleInputChange}
                required
                className="input-field"
              >
                <option value="">Seleccionar naviera</option>
                {navieras.map(naviera => (
                  <option key={naviera.id_navieras} value={naviera.id_navieras}>
                    {naviera.nombre}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Temperatura (°C)
              </label>
              <input
                type="number"
                name="temperatura_c"
                value={formData.temperatura_c}
                onChange={handleInputChange}
                step="0.1"
                className="input-field"
                placeholder="Ej: -18.5"
              />
            </div>
          </div>

          <div className="mt-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Observaciones
            </label>
            <textarea
              name="observaciones"
              value={formData.observaciones}
              onChange={handleInputChange}
              rows={3}
              className="input-field"
              placeholder="Notas adicionales sobre la inspección..."
            />
          </div>
        </div>

        {/* Fotos */}
        <div className="bg-white rounded-lg shadow-card p-5 sm:p-6">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-5 sm:mb-6">
            <h2 className="text-lg sm:text-xl font-semibold text-gray-800">📸 Fotos *</h2>
            <button
              type="button"
              onClick={() => setMostrarCamara(!mostrarCamara)}
              className="btn-primary"
            >
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              {mostrarCamara ? 'Cerrar Cámara' : 'Capturar Foto'}
            </button>
          </div>

          {mostrarCamara && (
            <div className="mb-4">
              <CamaraPreview 
                onCapture={handleCapturarFoto}
                onClose={() => setMostrarCamara(false)}
              />
            </div>
          )}

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {fotos.map((foto, index) => (
              <div key={index} className="relative group bg-gray-100 rounded-lg overflow-hidden">
                <img
                  src={foto}
                  alt={`Foto ${index + 1}`}
                  className="w-full h-40 object-contain"
                />
                <button
                  type="button"
                  onClick={() => handleEliminarFoto(index)}
                  className="absolute top-2 right-2 bg-red-600 text-white p-2 rounded-full opacity-0 group-hover:opacity-100 transition-opacity shadow-lg hover:bg-red-700"
                  title="Eliminar foto"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            ))}
          </div>

          {fotos.length === 0 && !mostrarCamara && (
            <p className="text-gray-500 text-center py-8">
              No hay fotos capturadas. Haz clic en "Capturar Foto" para agregar.
            </p>
          )}
        </div>

        {/* Firma */}
        <div className="bg-white rounded-lg shadow-card p-5 sm:p-6">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-5 sm:mb-6">
            <h2 className="text-lg sm:text-xl font-semibold text-gray-800">✍️ Firma del Inspector *</h2>
            {firma && (
              <button
                type="button"
                onClick={() => setMostrarFirma(true)}
                className="text-blue-600 hover:text-blue-700 text-sm"
              >
                Cambiar firma
              </button>
            )}
          </div>

          {!firma || mostrarFirma ? (
            <FirmaCanvas onSave={handleGuardarFirma} />
          ) : (
            <div className="border-2 border-gray-200 rounded-lg p-4 bg-gray-50">
              <img src={firma} alt="Firma" className="max-w-full h-auto" />
            </div>
          )}
        </div>

        {/* Botones */}
        <div className="flex gap-4">
          <button
            type="button"
            onClick={() => navigate('/inspecciones')}
            className="btn-secondary flex-1"
          >
            Cancelar
          </button>
          <button
            type="submit"
            disabled={loading}
            className="btn-primary flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Guardando...' : 'Guardar Inspección'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default InspeccionNueva;
