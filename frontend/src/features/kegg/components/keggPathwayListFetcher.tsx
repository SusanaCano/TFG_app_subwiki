//src/features/kegg/components/KeggPathwayListFetcher.tsx

/**
 * @file KeggPathwayListFetcher.tsx
 * @description Obtiene el genId (del GenContext o SearchQueryContext),
 * busca la lista de rutas KEGG asociadas y las pasa a KeggPathwayListDisplay.
*/

'use client';

import React, { useEffect, useState } from 'react';
import { useSelectedGen } from '../context/GenContext';
import { useSearchQuery } from '@/contexts/SearchQueryContext';
import KeggPathwayListDisplay from './keggPathwayListDisplay';
import { KeggGeneWithpathways, KeggPathwayEntry } from '../types/keggTypes';
import ErrorMessage from '@/components/ErrorMessage';

const KeggPathwayListFetcher: React.FC = () => {
    //const { genId: genIdFromContext, setGenId } = useGen();
    
    // useSelectedGen devuelve un objeto con `selectedGen` y `setSelectedGen`
    // `selectedGen` es un objeto con `userInput`, `keggGeneId`, etc.
    const { selectedGen, setSelectedGen } = useSelectedGen();

    const { searchQuery } = useSearchQuery();

    const genIdFromContext = selectedGen.keggGeneId;

    // Decidir qué ID usar: el del GenContext tiene prioridad si existe,
    // si no, usa el searchQuery global.
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
            
            // Solo limpiar currentFetchedId si realmente no hay nada que buscar.
            if (!currentFetchedId && effectiveGenId === null) setCurrentFetchedId(null); // Condición ajustada

            return;
        }
        
        if (effectiveGenId === currentFetchedId && (pathwayData || isLoading)) {
            // console.log(`[KeggPathwayListFetcher] Data for ${effectiveGenId} already fetched or loading. Skipping.`);
            return;
        }
        
            // Si el effectiveGenId cambia, pero no es el currentFetchedId, procedemos a buscar
        // y limpiamos los datos anteriores si el ID es diferente al que ya se cargó
        if (effectiveGenId !== currentFetchedId) {
            setPathwayData(null); // Limpiar datos de un gen anterior si el ID es nuevo
            setError(null);
        }

 
        const fetchData = async () => {
            setIsLoading(true);
            // setError(null); // Ya se limpió arriba
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

    if (isLoading && effectiveGenId) { // O effectiveGenId === currentFetchedId
        return <p className="mt-2">Cargando lista de rutas KEGG para "{effectiveGenId}"...</p>;
    }

    if (error && (effectiveGenId === currentFetchedId || (!effectiveGenId && currentFetchedId) )) { // Condición ajustada
        const idForErrorMessage = currentFetchedId || 'el gen';
        return <ErrorMessage message={`Error obteniendo rutas para "${idForErrorMessage}": ${error}`} />;
    }

    if ((!pathwayData || pathwayData.pathways.length === 0) && currentFetchedId === effectiveGenId && !isLoading && !error) {
        let noResultsFor = effectiveGenId;
        // Usar displayName si está disponible y corresponde al ID que no dio resultados
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
        // Determinar el título. Usar displayName si está disponible y relevante.
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
