// src/features/kegg/components/KeggPathwayGraphFetcher.tsx

/**
 * @file KeggPathwayGraphFetcher.tsx
 * @description  Componente de React (Next.js 'use client') encargado de obtener los datos
 *              detallados de un grafo de ruta metabólica de KEGG y pasarlos al componente
 *              `KeggPathwayGraphDisplay` para su renderizado.
 *
 * Funcionalidad:
 * - Consume `pathwayId` y `pathwayName` del `PathwayContext` mediante el hook `usePathway`.
 * - Gestiona estados internos para `graphData` (datos del grafo), `isLoading` (estado de carga),
 *   `error` (mensajes de error) y `currentFetchedPathwayId` (para evitar recargas innecesarias).
 * - Cuando `pathwayId` cambia (o al montar si hay un `pathwayId` inicial):
 *   - Si no hay `pathwayId`, limpia los datos y el estado de error.
 *   - Si el `pathwayId` ya ha sido cargado o está en proceso, evita una nueva petición.
 *   - Realiza una petición `fetch` al endpoint `/api/kegg/pathway_graph/[pathwayId]` para
 *     obtener los datos del grafo (`KeggPathwayGraphData`). Esta petición tiene un
 *     ligero "debounce" (100ms).
 *   - Valida la estructura de la respuesta de la API.
 *   - Actualiza `graphData` con los resultados o `error` si la petición falla.
 * - Lógica de Renderizado:
 *   - Muestra un mensaje inicial si no se ha seleccionado ninguna ruta.
 *   - Muestra un indicador de carga ("Cargando gráfico para...") mientras se obtienen los datos.
 *   - Muestra un `ErrorMessage` si ocurre un error durante la obtención de datos.
 *   - Muestra un mensaje si no se pudo cargar la representación gráfica para una ruta específica.
 *   - Si los datos del grafo (`graphData`) se obtienen correctamente y hay un `pathwayId`,
 *     renderiza el componente `KeggPathwayGraphDisplay`, pasándole `graphData`.
 *
 * Este componente actúa como un controlador que maneja la lógica de obtención de datos y
 * los estados asociados, delegando la visualización del grafo al componente
 * `KeggPathwayGraphDisplay`.
 */

'use client';

import React, { useEffect, useState } from 'react';
import { usePathway } from '../context/PathwayContext';
import KeggPathwayGraphDisplay from './keggPathwayGraphDisplay'; 
import { KeggPathwayGraphData } from '../types/keggTypes';
import ErrorMessage from '@/components/ErrorMessage';

const KeggPathwayGraphFetcher: React.FC = () => {
    const { pathwayId, pathwayName } = usePathway(); 
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
        setGraphData(null); 
        setError(null);
      }
        
        const fetchData = async () => {
          console.log(`[KeggPathwayGraphFetcher] Fetching graph data for pathwayId: ${pathwayId}`);
          setIsLoading(true);
          setError(null);
          
        
          try {
            
            const response = await fetch(`/api/kegg/pathway_graph/${encodeURIComponent(pathwayId)}`);
            

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
        
        const timer = setTimeout(fetchData, 100); // debounce
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
                     
                      Gráfico de la Ruta: {graphData.pathwayName || pathwayName || graphData._id}
                    </h4>

                    <KeggPathwayGraphDisplay graphData={graphData} />
                </div>
            );
        }
    
        return null; 
    };

    export default KeggPathwayGraphFetcher;