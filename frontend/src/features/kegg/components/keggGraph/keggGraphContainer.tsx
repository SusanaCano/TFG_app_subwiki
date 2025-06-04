// src/app/features/kegg/components/keggGraph/keggGraphContainer.tsx

/**
 * @file keggGraphContainer.tsx
 * @description Componente contenedor de React (Next.js 'use client') para `KeggGraph`.
 *              Es responsable de obtener los datos de las rutas metabólicas de KEGG
 *              asociadas a un `genId` específico y luego pasar estos datos al
 *              componente de presentación `KeggGraph`.
 *
 * Props:
 * - `genId` (string): El identificador del gen para el cual se deben obtener
 *                     los datos de las rutas metabólicas.
 *
 * Funcionalidad:
 * - Utiliza `useEffect` para iniciar la carga de datos cuando el componente
 *   se monta o cuando la prop `genId` cambia.
 * - Realiza una petición `fetch` al endpoint `/api/kegg/pathways_for_gene/[genId]`
 *   para obtener los datos.
 * - Gestiona estados internos para `data` (de tipo `KeggData | null`) y `loading` (booleano).
 * - Muestra un mensaje "Cargando datos..." durante la carga.
 * - Muestra un mensaje "No se encontraron datos." si no se obtienen datos después de la carga
 *   o si la petición no fue exitosa y `data` permanece `null`.
 * - Si la carga es exitosa y se reciben datos, renderiza el componente `KeggGraph`,
 *   pasándole los `data` (de tipo `KeggData`) obtenidos.
 */

'use client';

import React, { useEffect, useState } from "react";
import KeggGraph from "./keggGraph";
import { KeggData } from "./types";


interface Props {
  genId: string;
}

export function KeggGraphContainer({ genId }: Props) {
  const [data, setData] = useState<KeggData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch(`/api/kegg/pathways_for_gene/${genId}`);
        const result = await res.json();
        setData(result);
      } catch (err) {
        console.error('Error al cargar datos:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [genId]);

  if (loading) return <p>Cargando datos...</p>;
  if (!data) return <p>No se encontraron datos.</p>;

  return <KeggGraph data={data} />;
}


export default KeggGraphContainer;
