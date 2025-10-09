import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./index.css";

// Importa componentes y páginas
import Navbar from "./components/navbar";
import CreateUser from "./pages/admin/CreateUser";
import Inspeccion from "./pages/admin/Inspeccion";
// Si tienes login, puedes importarlo también
import Login from "./pages/admin/CreateUser";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <BrowserRouter>
      {/* Navbar fija arriba */}
      <Navbar />
      {/* Rutas */}
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/admin/inspeccion" element={<Inspeccion />} />
        <Route path="/admin/users/create" element={<CreateUser />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
