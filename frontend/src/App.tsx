import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import ToastContainer from './components/ToastContainer';
import Dashboard from './pages/Dashboard';
import InspeccionNueva from './pages/InspeccionNueva';
import Inspecciones from './pages/Inspecciones';
import Reportes from './pages/Reportes';
import Admin from './pages/Admin';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="inspeccion-nueva" element={<InspeccionNueva />} />
          <Route path="inspecciones" element={<Inspecciones />} />
          <Route path="reportes" element={<Reportes />} />
          <Route path="admin" element={<Admin />} />
        </Route>
      </Routes>
      <ToastContainer />
    </Router>
  );
}

export default App;
