import React, { useRef, useState, useImperativeHandle, forwardRef } from "react";
import { Camera, CheckCircle, Repeat, Zap } from "lucide-react";

function CameraCaptureComponent(
  {
    onCapture,
    mode = "single",
  }: {
    onCapture: (file: File | File[]) => void;
    mode?: "single" | "burst";
  },
  ref: React.ForwardedRef<{ restart: () => void }>
) {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const [preview, setPreview] = useState<string | string[] | null>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [facingMode, setFacingMode] = useState<"user" | "environment">("environment");
  const [loadingBurst, setLoadingBurst] = useState(false);

  const startCamera = async () => {
    if (stream) stream.getTracks().forEach((t: any) => t.stop());
    const media = await navigator.mediaDevices.getUserMedia({
      video: { facingMode },
    });
    setStream(media);
    if (videoRef.current) videoRef.current.srcObject = media;
  };

  const capture = async () => {
    if (!videoRef.current) return;
    const canvas = document.createElement("canvas");
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    ctx.drawImage(videoRef.current, 0, 0);
    return new Promise<File>((resolve) => {
      canvas.toBlob((blob) => {
        if (!blob) return;
        const file = new File([blob], "foto.jpg", { type: "image/jpeg" });
        resolve(file);
      }, "image/jpeg", 0.9);
    });
  };

  const handleSingle = async () => {
    const file = await capture();
    if (!file) return;
    setPreview(URL.createObjectURL(file));
    onCapture(file);
    if (stream) stream.getTracks().forEach((t) => t.stop());
  };

  const handleBurst = async () => {
    setLoadingBurst(true);
    const files: File[] = [];
    const previews: string[] = [];
    for (let i = 0; i < 3; i++) {
      const file = await capture();
      if (file) {
        files.push(file);
        previews.push(URL.createObjectURL(file));
      }
      await new Promise((r) => setTimeout(r, 4000));
    }
    setPreview(previews);
    onCapture(files);
    setLoadingBurst(false);
    if (stream) stream.getTracks().forEach((t) => t.stop());
  };

  const restart = () => {
    setPreview(null);
    startCamera();
  };

  const revertCamera = () => {
    setFacingMode((prev) => (prev === "environment" ? "user" : "environment"));
    setPreview(null);
    setTimeout(startCamera, 200);
  };

  useImperativeHandle(ref, () => ({ restart }));

  return (
    <div className="flex flex-col items-center">
      {!preview ? (
                <>
                  <video ref={videoRef} autoPlay className="rounded-lg border-2 border-gray-300 w-full max-w-sm shadow-sm" />
                  <div className="mt-3 flex gap-3 flex-wrap">
                    <button
                      onClick={startCamera}
                      className="bg-secondary text-white py-2 px-4 rounded-lg flex items-center gap-2 hover:bg-primary transition"
                    >
                      <Camera className="w-4 h-4" /> Iniciar cámara
                    </button>
                    <button
                      onClick={revertCamera}
                      className="bg-primary text-white py-2 px-4 rounded-lg flex items-center gap-2 hover:bg-secondary transition"
                    >
                      <Repeat className="w-4 h-4" /> Revertir cámara
                    </button>
                    <button
                      onClick={mode === "single" ? handleSingle : handleBurst}
                      disabled={loadingBurst}
                      className={`${
                        loadingBurst ? "opacity-60" : ""
                      } bg-primary text-white py-2 px-4 rounded-lg flex items-center gap-2 hover:bg-secondary transition`}
                    >
                      {mode === "single" ? (
                        <>
                          <CheckCircle className="w-4 h-4" /> Capturar
                        </>
                      ) : (
                        <>
                          <Zap className="w-4 h-4" /> Ráfaga (3 fotos)
                        </>
                      )}
                    </button>
                  </div>
                </>
              ) : Array.isArray(preview) ? (
                <div className="text-center flex gap-2">
                  {preview.map((src, idx) => (
                    <img
                      key={idx}
                      src={src}
                      alt={`Captura ${idx + 1}`}
                      className="rounded-lg border shadow-md w-full max-w-[120px]"
                    />
                  ))}
                  <p className="text-sm text-gray-600 mt-2 w-full">Ráfaga capturada ✔️</p>
                </div>
              ) : (
                <div className="text-center">
                  <img src={preview} alt="Captura previa" className="rounded-lg border shadow-md w-full max-w-sm" />
                  <p className="text-sm text-gray-600 mt-2">Foto capturada ✔️</p>
                </div>
              )}
            </div>
          );
        }

const CameraCapture = forwardRef(CameraCaptureComponent);
export default CameraCapture;
