import React, { useEffect, useState } from "react";
import axios from "../api/axios";
import { Bell } from "lucide-react";
import { Link } from "react-router-dom";

type Notif = {
  id: string;
  title: string;
  message: string;
  link?: string;
  read: boolean;
  created_at: string;
};

const POLL_INTERVAL = 30000; // 30s

const NotificationsBell: React.FC = () => {
  const [open, setOpen] = useState(false);
  const [notifs, setNotifs] = useState<Notif[]>([]);
  const unread = notifs.filter((n) => !n.read).length;

  const load = async () => {
    try {
      const res = await axios.get<Notif[]>("/notifications/");
      setNotifs(res.data || []);
    } catch (err) {
      console.error("Error cargando notificaciones", err);
    }
  };

  useEffect(() => {
    load();
    const id = setInterval(load, POLL_INTERVAL);
    // Refresh notifications when any inspection changes state (dispatched elsewhere)
    const handler = () => {
      load();
    };
    window.addEventListener(
      "inspeccion:estado_cambiado",
      handler as EventListener
    );
    return () => clearInterval(id);
  }, []);

  useEffect(() => {
    const handler = () => load();
    window.addEventListener(
      "inspeccion:estado_cambiado",
      handler as EventListener
    );
    return () =>
      window.removeEventListener(
        "inspeccion:estado_cambiado",
        handler as EventListener
      );
  }, []);

  const markRead = async (id: string) => {
    try {
      await axios.post(`/notifications/${id}/read`);
      setNotifs((prev) =>
        prev.map((n) => (n.id === id ? { ...n, read: true } : n))
      );
    } catch (err) {
      console.error("Error marcando como leída", err);
    }
  };

  return (
    <div className="relative inline-block">
      <button
        onClick={() => setOpen((o) => !o)}
        className="relative p-2 rounded hover:bg-blue-600 transition-colors"
        title="Notificaciones"
      >
        <Bell className="w-5 h-5 text-blue-600 dark:text-blue-300" />
        {unread > 0 && (
          <span className="absolute -top-1 -right-1 inline-flex items-center justify-center px-1.5 py-0.5 text-xs font-bold leading-none text-white bg-red-500 rounded-full">
            {unread}
          </span>
        )}
      </button>

      {open && (
        <div className="absolute right-0 mt-2 w-80 bg-white text-black rounded shadow-lg z-50">
          <div className="p-2 border-b flex items-center justify-between">
            <strong>Notificaciones</strong>
            <button
              className="text-sm text-gray-500"
              onClick={() => setOpen(false)}
            >
              Cerrar
            </button>
          </div>
          <div className="max-h-64 overflow-y-auto">
            {notifs.length === 0 && (
              <div className="p-4 text-sm text-gray-500">
                No hay notificaciones
              </div>
            )}
            {notifs.map((n) => (
              <div
                key={n.id}
                className={`p-3 border-b hover:bg-gray-100 ${
                  n.read ? "opacity-80" : ""
                }`}
              >
                <div className="flex justify-between items-start">
                  <div>
                    <div className="text-sm font-semibold">{n.title}</div>
                    <div className="text-xs text-gray-600">{n.message}</div>
                    <div className="text-xs text-gray-400 mt-1">
                      {new Date(n.created_at).toLocaleString()}
                    </div>
                  </div>
                  <div className="ml-2 flex flex-col items-end">
                    {!n.read && (
                      <button
                        onClick={() => markRead(n.id)}
                        className="text-xs text-blue-600 hover:underline"
                      >
                        Marcar leída
                      </button>
                    )}
                    {n.link && (
                      <Link
                        to={n.link}
                        onClick={() => setOpen(false)}
                        className="text-xs text-gray-600 hover:underline ml-1"
                      >
                        Abrir
                      </Link>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default NotificationsBell;
