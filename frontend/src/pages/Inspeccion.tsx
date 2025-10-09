import React, { useState, useRef } from "react";
import CameraCapture from "../components/CameraCapture";
import axios from "axios";
import { Camera, Send, RefreshCcw, ClipboardList, Trash2, Zap, Repeat } from "lucide-react";

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
      (foto as File[]).forEach((f, idx) => fd.append("foto", f, `foto${idx + 1}.jpg`));
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
    <div className="min-h-screen bg-background p-8">
      <header className="flex items-center gap-3 mb-8 border-b pb-4">
        <ClipboardList className="text-primary w-8 h-8" />
        <h1 className="text-2xl font-bold text-primary">Registro de Inspección</h1>
      </header>

      <div className="grid md:grid-cols-2 gap-8">
        <div className="bg-white shadow-md rounded-2xl p-6 border">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2 text-secondary">
            <Camera className="w-5 h-5" /> Captura de evidencia
          </h2>
          <div className="mb-3 flex gap-2">
            <button
              className={`py-1 px-3 rounded-lg border ${modo === "single" ? "bg-primary text-white" : "bg-background text-primary"}`}
              onClick={() => setModo("single")}
            >
              Foto individual
            </button>
            <button
              className={`py-1 px-3 rounded-lg border ${modo === "burst" ? "bg-primary text-white" : "bg-background text-primary"} flex items-center gap-1`}
              onClick={() => setModo("burst")}
            >
              <Zap className="w-4 h-4" /> Ráfaga (3)
            </button>
          </div>
          <CameraCapture ref={cameraRef} onCapture={(f) => setFoto(f)} mode={modo} />
          <div className="mt-4 flex flex-col gap-3">
            <input
              placeholder="Nombre del inspector"
              className="border rounded-lg p-2 w-full focus:outline-primary"
              value={inspector}
              onChange={(e) => setInspector(e.target.value)}
              required
            />
            <input
              placeholder="Código de contenedor"
              className="border rounded-lg p-2 w-full focus:outline-primary"
              value={contenedor}
              onChange={(e) => setContenedor(e.target.value)}
              required
            />
            <input
              placeholder="Temperatura (°C)"
              className="border rounded-lg p-2 w-full focus:outline-primary"
              value={temperatura}
              onChange={(e) => setTemperatura(e.target.value)}
              required
            />
            <input
              placeholder="Sello"
              className="border rounded-lg p-2 w-full focus:outline-primary"
              value={sello}
              onChange={(e) => setSello(e.target.value)}
              required
            />
            <button
              onClick={enviar}
              className="bg-primary text-white py-2 px-4 rounded-lg flex items-center justify-center gap-2 hover:bg-secondary transition"
            >
              <Send className="w-4 h-4" /> Enviar inspección
            </button>
          </div>
        </div>

        <div className="bg-white shadow-md rounded-2xl p-6 border">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold flex items-center gap-2 text-secondary">
              <ClipboardList className="w-5 h-5" /> Inspecciones registradas
            </h2>
            <button
              onClick={loadAll}
              className="text-primary hover:text-secondary flex items-center gap-1 transition"
            >
              <RefreshCcw className="w-4 h-4" /> Actualizar
            </button>
          </div>
          <ul className="space-y-3 max-h-[450px] overflow-y-auto">
            {list.map((i) => (
              <li key={i.id} className="border rounded-lg p-3 shadow-sm">
                <p className="font-medium">{i.inspector}</p>
                <p className="text-sm text-gray-600">Contenedor: {i.contenedor}</p>
                {i.evidencias.map((e: any) => (
                  <div key={e.id} className="mt-2 flex items-center gap-2">
                    <a
                      target="_blank"
                      href={`http://localhost:4000/uploads/${e.rutaArchivo}`}
                      className="text-primary underline text-sm"
                    >
                      Ver foto
                    </a>
                    <p className="text-xs text-gray-500 break-all">Hash: {e.hash}</p>
                    <button
                      onClick={() => eliminarEvidencia(e.id)}
                      className="text-red-500 hover:text-red-700"
                      title="Eliminar evidencia"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                ))}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );

}

export default Inspeccion;
