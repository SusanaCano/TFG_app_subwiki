// src/features/kegg/components/keggGraph/keggGraph.tsx

/**
 * @file keggGraph.tsx
 * @description Componente de React (`KeggGraph`) encargado de mostrar una vista previa
 *              o un enlace a una ruta metabólica de KEGG para un gen específico.
 *
 * Props:
 * - `data` (KeggData): Un objeto que contiene la información necesaria, principalmente
 *                      `genId`, para identificar la ruta metabólica.
 *
 * Funcionalidad:
 * - Muestra un encabezado indicando la ruta metabólica del `genId` proporcionado.
 * - Renderiza un enlace (usando `next/link`) que dirige al usuario a una página
 *   dedicada para visualizar la ruta metabólica completa de ese `genId`.
 *   (`/app/api/kegg/[genId]`).
 *
 * Este componente sirve como un punto de entrada para la visualización
 * más detallada de la ruta metabólica.
 */

import React from "react";
import { KeggData } from "./types"; 
import Link from 'next/link';

interface KeggGraphProps {
  data: KeggData;
}

const KeggGraph: React.FC<KeggGraphProps> = ({ data }) => {
  return (
    <div>
      <h3>Ruta Metabólica de {data.genId}</h3>
   
      <Link href={`/features/kegg/${data.genId}`}>
         Ver ruta metabólica
      </Link>
    </div>
  );
};

export default KeggGraph;

