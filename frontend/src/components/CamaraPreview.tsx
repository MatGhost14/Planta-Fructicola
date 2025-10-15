import React, { useRef, useState, useEffect } from 'react';

interface CamaraPreviewProps {
  onCapture: (imageDataUrl: string) => void;
}

const CamaraPreview: React.FC<CamaraPreviewProps> = ({ onCapture }) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [error, setError] = useState<string>('');
  const [capturing, setCapturing] = useState(false);

  useEffect(() => {
    iniciarCamara();
    return () => {
      detenerCamara();
    };
  }, []);

  const iniciarCamara = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: { 
          facingMode: 'environment',
          width: { ideal: 1920, max: 3840 },
          height: { ideal: 1080, max: 2160 },
          aspectRatio: { ideal: 16/9 }
        }
      });
      
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
      setStream(mediaStream);
      setError('');
    } catch (err) {
      console.error('Error al acceder a la cámara:', err);
      setError('No se pudo acceder a la cámara. Verifica los permisos.');
    }
  };

  const detenerCamara = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
    }
  };

  const capturarFoto = () => {
    if (!videoRef.current || !canvasRef.current) return;

    setCapturing(true);
    const video = videoRef.current;
    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');

    if (context) {
      // Usar las dimensiones reales del video para mejor calidad
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      
      // Dibujar imagen con mejor calidad
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      
      // Aumentar calidad JPEG a 0.95 (de 0.8)
      const imageDataUrl = canvas.toDataURL('image/jpeg', 0.95);
      onCapture(imageDataUrl);

      // Efecto flash
      setTimeout(() => setCapturing(false), 200);
    }
  };

  return (
    <div className="relative bg-gray-900 rounded-lg overflow-hidden">
      {error ? (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
          {error}
        </div>
      ) : (
        <>
          {/* Video preview */}
          <div className="relative flex items-center justify-center min-h-[300px] max-h-[600px]">
            <video
              ref={videoRef}
              autoPlay
              playsInline
              className="w-full h-full rounded-lg"
              style={{ objectFit: 'contain' }}
            />
          </div>
          
          <canvas ref={canvasRef} className="hidden" />
          
          {/* Efecto flash al capturar */}
          {capturing && (
            <div className="absolute inset-0 bg-white opacity-80 animate-pulse" />
          )}

          {/* Botón de captura mejorado */}
          <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/60 to-transparent p-6">
            <button
              type="button"
              onClick={capturarFoto}
              className="mx-auto block w-20 h-20 bg-white rounded-full shadow-2xl flex items-center justify-center hover:scale-105 active:scale-95 transition-transform"
              title="Capturar foto"
            >
              <div className="w-[72px] h-[72px] border-4 border-blue-500 rounded-full flex items-center justify-center">
                <div className="w-14 h-14 bg-blue-500 rounded-full" />
              </div>
            </button>
            
            {/* Texto de ayuda */}
            <p className="text-center text-white text-sm mt-3 drop-shadow-lg">
              📸 Toca el botón para capturar
            </p>
          </div>

          {/* Indicador de resolución */}
          <div className="absolute top-4 right-4 bg-black/50 backdrop-blur-sm text-white px-3 py-1.5 rounded-full text-xs font-medium">
            🎥 HD
          </div>
        </>
      )}
    </div>
  );
};

export default CamaraPreview;
