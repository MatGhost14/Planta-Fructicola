import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useEffect } from 'react';
import { AuthProvider } from './contexts/AuthContext';
import { ToastProvider } from './components/ToastProvider';
import { useStore } from './store';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import InspeccionNueva from './pages/InspeccionNueva';
import Inspecciones from './pages/Inspecciones';
import Reportes from './pages/Reportes';
import Admin from './pages/Admin';
import Usuarios from './pages/Usuarios';
import Plantas from './pages/Plantas';
import Navieras from './pages/Navieras';
import Configuracion from './pages/Configuracion';

function AppContent() {
  const { theme } = useStore();

  // Aplicar tema al cargar
  useEffect(() => {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [theme]);

  return (
    <Routes>
      {/* Ruta pública: Login */}
      <Route path="/login" element={<Login />} />
      
      {/* Rutas protegidas */}
      <Route element={<ProtectedRoute />}>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="inspeccion-nueva" element={<InspeccionNueva />} />
          <Route path="inspecciones" element={<Inspecciones />} />
          <Route path="reportes" element={<Reportes />} />
          <Route path="configuracion" element={<Configuracion />} />
          
          {/* Rutas para supervisor/admin */}
          <Route element={<ProtectedRoute requireRole={['supervisor', 'admin']} />}>
            <Route path="plantas" element={<Plantas />} />
            <Route path="navieras" element={<Navieras />} />
          </Route>
          
          {/* Rutas solo para admin */}
          <Route element={<ProtectedRoute requireRole="admin" />}>
            <Route path="admin" element={<Admin />} />
            <Route path="usuarios" element={<Usuarios />} />
          </Route>
        </Route>
      </Route>
      
      {/* Ruta por defecto */}
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <ToastProvider>
          <AppContent />
        </ToastProvider>
      </AuthProvider>
    </Router>
  );
}

export default App;
