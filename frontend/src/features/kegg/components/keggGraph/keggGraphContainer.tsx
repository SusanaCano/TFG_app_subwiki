// src/app/features/kegg/components/keggGraph/keggGraphContainer.tsx
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
/**
interface KeggGraphContainerProps {
  genId: string;
}

const KeggGraphContainer: React.FC<KeggGraphContainerProps> = ({ genId }) => {
  const [data, setData] = useState<KeggData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        // Cambio: La ruta ahora usa el campo 'entry' en lugar de 'genId'
        const response = await fetch(`/api/kegg/${genId}`);  // El 'genId' se pasa en la URL
        
        if (!response.ok) {
          const errorText = await response.text(); // Obtén el texto de error si es posible
          //throw new Error("Ruta metabólica no encontrada");
          throw new Error(`Error en la API: ${errorText}`);
        }

        const result: KeggData = await response.json();
        console.log("Datos recibidos:", result);  
        setData(result);
      }catch (error) {
        setError(error instanceof Error ? error.message : "Error desconocido");
      } finally {
        setLoading(false);
      }
    };

    if (genId) { 
      fetchData();
    }
  }, [genId]);

  if (loading) {
    return <p>Cargando datos...</p>;
  }

    // Si hay un error, mostramos el mensaje de error
    if (error) {
      return <p>Error: {error}</p>;
    }
    
  return (
    <div>
      {data ? <KeggGraph data={data} /> : <p>Cargando datos...</p>}
    </div>
  );
};

export default KeggGraphContainer;
 */

/*
import React from 'react';
import { GraphData } from './types';  // Asumimos que tienes tipos definidos en types.ts

interface Props {
  data: GraphData;
}

const KeggGraphContainer = ({ data }: Props) => {
  // Usa la variable 'data' de alguna manera, por ejemplo:
  return (
    <div>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
};
*/
export default KeggGraphContainer;
