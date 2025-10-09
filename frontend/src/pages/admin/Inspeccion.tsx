import React, { useState, useRef } from "react";
import CameraCapture from "../../components/CameraCapture";
import axios from "axios";
import {
  Camera,
  Send,
  RefreshCcw,
  ClipboardList,
  Trash2,
  Zap,
} from "lucide-react";

function Inspeccion() {
  const [inspector, setInspector] = useState("");
  const [contenedor, setContenedor] = useState("");
  const [temperatura, setTemperatura] = useState("");
  const [sello, setSello] = useState("");
  const [foto, setFoto] = useState<File | File[] | null>(null);
  const [modo, setModo] = useState<"single" | "burst">("single");
  const [list, setList] = useState<any[]>([]);
  const cameraRef = useRef<{ restart: () => void } | null>(null);

  const loadAll = async () => {
    const res = await axios.get("http://localhost:4000/api/inspecciones");
    setList(res.data);
  };

  const eliminarEvidencia = async (id: string) => {
    if (!window.confirm("¿Eliminar evidencia completamente?")) return;
    await axios.delete(`http://localhost:4000/api/evidencias/${id}`);
    loadAll();
  };

  const enviar = async () => {
    if (!foto) return alert("Capture una foto primero");
    if (!inspector.trim() || !contenedor.trim() || !temperatura.trim() || !sello.trim()) {
      return alert("Todos los campos son obligatorios");
    }
    const fd = new FormData();
    fd.append("inspector", inspector);
    fd.append("contenedor", contenedor);
    fd.append("temperatura", temperatura);
    fd.append("sello", sello);
    if (Array.isArray(foto)) {
      (foto as File[]).forEach((f, idx) =>
        fd.append("foto", f, `foto${idx + 1}.jpg`)
      );
    } else {
      fd.append("foto", foto as File);
    }
    await axios.post("http://localhost:4000/api/inspecciones", fd);
    alert("Inspección enviada con éxito 🚀");
    setInspector("");
    setContenedor("");
    setTemperatura("");
    setSello("");
    setFoto(null);
    cameraRef.current?.restart();
    loadAll();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100 p-6 md:p-10 fade-in">
      {/* Título principal */}
      <header className="flex items-center gap-3 mb-10">
        <ClipboardList className="text-blue-700 w-8 h-8" />
        <h1 className="text-3xl font-bold text-blue-800">Registro de Inspección</h1>
      </header>

      {/* Contenido principal */}
      <div className="grid lg:grid-cols-2 gap-10">
        {/* 📸 Captura de evidencia */}
        <div className="bg-white border rounded-2xl shadow-lg p-6 hover:shadow-xl transition-all">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2 text-blue-700">
            <Camera className="w-6 h-6" /> Captura de evidencia
          </h2>

          {/* Botones modo */}
          <div className="flex gap-2 mb-4">
            <button
              className={`flex items-center gap-1 py-1.5 px-4 rounded-lg text-sm font-medium border transition ${
                modo === "single"
                  ? "bg-blue-600 text-white shadow"
                  : "bg-gray-100 text-blue-700 hover:bg-blue-50"
              }`}
              onClick={() => setModo("single")}
            >
              Foto individual
            </button>
            <button
              className={`flex items-center gap-1 py-1.5 px-4 rounded-lg text-sm font-medium border transition ${
                modo === "burst"
                  ? "bg-blue-600 text-white shadow"
                  : "bg-gray-100 text-blue-700 hover:bg-blue-50"
              }`}
              onClick={() => setModo("burst")}
            >
              <Zap className="w-4 h-4" /> Ráfaga (3)
            </button>
          </div>

          {/* Cámara */}
          <div className="rounded-xl overflow-hidden border">
            <CameraCapture ref={cameraRef} onCapture={(f) => setFoto(f)} mode={modo} />
          </div>

          {/* Campos */}
          <div className="mt-6 space-y-4">
            <input
              placeholder="Nombre del inspector"
              className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-blue-400"
              value={inspector}
              onChange={(e) => setInspector(e.target.value)}
              required
            />
            <input
              placeholder="Código de contenedor"
              className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-blue-400"
              value={contenedor}
              onChange={(e) => setContenedor(e.target.value)}
              required
            />
            <input
              placeholder="Temperatura (°C)"
              className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-blue-400"
              value={temperatura}
              onChange={(e) => setTemperatura(e.target.value)}
              required
            />
            <input
              placeholder="Sello"
              className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-blue-400"
              value={sello}
              onChange={(e) => setSello(e.target.value)}
              required
            />
            <button
              onClick={enviar}
              className="w-full bg-blue-600 text-white py-2.5 rounded-lg hover:bg-blue-700 transition flex items-center justify-center gap-2 font-medium"
            >
              <Send className="w-4 h-4" /> Enviar inspección
            </button>
          </div>
        </div>

        {/* 📋 Lista de inspecciones */}
        <div className="bg-white border rounded-2xl shadow-lg p-6 hover:shadow-xl transition-all">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold flex items-center gap-2 text-blue-700">
              <ClipboardList className="w-6 h-6" /> Inspecciones registradas
            </h2>
            <button
              onClick={loadAll}
              className="text-blue-600 hover:text-blue-800 flex items-center gap-1 text-sm font-medium"
            >
              <RefreshCcw className="w-4 h-4" /> Actualizar
            </button>
          </div>

          {list.length === 0 ? (
            <p className="text-gray-500 text-sm italic text-center py-6">
              No hay inspecciones registradas todavía.
            </p>
          ) : (
            <ul className="space-y-3 max-h-[450px] overflow-y-auto pr-2">
              {list.map((i) => (
                <li
                  key={i.id}
                  className="border rounded-xl p-4 bg-gray-50 hover:bg-gray-100 transition"
                >
                  <p className="font-semibold text-blue-800">{i.inspector}</p>
                  <p className="text-sm text-gray-600">
                    Contenedor: <span className="font-medium">{i.contenedor}</span>
                  </p>

                  {i.evidencias.map((e: any) => (
                    <div
                      key={e.id}
                      className="mt-2 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1 border-t pt-2"
                    >
                      <div className="flex flex-wrap items-center gap-2 text-sm">
                        <a
                          target="_blank"
                          href={`http://localhost:4000/uploads/${e.rutaArchivo}`}
                          className="text-blue-600 hover:underline font-medium"
                        >
                          Ver foto
                        </a>
                        <span className="text-gray-500 text-xs break-all">
                          Hash: {e.hash}
                        </span>
                      </div>
                      <button
                        onClick={() => eliminarEvidencia(e.id)}
                        className="text-red-500 hover:text-red-700 transition p-1"
                        title="Eliminar evidencia"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  ))}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}

export default Inspeccion;
