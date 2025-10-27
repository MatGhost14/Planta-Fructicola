import React, { useRef, useState, useEffect } from "react";

interface CamaraPreviewProps {
  onCapture: (imageDataUrl: string | string[]) => void;
  onClose: () => void;
}

const CamaraPreview: React.FC<CamaraPreviewProps> = ({
  onCapture,
  onClose,
}) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [error, setError] = useState<string>("");
  const [capturing, setCapturing] = useState(false);
  const [fotoCapturada, setFotoCapturada] = useState<string | null>(null);
  const [burstMode, setBurstMode] = useState(false);
  const [burstCount, setBurstCount] = useState<number>(3);
  const [burstFotos, setBurstFotos] = useState<string[]>([]);

  useEffect(() => {
    iniciarCamara();
    return () => {
      detenerCamara();
    };
  }, []);

  // Efecto para mantener el srcObject asignado
  useEffect(() => {
    if (videoRef.current && stream && !fotoCapturada) {
      if (videoRef.current.srcObject !== stream) {
        console.log("🔧 Asignando srcObject al video");
        videoRef.current.srcObject = stream;
      }
    }
  }, [stream, fotoCapturada]);

  // Efecto para asegurar que el video se reanude cuando fotoCapturada se limpia
  useEffect(() => {
    console.log(
      "🔄 useEffect triggered - fotoCapturada:",
      fotoCapturada,
      "stream:",
      !!stream,
      "videoRef:",
      !!videoRef.current
    );

    if (fotoCapturada === null && videoRef.current && stream) {
      console.log("▶️ Intentando reanudar video...");

      const video = videoRef.current;

      // Verificar si el video tiene el stream asignado
      if (!video.srcObject) {
        console.log("⚠️ Video sin srcObject, reasignando stream...");
        video.srcObject = stream;
      }

      // Pequeño delay para asegurar que el DOM se actualice
      const timer = setTimeout(() => {
        if (videoRef.current) {
          const video = videoRef.current;
          console.log(
            "📊 Estado del video - paused:",
            video.paused,
            "readyState:",
            video.readyState,
            "srcObject:",
            !!video.srcObject
          );

          // Si readyState es 0, esperar a que cargue
          if (video.readyState === 0) {
            console.log(
              "⏳ Video no listo, esperando evento loadedmetadata..."
            );
            const handleLoadedMetadata = () => {
              console.log("✅ Video metadata cargada, reproduciendo...");
              video
                .play()
                .then(() => console.log("✅ Video reanudado exitosamente"))
                .catch((err) =>
                  console.error("❌ Play falló después de metadata:", err)
                );
              video.removeEventListener("loadedmetadata", handleLoadedMetadata);
            };
            video.addEventListener("loadedmetadata", handleLoadedMetadata);
          } else {
            // Video listo, reproducir directamente
            video
              .play()
              .then(() => {
                console.log("✅ Video reanudado exitosamente");
              })
              .catch((err) => {
                console.error("❌ Video play() en useEffect falló:", err);
              });
          }
        }
      }, 100);

      return () => clearTimeout(timer);
    }
  }, [fotoCapturada, stream]);

  const iniciarCamara = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: "environment",
          width: { ideal: 1920, max: 3840 },
          height: { ideal: 1080, max: 2160 },
          aspectRatio: { ideal: 16 / 9 },
        },
      });

      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
        // Forzar play después de asignar srcObject
        await videoRef.current.play().catch((err) => {
          console.warn("Play en iniciarCamara:", err);
        });
      }
      setStream(mediaStream);
      setError("");
    } catch (err) {
      console.error("Error al acceder a la cámara:", err);
      setError("No se pudo acceder a la cámara. Verifica los permisos.");
    }
  };

  const detenerCamara = () => {
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
    }
  };

  const capturarFoto = () => {
    if (!videoRef.current || !canvasRef.current) return;
    // Función auxiliar para capturar una sola imagen y devolver dataUrl
    const captureSingle = (): string | null => {
      const video = videoRef.current!;
      const canvas = canvasRef.current!;
      const context = canvas.getContext("2d");
      if (!context) return null;
      canvas.width = video.videoWidth || 1280;
      canvas.height = video.videoHeight || 720;
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      return canvas.toDataURL("image/jpeg", 0.95);
    };

    const sleep = (ms: number) =>
      new Promise((resolve) => setTimeout(resolve, ms));

    console.log("📸 Capturando foto(s)...");
    setCapturing(true);

    if (burstMode) {
      // Captura en ráfaga: N fotos con pequeño delay entre ellas
      (async () => {
        const fotos: string[] = [];
        for (let i = 0; i < burstCount; i++) {
          const dataUrl = captureSingle();
          if (dataUrl) fotos.push(dataUrl);
          // pequeño delay para dar tiempo al sensor/animación
          await sleep(200);
        }
        setBurstFotos(fotos);
        // Pausar video cuando se captura
        if (videoRef.current) {
          videoRef.current.pause();
          console.log("⏸️ Video pausado después de ráfaga");
        }
        setCapturing(false);
      })();
    } else {
      const dataUrl = captureSingle();
      if (dataUrl) {
        setFotoCapturada(dataUrl);
        if (videoRef.current) {
          videoRef.current.pause();
          console.log("⏸️ Video pausado después de captura");
        }
      }
      setTimeout(() => setCapturing(false), 200);
    }
  };

  const tomarDeNuevo = () => {
    // Anular la foto y preparar cámara para nueva captura
    // NO guardar la foto, solo descartarla
    console.log("🔄 Tomar de Nuevo - Descartando foto");
    setFotoCapturada(null);
    setBurstFotos([]);
    setCapturing(false);
    // El useEffect se encargará de reanudar el video
  };

  const guardarFoto = () => {
    // Guardar foto y CERRAR la cámara completamente
    if (burstFotos.length > 0) {
      console.log("✅ Guardar ráfaga y Terminar - Guardando fotos y cerrando");
      // Enviar todas las fotos capturadas en ráfaga como un array
      onCapture(burstFotos);
      detenerCamara();
      onClose();
      return;
    }

    if (fotoCapturada) {
      console.log("✅ Guardar y Terminar - Guardando foto y cerrando");
      onCapture(fotoCapturada);
      detenerCamara();
      onClose();
    }
  };

  const tomarOtraFoto = () => {
    // Guardar foto(s) actual(es) y preparar para siguiente
    if (burstFotos.length > 0) {
      console.log(
        "💾 Guardar ráfaga y Tomar Otra - Guardando ráfaga y preparando para siguiente"
      );
      // Enviar todas las fotos de ráfaga como un array
      onCapture(burstFotos);
      setBurstFotos([]);
      setCapturing(false);
      setFotoCapturada(null);
      // El useEffect reanudará el video
      return;
    }

    if (fotoCapturada) {
      console.log(
        "💾 Guardar y Tomar Otra - Guardando y preparando para siguiente"
      );
      onCapture(fotoCapturada);

      // Resetear estado para permitir nueva captura
      setFotoCapturada(null);
      setCapturing(false);
      // El useEffect se encargará de reanudar el video
    }
  };

  const confirmarRafaga = () => {
    // Guardar todas las fotos de la ráfaga y cerrar cámara
    if (burstFotos.length > 0) {
      console.log("✅ Confirmar ráfaga - Guardando todas las fotos y cerrando");
      // Enviar todas las fotos de ráfaga como un array
      onCapture(burstFotos);
      detenerCamara();
      onClose();
    }
  };

  const tomarNuevaRafaga = () => {
    // Descartar fotos actuales y preparar para nueva ráfaga
    console.log("🔄 Tomar nueva ráfaga - Descartando fotos y reiniciando");
    setBurstFotos([]);
    setFotoCapturada(null);
    setCapturing(false);
    // El useEffect se encargará de reanudar el video
  };

  const cerrarCamara = () => {
    detenerCamara();
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 bg-black flex flex-col">
      <div className="w-full h-full bg-gray-900 flex flex-col">
        {error ? (
          <div className="p-4 sm:p-6">
            <div className="bg-red-50 border-2 border-red-200 rounded-lg p-4 sm:p-6 text-red-700">
              <div className="flex items-start gap-3">
                <svg
                  className="w-6 h-6 flex-shrink-0 mt-0.5"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  />
                </svg>
                <div>
                  <h3 className="font-semibold text-lg mb-1">
                    Error de Cámara
                  </h3>
                  <p className="text-sm">{error}</p>
                </div>
              </div>
              <button
                onClick={cerrarCamara}
                className="mt-4 w-full sm:w-auto px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
              >
                Cerrar
              </button>
            </div>
          </div>
        ) : burstFotos.length > 0 ? (
          <div className="flex flex-col h-full bg-gray-900">
            {/* Header para galería */}
            <div className="flex-shrink-0 bg-gray-800 px-3 py-2 border-b border-gray-700">
              <div className="flex items-center justify-between">
                <h3 className="text-white font-medium text-sm flex items-center gap-2">
                  <span className="text-base">📸</span>
                  Ráfaga Capturada ({burstFotos.length} fotos)
                </h3>
                <button
                  onClick={cerrarCamara}
                  className="text-gray-400 hover:text-white transition-colors p-1"
                >
                  <svg
                    className="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>
              </div>
            </div>

            {/* Grid de fotos */}
            <div className="flex-1 p-4 overflow-y-auto">
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {burstFotos.map((foto, index) => (
                  <div key={index} className="relative group">
                    <img
                      src={foto}
                      alt={`Foto ${index + 1}`}
                      className="w-full h-48 sm:h-64 object-cover rounded-lg border border-gray-600 group-hover:border-blue-500 transition-colors"
                    />
                    <div className="absolute top-2 right-2 bg-black/70 text-white px-2 py-1 rounded text-sm font-medium">
                      {index + 1}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Botones de acción */}
            <div className="flex-shrink-0 bg-gray-800 p-4 border-t border-gray-700">
              <div className="flex gap-3 justify-center">
                <button
                  onClick={confirmarRafaga}
                  className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-medium transition-colors flex items-center gap-2"
                >
                  ✅ Usar estas fotos
                </button>
                <button
                  onClick={tomarNuevaRafaga}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors flex items-center gap-2"
                >
                  📸 Nueva ráfaga
                </button>
                <button
                  onClick={cerrarCamara}
                  className="bg-gray-600 hover:bg-gray-700 text-white px-6 py-3 rounded-lg font-medium transition-colors"
                >
                  Cerrar
                </button>
              </div>
            </div>
          </div>
        ) : (
          <>
            {/* Header - Altura fija y compacta */}
            <div className="flex-shrink-0 bg-gray-800 px-3 py-2 border-b border-gray-700">
              <div className="flex items-center justify-between">
                {/* Título */}
                <h3 className="text-white font-medium text-sm flex items-center gap-2">
                  <span className="text-base">📸</span>
                  <span className="hidden sm:inline">
                    {burstFotos.length > 0
                      ? `Ráfaga (${burstFotos.length})`
                      : fotoCapturada
                      ? "Vista Previa"
                      : "Capturar Foto"}
                  </span>
                </h3>

                {/* Controles de ráfaga - Al lado del título */}
                <div className="flex items-center gap-1 sm:gap-3">
                  {!fotoCapturada && burstFotos.length === 0 && (
                    <>
                      <div className="flex items-center gap-1 text-xs text-white">
                        <label className="flex items-center gap-1 cursor-pointer">
                          <input
                            type="checkbox"
                            checked={burstMode}
                            onChange={() => setBurstMode(!burstMode)}
                            className="w-3 h-3 cursor-pointer"
                          />
                          <span className="hidden sm:inline text-xs">
                            Ráfaga
                          </span>
                          <span className="sm:hidden">📷</span>
                        </label>
                      </div>

                      {burstMode && (
                        <div className="flex items-center gap-1">
                          {[3, 4, 5].map((n) => (
                            <button
                              key={n}
                              type="button"
                              onClick={() => setBurstCount(n)}
                              className={`px-1.5 py-0.5 rounded text-xs font-medium transition-colors ${
                                burstCount === n
                                  ? "bg-blue-600 text-white"
                                  : "bg-gray-700 text-gray-200 hover:bg-gray-600"
                              }`}
                              title={`Capturar ${n} fotos`}
                            >
                              {n}
                            </button>
                          ))}
                        </div>
                      )}
                    </>
                  )}

                  {/* Botón cerrar */}
                  <button
                    onClick={cerrarCamara}
                    className="text-gray-400 hover:text-white transition-colors p-1 flex-shrink-0"
                    title="Cerrar"
                  >
                    <svg
                      className="w-5 h-5"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M6 18L18 6M6 6l12 12"
                      />
                    </svg>
                  </button>
                </div>
              </div>
            </div>

            {/* Video/Imagen Preview - Área principal */}
            <div className="flex-1 flex flex-col bg-black overflow-hidden">
              {!fotoCapturada ? (
                <div className="flex-1 relative">
                  <div className="absolute inset-0 flex items-center justify-center">
                    <video
                      ref={videoRef}
                      autoPlay
                      playsInline
                      muted
                      className="w-full h-full object-cover"
                    />
                  </div>

                  {/* Indicador HD */}
                  <div className="absolute top-3 right-3 bg-black/50 backdrop-blur-sm text-white px-2 py-1 rounded-full text-xs font-medium">
                    🎥 HD
                  </div>

                  {/* Efecto flash */}
                  {capturing && (
                    <div className="absolute inset-0 bg-white opacity-80 animate-pulse" />
                  )}

                  {/* Botón captura */}
                  <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent p-4">
                    <button
                      type="button"
                      onClick={capturarFoto}
                      className="mx-auto block w-16 h-16 bg-white rounded-full shadow-2xl flex items-center justify-center hover:scale-105 active:scale-95 transition-transform"
                      title="Capturar foto"
                    >
                      <div className="w-14 h-14 border-4 border-blue-500 rounded-full flex items-center justify-center">
                        <div className="w-10 h-10 bg-blue-500 rounded-full" />
                      </div>
                    </button>
                    <p className="text-center text-white text-xs mt-2 drop-shadow-lg">
                      📸 Toca el botón para capturar
                    </p>
                  </div>
                </div>
              ) : (
                <>
                  {/* Imagen capturada */}
                  <div className="flex-1 relative bg-black flex items-center justify-center">
                    <img
                      src={fotoCapturada}
                      alt="Foto capturada"
                      className="max-w-full max-h-full object-contain"
                    />

                    {/* Badge de confirmación */}
                    <div className="absolute top-3 left-3 bg-green-500/90 backdrop-blur-sm text-white px-3 py-1.5 rounded-full text-xs font-medium flex items-center gap-1.5">
                      <svg
                        className="w-4 h-4"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path
                          fillRule="evenodd"
                          d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        />
                      </svg>
                      Foto Capturada
                    </div>
                  </div>

                  {/* Botones de acción - Siempre visibles */}
                  <div className="flex-shrink-0 bg-gray-800 p-4 border-t border-gray-700">
                    <p className="text-gray-300 text-sm mb-4 text-center">
                      ¿Qué deseas hacer con esta foto?
                    </p>
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                      {/* Tomar de nuevo */}
                      <button
                        type="button"
                        onClick={tomarDeNuevo}
                        className="flex items-center justify-center gap-2 px-4 py-3 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors text-sm font-medium"
                      >
                        <svg
                          className="w-5 h-5"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                          />
                        </svg>
                        <span>Tomar de Nuevo</span>
                      </button>

                      {/* Guardar y tomar otra */}
                      <button
                        type="button"
                        onClick={tomarOtraFoto}
                        className="flex items-center justify-center gap-2 px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
                      >
                        <svg
                          className="w-5 h-5"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M12 4v16m8-8H4"
                          />
                        </svg>
                        <span className="hidden sm:inline">
                          Guardar y Tomar Otra
                        </span>
                        <span className="sm:hidden">Tomar Otra</span>
                      </button>

                      {/* Guardar y terminar */}
                      <button
                        type="button"
                        onClick={guardarFoto}
                        className="flex items-center justify-center gap-2 px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm font-medium"
                      >
                        <svg
                          className="w-5 h-5"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M5 13l4 4L19 7"
                          />
                        </svg>
                        <span className="hidden sm:inline">
                          Guardar y Terminar
                        </span>
                        <span className="sm:hidden">Terminar</span>
                      </button>
                    </div>
                  </div>
                </>
              )}
            </div>

            <canvas ref={canvasRef} className="hidden" />
          </>
        )}
      </div>
    </div>
  );
};

export default CamaraPreview;
