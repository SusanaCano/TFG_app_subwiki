//src/features/kegg/components/KeggPathwayListFetcher.tsx

/**
 * @file KeggPathwayListFetcher.tsx
 * @description Componente de React (Next.js 'use client') que obtiene una lista de rutas
 *              metabólicas de KEGG asociadas a un identificador de gen y las pasa al
 *              componente `KeggPathwayListDisplay` para su visualización.
 *
 * Funcionalidad Principal:
 * - Determina el `effectiveGenId` a utilizar para la búsqueda:
 *   - Prioriza `selectedGen.keggGeneId` del `GenContext` (obtenido vía `useSelectedGen`).
 *   - Si no está disponible, utiliza `searchQuery` del `SearchQueryContext` (obtenido vía `useSearchQuery`).
 * - Gestiona estados internos para `pathwayData` (datos de rutas), `isLoading` (estado de carga),
 *   `error` (mensajes de error) y `currentFetchedId` (para evitar recargas innecesarias).
 * - Cuando `effectiveGenId` cambia (o al montar si existe):
 *   - Si no hay `effectiveGenId`, limpia los datos y el estado de error.
 *   - Si el `effectiveGenId` ya ha sido cargado o está en proceso, evita una nueva petición.
 *   - Realiza una petición `fetch` al endpoint `/api/kegg/pathways_for_gene/[effectiveGenId]`
 *     para obtener los datos (`KeggGeneWithpathways`). Esta petición tiene un "debounce" (300ms).
 *   - Valida la estructura de la respuesta de la API.
 *   - Actualiza `pathwayData` con los resultados o `error` si la petición falla.
 * - Lógica de Renderizado:
 *   - Muestra un mensaje inicial si no se ha proporcionado ningún gen para buscar.
 *   - Muestra un indicador de carga ("Cargando lista de rutas...") durante la obtención de datos.
 *   - Muestra un `ErrorMessage` si ocurre un error.
 *   - Muestra un mensaje si no se encontraron rutas KEGG para el gen especificado.
 *   - Si los datos (`pathwayData.pathways`) se obtienen correctamente:
 *     - Muestra un título con el nombre/ID del gen.
 *     - Si se usó un `genIdFromContext` diferente al `searchQuery` global, muestra un botón
 *       para "volver" a los resultados del `searchQuery` (limpiando `selectedGen` en `GenContext`).
 *     - Muestra la definición del gen si está disponible (`pathwayData.geneDefinition`).
 *     - Renderiza `KeggPathwayListDisplay`, pasándole `pathwayData.pathways`.
 *   - Muestra un mensaje si la búsqueda ha sido limpiada después de tener resultados.
 *
 * Este componente actúa como un controlador que maneja la lógica de selección de ID de gen,
 * obtención de datos de rutas y los estados asociados, delegando la visualización
 * de la lista al componente `KeggPathwayListDisplay`.
 */

'use client';

import React, { useEffect, useState } from 'react';
import { useSelectedGen } from '../context/GenContext';
import { useSearchQuery } from '@/features/uniprot/context/SearchQueryContext';
import KeggPathwayListDisplay from './keggPathwayListDisplay';
import { KeggGeneWithpathways, KeggPathwayEntry } from '../types/keggTypes';
import ErrorMessage from '@/components/ErrorMessage';

