const express = require('express');
const cors = require('cors');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const crypto = require('crypto');
const { PrismaClient } = require('@prisma/client');
import 'dotenv/config';

const FASTAPI_URL = process.env.FASTAPI_URL;



const prisma = new PrismaClient();
const app = express();
app.use(cors());
app.use(express.json());

const uploadDir = path.join(__dirname, '..', 'uploads');
if (!fs.existsSync(uploadDir)) fs.mkdirSync(uploadDir, { recursive: true });

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, uploadDir);
  },
  filename: function (req, file, cb) {
    const unique = Date.now() + '-' + Math.round(Math.random() * 1e9);
    cb(null, unique + '-' + file.originalname);
  }
});
const upload = multer({ storage });

app.use('/uploads', express.static(uploadDir));

app.post('/api/inspecciones', upload.array('foto', 3), async (req, res) => {
  try {
    const { inspector, contenedor, temperatura, sello, observaciones } = req.body;
    if (!req.files || req.files.length === 0) return res.status(400).json({ error: 'Falta archivo' });
    if (!inspector || !contenedor || !temperatura || !sello)
      return res.status(400).json({ error: 'Campos obligatorios faltantes' });

    const evidenciasData = [];
    for (const file of req.files) {
      const buffer = fs.readFileSync(file.path);
      const hash = crypto.createHash('sha256').update(buffer).digest('hex');
      evidenciasData.push({ hash, rutaArchivo: file.filename });
    }

    const inspeccion = await prisma.inspeccion.create({
      data: {
        inspector,
        contenedor,
        temperatura,
        sello,
        observaciones,
        evidencias: { create: evidenciasData }
      },
      include: { evidencias: true }
    });

    res.json(inspeccion);
  } catch (e) {
    console.error(e);
    res.status(500).json({ error: 'Error interno del servidor' });
  }
});
app.delete('/api/evidencias/:id', async (req, res) => {
  try {
    const evidencia = await prisma.evidencia.findUnique({ where: { id: req.params.id } });
    if (!evidencia) return res.status(404).json({ error: 'No encontrada' });
    const filePath = path.join(uploadDir, evidencia.rutaArchivo);
    if (fs.existsSync(filePath)) fs.unlinkSync(filePath);
    await prisma.evidencia.delete({ where: { id: req.params.id } });
    res.json({ ok: true });
  } catch (e) {
    res.status(500).json({ error: 'Error al eliminar' });
  }
});

app.get('/api/inspecciones', async (req, res) => {
  const data = await prisma.inspeccion.findMany({
    include: { evidencias: true },
    orderBy: { fecha: 'desc' }
  });
  res.json(data);
});

// ===========================
// 💼 HU15 - Crear usuarios (solo ADMIN)
// ===========================
app.post("/api/admin/users", async (req, res) => {
  try {
    const { email, password, role } = req.body;

    // 1. Validar campos
    if (!email || !role) {
      return res.status(400).json({ error: "Faltan campos obligatorios" });
    }

    // 2. Validar formato de email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return res.status(400).json({ error: "Correo electrónico inválido" });
    }

    // 3. Validar roles permitidos
    const rolesValidos = ["ADMIN", "INSPECTOR", "GERENCIA"];
    if (!rolesValidos.includes(role)) {
      return res.status(400).json({ error: "Rol no permitido" });
    }

    // 4. Evitar duplicados (si ya hay Prisma configurado con User)
    const existe = await prisma.usuario.findUnique({
      where: { email: email },
    });
    if (existe) {
      return res.status(409).json({ error: "El correo ya está registrado" });
    }

    // 5. Encriptar o asignar contraseña
    const bcrypt = require("bcrypt");
    const passwordFinal = password || Math.random().toString(36).slice(-10);
    const hash = await bcrypt.hash(passwordFinal, 10);

    // 6. Crear usuario en BD (ajusta el modelo si tu tabla tiene otros nombres)
    const nuevoUsuario = await prisma.usuario.create({
      data: {
        email,
        passwordHash: hash,
        role,
        status: "ACTIVE",
      },
    });

    // 7. Responder al front
    res.status(201).json({
      message: "Usuario creado correctamente",
      user: {
        id: nuevoUsuario.id,
        email: nuevoUsuario.email,
        role: nuevoUsuario.role,
      },
      passwordTemporal: password ? null : passwordFinal,
    });
  } catch (error) {
    console.error("Error al crear usuario:", error);
    res.status(500).json({ error: "Error interno del servidor" });
  }
});


const PORT = process.env.PORT || 4000;
app.listen(PORT, () => console.log('✅ Backend listo en puerto', PORT));
