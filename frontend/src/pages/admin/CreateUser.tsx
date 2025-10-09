import { useState } from "react";

export default function CreateUser() {
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("INSPECTOR");
  const [password, setPassword] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    alert(`Usuario creado:
Email: ${email}
Rol: ${role}
Contraseña: ${password || "(temporal generada)"}`);
  };

  return (
    <div className="max-w-lg mx-auto mt-10 bg-white p-8 rounded-2xl shadow-lg fade-in">
      <h1 className="text-2xl font-bold text-blue-700 mb-6 text-center">
        Crear nuevo usuario
      </h1>

      <form onSubmit={handleSubmit} className="space-y-5">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Correo electrónico
          </label>
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full border p-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
            placeholder="usuario@empresa.cl"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Rol
          </label>
          <select
            value={role}
            onChange={(e) => setRole(e.target.value)}
            className="w-full border p-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
          >
            <option value="INSPECTOR">INSPECTOR</option>
            <option value="GERENCIA">GERENCIA</option>
            <option value="ADMIN">ADMIN</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Contraseña (opcional)
          </label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full border p-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
            placeholder="Dejar vacío para generar una temporal"
          />
        </div>

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition"
        >
          Crear usuario
        </button>
      </form>
    </div>
  );
}
