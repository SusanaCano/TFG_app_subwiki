// src/features/kegg/components/KeggPathwayGraphFetcher.tsx

/**
 * @file KeggPathwayGraphFetcher.tsx
 * @description Obtiene el pathwayId del PathwayContext, busca los datos del gráfico
 * para ese pathway y los pasa a KeggPathwayGraphDisplay.
*/

'use client';

import React, { useEffect, useState } from 'react';
import { usePathway } from '../context/PathwayContext';
import KeggPathwayGraphDisplay from './keggPathwayGraphDisplay'; // Tu componente que dibuja
import { KeggPathwayGraphData } from '../types/keggTypes';
import ErrorMessage from '@/components/ErrorMessage';

const KeggPathwayGraphFetcher: React.FC = () => {
    const { pathwayId, pathwayName } = usePathway(); // Usa el contexto
    const [graphData, setGraphData] = useState<KeggPathwayGraphData | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [currentFetchedPathwayId, setCurrentFetchedPathwayId] = useState<string | null>(null);

    useEffect(() => {
        if (!pathwayId) {
            setGraphData(null); // Limpia el gráfico si no hay pathway seleccionado
            setError(null);
            setIsLoading(false);
            setCurrentFetchedPathwayId(null);
            // console.log("[KeggPathwayGraphFetcher] No pathwayId, clearing graph data.");
            return;
        }

        if (pathwayId === currentFetchedPathwayId && (graphData || isLoading)) {
            // console.log(`[KeggPathwayGraphFetcher] Graph for ${pathwayId} already fetched or loading. Skipping.`);
            return;
        }

        // Si el pathwayId es nuevo, limpiar datos/errores anteriores
      if (pathwayId !== currentFetchedPathwayId) {
        setGraphData(null); // Limpiar datos de un pathway anterior
        setError(null);
      }
        
        const fetchData = async () => {
          console.log(`[KeggPathwayGraphFetcher] Fetching graph data for pathwayId: ${pathwayId}`);
          setIsLoading(true);
          setError(null);
          
        
          try {
            // Esta API debería devolver nodos, ejes, etc.
            const response = await fetch(`/api/kegg/pathway_graph/${encodeURIComponent(pathwayId)}`);
            //const response = await fetch(`/api/kegg/pathway/graph/${encodeURIComponent(pathwayId)}`);

            if (!response.ok) {
              let errorMessage = `Error ${response.status}`;
              try {
                const errData = await response.json();
                errorMessage = `${errorMessage}: ${errData.detail || errData.error || 'Failed to fetch pathway graph'}`;
              } catch (e) { /* no-op */ }
              throw new Error(errorMessage);
            }
        
            const result: KeggPathwayGraphData = await response.json();
            console.log("[KeggPathwayGraphFetcher] Pathway graph data received:", result);
            
            /** 
            if (!result || !result.nodes || !result.edges || !result.pathwayId) {
              console.error("[KeggPathwayGraphFetcher] Invalid data structure for pathway graph:", result);
            //   throw new Error("Respuesta de API para gráfico de pathway no válida.");
              setGraphData(null);
              setError(`Datos del gráfico para ${pathwayId} inválidos o vacíos.`);
            } else {
                setGraphData(result);
                setError(null);
            }
            */

                        // VALIDACIÓN USANDO LAS CLAVES CORRECTAS DEL TIPO ACTUALIZADO
            if (!result || !result._id || !Array.isArray(result.nodes) || !Array.isArray(result.edges)) {
              console.error("[KeggPathwayGraphFetcher] Invalid data structure. Missing _id, or nodes/edges are not arrays:", result);
              setGraphData(null);
              // Usa pathwayId de la URL para el mensaje de error, y result._id si está disponible
              setError(`Datos del gráfico para la ruta solicitada (${pathwayId}) inválidos o incompletos. API _id: ${result?._id || 'N/A'}`);
            } else {
                setGraphData(result);
                setError(null);
            }

            setCurrentFetchedPathwayId(pathwayId);
        
          } catch (err) {
            const message = err instanceof Error ? err.message : "Error desconocido obteniendo gráfico de pathway.";
            console.error("[KeggPathwayGraphFetcher] Error:", message, err);
            setError(message);
            setGraphData(null);
            setCurrentFetchedPathwayId(pathwayId);
          } finally {
            setIsLoading(false);
          }
        };
        
        const timer = setTimeout(fetchData, 100); // Pequeño debounce
        return () => clearTimeout(timer);

        }, [pathwayId, currentFetchedPathwayId, graphData, isLoading]);
    
        if (!pathwayId && !currentFetchedPathwayId) {
            return <p className="text-sm text-gray-500 mt-4">Selecciona una ruta de la lista de arriba para ver su representación gráfica.</p>;
        }
        
        if (isLoading && pathwayId) {
            return <p className="mt-4">Cargando gráfico para la ruta {pathwayName || pathwayId}...</p>;
        }

        if (error && (pathwayId === currentFetchedPathwayId || !pathwayId)) {
            return <ErrorMessage message={`Error obteniendo gráfico para "${pathwayName || currentFetchedPathwayId || 'la ruta'}": ${error}`} />;
        }
    
        // Si no hay datos del gráfico PERO un pathway fue seleccionado y ya no está cargando ni hay error
        if (!graphData && pathwayId && currentFetchedPathwayId === pathwayId && !isLoading && !error) {
            return <p className="mt-4">No se pudo cargar la representación gráfica para la ruta "{pathwayName || pathwayId}".</p>;
        }

        if (graphData && pathwayId) { // Solo mostrar si hay datos Y un pathwayId
            return (
            
                <div className="mt-6 p-4 border rounded-md shadow">
                    <h4 className="text-md font-semibold mb-3">
                      {/*Gráfico de la Ruta: {graphData.pathwayName || pathwayName || graphData.pathwayId}*/}
                      Gráfico de la Ruta: {graphData.pathwayName || pathwayName || graphData._id}
                    </h4>

                    <KeggPathwayGraphDisplay graphData={graphData} />
                </div>
            );
        }
    
        return null; // O un placeholder si no hay pathwayId pero sí un currentFetched (se deseleccionó)
    };

    export default KeggPathwayGraphFetcher;