const KeggPathwayListFetcher: React.FC = () => {
    

    const { selectedGen, setSelectedGen } = useSelectedGen();

    const { searchQuery } = useSearchQuery();

    const genIdFromContext = selectedGen.keggGeneId;

    const effectiveGenId = genIdFromContext || (searchQuery && searchQuery.trim() !== "" ? searchQuery.trim() : null);
    
    const [pathwayData, setPathwayData] = useState<KeggGeneWithpathways | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [currentFetchedId, setCurrentFetchedId] = useState<string | null>(null);
    
    useEffect(() => {
        if (!effectiveGenId) {
            setPathwayData(null);
            setError(null);
            setIsLoading(false);
            setCurrentFetchedId(null);
            // console.log("[KeggPathwayListFetcher] No effectiveGenId, clearing data.");
            
            if (!currentFetchedId && effectiveGenId === null) setCurrentFetchedId(null); 

            return;
        }
        
        if (effectiveGenId === currentFetchedId && (pathwayData || isLoading)) {
            // console.log(`[KeggPathwayListFetcher] Data for ${effectiveGenId} already fetched or loading. Skipping.`);
            return;
        }
        
        if (effectiveGenId !== currentFetchedId) {
            setPathwayData(null); // Limpiar datos de un gen anterior si el ID es nuevo
            setError(null);
        }

 
        const fetchData = async () => {
            setIsLoading(true);
          
            try {
                const response = await fetch(`/api/kegg/pathways_for_gene/${encodeURIComponent(effectiveGenId)}`);
    
                if (!response.ok) {
                    let errorMessage = `Error ${response.status}`;
                    try {
                        const errData = await response.json();
                        errorMessage = `${errorMessage}: ${errData.detail || errData.error || 'Failed to fetch pathway list'}`;
                    } catch (e) { /* no-op */ }
                    throw new Error(errorMessage);
                }

                const result: KeggGeneWithpathways = await response.json();
            
                if (!result || !result.pathways || !Array.isArray(result.pathways)) {
                    setPathwayData(null);
                    setError(`No se encontraron pathways para ${effectiveGenId} o la respuesta es inválida.`);
                } else {
                    setPathwayData(result);
                }
                setCurrentFetchedId(effectiveGenId);
            } catch (err) {
                const message = err instanceof Error ? err.message : "Error desconocido obteniendo lista de pathways.";
                setError(message);
                setPathwayData(null);
                setCurrentFetchedId(effectiveGenId); 
            } finally {
                setIsLoading(false);
            }
        };

        const timer = setTimeout(fetchData, 300);
        return () => clearTimeout(timer);


    }, [effectiveGenId, currentFetchedId]);

    

    if (!effectiveGenId && !currentFetchedId) {
        return <p className="text-sm text-gray-500 mt-2">Busca un gen o selecciona uno de la tabla para ver sus rutas KEGG asociadas.</p>;
    }   

    if (isLoading && effectiveGenId) { 
        return <p className="mt-2">Cargando lista de rutas KEGG para "{effectiveGenId}"...</p>;
    }

    if (error && (effectiveGenId === currentFetchedId || (!effectiveGenId && currentFetchedId) )) { 
        const idForErrorMessage = currentFetchedId || 'el gen';
        return <ErrorMessage message={`Error obteniendo rutas para "${idForErrorMessage}": ${error}`} />;
    }

    if ((!pathwayData || pathwayData.pathways.length === 0) && currentFetchedId === effectiveGenId && !isLoading && !error) {
        let noResultsFor = effectiveGenId;
        
        if (selectedGen.keggGeneId && selectedGen.keggGeneId === effectiveGenId && selectedGen.displayName) {
            noResultsFor = `el gen seleccionado (${selectedGen.displayName})`;
        } else if (selectedGen.userInput && selectedGen.userInput === effectiveGenId && selectedGen.displayName) {
            noResultsFor = `el gen seleccionado (${selectedGen.displayName})`;
        } else if (searchQuery && searchQuery === effectiveGenId) {
            noResultsFor = `"${searchQuery}"`;
        }
        return <p className="mt-2">No se encontraron rutas KEGG asociadas a {noResultsFor}.</p>;
    }

    if (pathwayData && pathwayData.pathways.length > 0 && currentFetchedId === effectiveGenId && !isLoading && !error) {
        
        let displayTitle = pathwayData.geneId; // Fallback al ID devuelto por la API
        if (selectedGen.displayName) {
            if (selectedGen.keggGeneId === pathwayData.geneId || selectedGen.userInput === pathwayData.geneId) {
                displayTitle = selectedGen.displayName;
            }
        }
        
        return (
            <div className="mt-6">
                <h3 className="text-lg font-semibold mb-2">
                    Rutas Metabólicas KEGG para: <span className="font-mono">{displayTitle}</span>
                    {pathwayData.geneName && pathwayData.geneName !== displayTitle && ` (${pathwayData.geneName})`}
                </h3>

    
                {genIdFromContext && searchQuery && genIdFromContext !== searchQuery && (
                    <button 
                        onClick={() => {
                            setSelectedGen(null); // Limpia el genId del GenContext para volver al searchQuery
                        }} 
                        className="text-xs text-blue-600 hover:underline mb-3 block"
                        title={`Mostrar rutas para el término de búsqueda general: "${searchQuery}"`}
                    >
                        ← Ver rutas para "{searchQuery}"
                    </button>
                )}

                {pathwayData.geneDefinition && <p className="text-sm text-gray-600 mb-3">{pathwayData.geneDefinition}</p>}
            
                <KeggPathwayListDisplay pathways={pathwayData.pathways} />
            </div>
        );
    }

    if (!effectiveGenId && currentFetchedId) {
        return <p className="text-sm text-gray-500 mt-2">La búsqueda ha sido limpiada. Ingresa un nuevo término.</p>;
    }

    return null;
};

export default KeggPathwayListFetcher;
