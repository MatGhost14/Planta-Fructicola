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
        video: { facingMode: 'environment', width: 1280, height: 720 }
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
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      context.drawImage(video, 0, 0);
      
      const imageDataUrl = canvas.toDataURL('image/jpeg', 0.8);
      onCapture(imageDataUrl);

      // Efecto flash
      setTimeout(() => setCapturing(false), 200);
    }
  };

  return (
    <div className="relative">
      {error ? (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
          {error}
        </div>
      ) : (
        <>
          <video
            ref={videoRef}
            autoPlay
            playsInline
            className="w-full rounded-lg bg-black"
            style={{ maxHeight: '400px', objectFit: 'cover' }}
          />
          <canvas ref={canvasRef} className="hidden" />
          
          {capturing && (
            <div className="absolute inset-0 bg-white opacity-80 rounded-lg" />
          )}

          <button
            type="button"
            onClick={capturarFoto}
            className="absolute bottom-4 left-1/2 transform -translate-x-1/2 w-16 h-16 bg-white rounded-full shadow-lg flex items-center justify-center hover:bg-gray-100 transition-colors"
          >
            <div className="w-14 h-14 border-4 border-blue-600 rounded-full flex items-center justify-center">
              <div className="w-10 h-10 bg-blue-600 rounded-full" />
            </div>
          </button>
        </>
      )}
    </div>
  );
};

export default CamaraPreview;
