import { Link, useLocation } from "react-router-dom";
import { useState } from "react";
import { Sun, Moon } from "lucide-react";
import useDarkMode from "../hooks/useDarkMode";

export default function Navbar() {
  const location = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);
  const [darkMode, setDarkMode] = useDarkMode();

  const linkClass = (path: string) =>
    `block px-4 py-2 rounded-lg text-sm font-medium transition ${
      location.pathname === path
        ? "bg-blue-600 text-white"
        : "text-gray-700 dark:text-gray-300 hover:bg-blue-100 dark:hover:bg-gray-700"
    }`;

  return (
    <nav className="bg-white dark:bg-gray-900 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-14 items-center">
          <h1 className="text-xl font-bold text-blue-700 dark:text-blue-400">
            SIDC Panel
          </h1>

          {/* Botón móvil */}
          <button
            onClick={() => setMenuOpen(!menuOpen)}
            className="sm:hidden p-2 text-gray-600 dark:text-gray-300 hover:text-blue-600"
          >
            ☰
          </button>

          {/* Enlaces + botón tema */}
          <div className="hidden sm:flex items-center gap-4">
            <Link to="/admin/inspeccion" className={linkClass("/admin/inspeccion")}>
              Inspección
            </Link>
            <Link to="/admin/users/create" className={linkClass("/admin/users/create")}>
              Crear usuario
            </Link>
          
          </div>
        </div>

        {/* Menú móvil */}
        {menuOpen && (
          <div className="sm:hidden pb-3 space-y-1 fade-in">
            <Link
              to="/admin/inspeccion"
              className={linkClass("/admin/inspeccion")}
              onClick={() => setMenuOpen(false)}
            >
              Inspección
            </Link>
            <Link
              to="/admin/users/create"
              className={linkClass("/admin/users/create")}
              onClick={() => setMenuOpen(false)}
            >
              Crear usuario
            </Link>
            <div className="flex justify-center pt-2">
              
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}
