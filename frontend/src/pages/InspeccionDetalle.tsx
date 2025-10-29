import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import InspeccionModal from "../components/InspeccionModal";
import { inspeccionesApi } from "../api/inspecciones";
import type { InspeccionDetalle } from "../types";

const InspeccionDetalle: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [inspeccion, setInspeccion] = useState<InspeccionDetalle | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const load = async (ident: number) => {
    try {
      const data = await inspeccionesApi.obtener(ident);
      setInspeccion(data);
    } catch (err) {
      console.error("Error obteniendo inspección", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!id) return;
    const ident = parseInt(id, 10);
    if (isNaN(ident)) {
      navigate("/inspecciones");
      return;
    }
    load(ident);
  }, [id]);

  const handleClose = () => {
    navigate("/inspecciones");
  };

  const handleUpdate = () => {
    // After update, reload the inspection
    if (inspeccion) load(inspeccion.id_inspeccion);
  };

  if (loading) return null;

  return (
    <InspeccionModal
      inspeccion={inspeccion}
      isOpen={true}
      onClose={handleClose}
      onUpdate={handleUpdate}
    />
  );
};

export default InspeccionDetalle;
