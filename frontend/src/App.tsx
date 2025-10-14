import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import ToastContainer from './components/ToastContainer';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import InspeccionNueva from './pages/InspeccionNueva';
import Inspecciones from './pages/Inspecciones';
import Reportes from './pages/Reportes';
import Admin from './pages/Admin';

function App() {
  return (
    <Router>
      <AuthProvider>
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
              
              {/* Ruta solo para admin */}
              <Route element={<ProtectedRoute requireRole="admin" />}>
                <Route path="admin" element={<Admin />} />
              </Route>
            </Route>
          </Route>
          
          {/* Ruta por defecto */}
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
        <ToastContainer />
      </AuthProvider>
    </Router>
  );
}

export default App;
