import express from "express";
import axios from "axios";

const router = express.Router();

// Cambia esta URL cuando tu compañero te confirme su API
const API_URL = "http://localhost:8000/api"; 

// === HU15: Crear usuario (solo ADMIN) ===
router.post("/admin/users", async (req, res) => {
  try {
    const { email, password, role } = req.body;

    // 1. Validar campos obligatorios
    if (!email || !role) {
      return res.status(400).json({ error: "Faltan campos obligatorios" });
    }

    // 2. Validar formato del correo
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return res.status(400).json({ error: "Correo electrónico no válido" });
    }

    // 3. Validar rol permitido
    const rolesValidos = ["ADMIN", "INSPECTOR", "GERENCIA"];
    if (!rolesValidos.includes(role)) {
      return res.status(400).json({ error: "Rol inválido" });
    }

    // 4. (Pendiente) Consultar API o BD para evitar duplicado
    //    Este bloque se activará cuando tu compañero te entregue su endpoint.
    // try {
    //   const usuarios = await axios.get(`${API_URL}/usuarios`);
    //   const existe = usuarios.data.some((u) => u.email === email);
    //   if (existe) {
    //     return res.status(409).json({ error: "El correo ya está registrado" });
    //   }
    // } catch (err) {
    //   console.warn("⚠️ No se pudo verificar duplicado aún, falta conexión con la API.");
    // }

    // 5. (Pendiente) Enviar al backend FastAPI o BD
    // const response = await axios.post(`${API_URL}/usuarios`, { email, password, role });

    // 6. Por ahora solo confirmamos que la lógica pasa las validaciones
    res.status(200).json({
      message: "Validaciones correctas. Listo para conectar con API real.",
      data: { email, role },
    });

  } catch (error) {
    console.error("Error interno HU15:", error.message);
    res.status(500).json({ error: "Error interno del servidor" });
  }
});

export default router;
