import React, { useState } from 'react';
import { Link, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useToast } from './ToastProvider';
import { 
  LayoutDashboard, 
  Plus, 
  FileText, 
  BarChart3, 
  Building, 
  Ship, 
  Users, 
  Settings,
  LogOut,
  Menu,
  X
} from 'lucide-react';

const Layout: React.FC = () => {
  const location = useLocation();
  const { user, logout } = useAuth();
  const { confirm } = useToast();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const isActive = (path: string) => {
    return location.pathname === path ? 'bg-blue-700' : '';
  };

  const handleLogout = async () => {
    const confirmed = await confirm('¿Está seguro que desea cerrar sesión?');
    if (confirmed) {
      logout();
    }
  };

  // Menú basado en roles
  const menuItems = [
    { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard, roles: ['inspector', 'supervisor', 'admin'] },
    { path: '/inspeccion-nueva', label: 'Nueva Inspección', icon: Plus, roles: ['inspector', 'supervisor', 'admin'] },
    { path: '/inspecciones', label: 'Inspecciones', icon: FileText, roles: ['inspector', 'supervisor', 'admin'] },
    { path: '/reportes', label: 'Reportes', icon: BarChart3, roles: ['inspector', 'supervisor', 'admin'] },
    { path: '/plantas', label: 'Plantas', icon: Building, roles: ['supervisor', 'admin'] },
    { path: '/navieras', label: 'Navieras', icon: Ship, roles: ['supervisor', 'admin'] },
    { path: '/usuarios', label: 'Usuarios', icon: Users, roles: ['admin'] },
    { path: '/admin', label: 'Configuración', icon: Settings, roles: ['admin'] },
  ];

  const visibleMenuItems = menuItems.filter(item => 
    user && item.roles.includes(user.rol)
  );

  const closeMobileMenu = () => setMobileMenuOpen(false);

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Mobile Header */}
      <div className="lg:hidden fixed top-0 left-0 right-0 bg-gradient-to-r from-blue-600 to-blue-800 text-white shadow-lg z-30 px-4 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 hover:bg-blue-700 rounded-lg transition-colors"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
            <div>
              <h1 className="text-lg font-bold">Inspección</h1>
              <p className="text-xs text-blue-200">Contenedores</p>
            </div>
          </div>
          <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
            <span className="text-white text-sm font-semibold">
              {user?.nombre?.charAt(0) || 'U'}
            </span>
          </div>
        </div>
      </div>

      {/* Mobile Overlay */}
      {mobileMenuOpen && (
        <div 
          className="lg:hidden fixed inset-0 bg-black/50 z-20"
          onClick={closeMobileMenu}
        />
      )}

      {/* Sidebar - Desktop y Mobile */}
      <div className={`
        fixed inset-y-0 left-0 w-64 bg-gradient-to-b from-blue-600 to-blue-800 text-white shadow-lg z-40
        transform transition-transform duration-300 ease-in-out
        ${mobileMenuOpen ? 'translate-x-0' : '-translate-x-full'}
        lg:translate-x-0
      `}>
        {/* Desktop Header (oculto en mobile) */}
        <div className="hidden lg:block p-6">
          <h1 className="text-2xl font-bold mb-2">Inspección</h1>
          <p className="text-blue-200 text-sm">Contenedores Frutícolas</p>
        </div>

        {/* Mobile Header spacing */}
        <div className="lg:hidden h-16" />

        <nav className="flex-1 overflow-y-auto" style={{ maxHeight: 'calc(100vh - 240px)' }}>
          {visibleMenuItems.map((item) => {
            const Icon = item.icon;
            return (
              <Link
                key={item.path}
                to={item.path}
                onClick={closeMobileMenu}
                className={`flex items-center px-6 py-3 hover:bg-blue-700 transition-colors ${isActive(item.path)}`}
              >
                <Icon className="w-5 h-5 mr-3" />
                <span className="text-sm sm:text-base">{item.label}</span>
              </Link>
            );
          })}
        </nav>

        <div className="absolute bottom-0 left-0 right-0 bg-blue-900 bg-opacity-50">
          <div className="p-4 sm:p-6">
            <div className="flex items-center mb-3">
              <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center flex-shrink-0">
                <span className="text-white font-semibold">
                  {user?.nombre?.charAt(0) || 'U'}
                </span>
              </div>
              <div className="ml-3 flex-1 min-w-0">
                <p className="text-sm font-medium truncate">{user?.nombre || 'Usuario'}</p>
                <p className="text-xs text-blue-200 capitalize">{user?.rol || 'inspector'}</p>
              </div>
            </div>
            <button
              onClick={handleLogout}
              className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg transition-colors text-sm font-medium"
            >
              <LogOut className="w-4 h-4" />
              Cerrar Sesión
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="pt-16 lg:pt-0 lg:ml-64 p-4 sm:p-6 lg:p-8">
        <Outlet />
      </div>
    </div>
  );
};

export default Layout;
