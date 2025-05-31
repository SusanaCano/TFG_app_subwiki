// src/features/uniprot/components/GenesSearchPage.tsx
/**
 * @file GenesSearchPage.tsx
 * @description Componente encargado de mostrar los resultados de búsqueda de genes.
 * 
 * Funcionalidad:
 * - Utiliza el hook `useSearchQuery` para obtener el término de búsqueda (`searchQuery`)
 *   actual del contexto global (`SearchQueryContext`).
 * - Cuando `searchQuery` cambia y tiene un valor:
 *   - Activa un estado de carga (`isLoading`).
 *   - Realiza una petición asíncrona (`fetchGenes`) al endpoint del backend 
 *     (ej. `http://localhost:8000/buscar?query=...`) para obtener datos de genes.
 *   - Maneja la respuesta del backend:
 *     - Si es exitosa y los datos son válidos (espera un formato como `{"result": [...]}`),
 *       actualiza el estado `genes` para mostrarlos.
 *     - Si hay un error en la petición o la respuesta no es válida, actualiza el estado `error`.
 * - Muestra diferentes UI según el estado:
 *   - Indicador de carga (`isLoading`).
 *   - Mensaje de error (`error`).
 *   - Tabla de genes (`GenesTable`) si hay resultados (`genes.length > 0`).
 *   - Mensaje de "No se encontraron resultados" si la búsqueda se realizó pero no hubo coincidencias.
 *   - Mensaje para introducir un término si la búsqueda está vacía.
 * - Utiliza `useEffect` para reaccionar a los cambios en `searchQuery` y disparar `fetchGenes`.
 * - Incluye un pequeño debounce en `useEffect` para evitar múltiples llamadas rápidas a la API.
 */
/**
 * Componente que muestra en una tabla los datos de genes obtenidos de la QUERY GLOBAL.
 * Realiza una consulta al backend usando "_id", "primaryAccession" o "orderedLocusNames"
 * basados en la query global.
 * GeneEntry estructura de los datos que se reciben.
 * Muestra los resultados en una tabla usando el componente "GenesTable".
 * Con errores y excepciones si los datos recibidos son incorrectos o no se obtuvieron datos.
 */

'use client'

import React, { useState, useEffect, useCallback } from 'react';
import GenesTable from '@/components/GenesTable';
import ErrorMessage from '@/components/ErrorMessage';
import { GeneEntry } from '../types/geneTypes';
import { useSearchQuery } from '@/contexts/SearchQueryContext';

const GenesSearchPage = () => {
    // El estado 'query' y 'setQuery' ahora vienen del contexto global
  const { searchQuery } = useSearchQuery();
  //const [query, setQuery] = useState('');
  //const [genes, setGenes] = useState<Gene[]>([]);
  const [genes, setGenes] = useState<GeneEntry[]>([]); 
  const [error, setError] = useState<string | null>(null);
  
  //const [hasSearched, setHasSearched] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  
  const fetchGenes = useCallback(async () => {
    //setHasSearched(true); 
    console.log(`[GenesSearchPage] fetchGenes: Called. Current searchQuery: "${searchQuery}"`);

      // Si no hay searchQuery, no hacemos nada o limpiamos resultados
    if (!searchQuery || searchQuery.trim() === "") {
      console.log("[GenesSearchPage] fetchGenes: searchQuery is empty, clearing results and returning.");
      setGenes([]);
      setError(null);
      setIsLoading(false);
      return;
    }

        //  Log indicando que se va a proceder con el fetch
    console.log(`[GenesSearchPage] fetchGenes: searchQuery is "${searchQuery}", proceeding to fetch.`);
    
    setIsLoading(true);
    setError(null); // Limpiar error anterior al iniciar una nueva búsqueda
    
    try {
      
      //const response = await fetch(`http://localhost:8000/buscar?query=${query}`);
      const response = await fetch(`http://localhost:8000/buscar?query=${encodeURIComponent(searchQuery)}`);

            // 3. Log del estado de la respuesta
      console.log("[GenesSearchPage] fetchGenes: Backend response status:", response.status, response.statusText);

      if (!response.ok) {
                // Intenta obtener un mensaje de error del backend si es posible
        let errorMessage = 'No se encontraron resultados o hubo un error en el servidor';
        //throw new Error('No se encontraron resultados o hubo un error en el servidor');

        try {
          const errorData = await response.json();
            // Log de los datos del error del backend si la respuesta no fue OK
            console.log("[GenesSearchPage] fetchGenes: Backend error data:", errorData);
            errorMessage = errorData.detail || errorData.error || errorData.message || errorMessage;
        } catch (e) {
          // Si el cuerpo del error no es JSON, el error original de la respuesta es suficiente
          console.warn("[GenesSearchPage] fetchGenes: Could not parse error response JSON.");
        }
        throw new Error(errorMessage);
      }

      const data = await response.json();
      // Log de los datos recibidos del backend (la respuesta JSON completa)
      console.log("[GenesSearchPage] fetchGenes: Backend response data:", data);


      if (data.error) { // Si el backend formatea su error así: { "error": "mensaje de error" }
        console.error("[GenesSearchPage] fetchGenes: Backend returned an error property:", data.error);

        setError(data.error);
        setGenes([]);
      } else if (data.result && Array.isArray(data.result)) { // La estructura esperada para resultados exitosos
        console.log("[GenesSearchPage] fetchGenes: Successfully received and parsed data.result. Genes count:", data.result.length);
        setGenes(data.result);
      } else {
        // Esta condición es clave basada en nuestra discusión anterior
        console.error("[GenesSearchPage] fetchGenes: ❌ Response data.result is not an array or data is not in expected format. Data received:", data);
        setError("La respuesta del backend no tiene el formato esperado (se esperaba 'result' como un array).");
        setGenes([]);
      }
    } catch (err) {
      // 6. Log del error capturado en el bloque catch
      const errorMessage = err instanceof Error ? err.message : "Ocurrió un error desconocido durante el fetch.";
      console.error("[GenesSearchPage] fetchGenes: CATCH block error:", err); // Loguea el objeto 'err' completo
      console.error("[GenesSearchPage] fetchGenes: CATCH block error message:", errorMessage);
      setError(errorMessage);
      setGenes([]);
    } finally {
      setIsLoading(false);
      console.log("[GenesSearchPage] fetchGenes: fetch operation finished (finally block).");
    }
  }, [searchQuery]); 

  useEffect(() => {
 //  Log dentro del useEffect cuando searchQuery cambia
    console.log(`[GenesSearchPage] useEffect: searchQuery changed to "${searchQuery}".`);

 // Llama a fetchGenes directamente si searchQuery tiene valor.
    if (searchQuery && searchQuery.trim() !== "") {
   
    console.log("[GenesSearchPage] useEffect: searchQuery has value, preparing to call fetchGenes with debounce.");
    const delayDebounce = setTimeout(() => {
      console.log("[GenesSearchPage] useEffect: Debounce timer expired, calling fetchGenes.");
     fetchGenes();
   }, 300); 
   return () => {
     console.log("[GenesSearchPage] useEffect: Cleanup. Clearing debounce timer.");
     clearTimeout(delayDebounce);
   };
 } else {
   // Si la query se borra o está vacía inicialmente, limpia los resultados
   console.log("[GenesSearchPage] useEffect: searchQuery is empty, clearing results.");
   setGenes([]);
   setError(null);
   setIsLoading(false);
 }
}, [searchQuery, fetchGenes]); 

  return (
    <div>
      <h1>Genes de Bacillus Cereus</h1>

      {isLoading && <p>Cargando...</p>}
      {error && !isLoading && <ErrorMessage message={error} />}

      {!isLoading && !error && genes.length > 0 && (
        <GenesTable data_genes={genes} resultsPerPage={25} />
      )}

      {!isLoading && !error && genes.length === 0 && searchQuery && searchQuery.trim() !== "" && (
        <p className="mt-4 text-gray-500">
          No se encontraron resultados para "{searchQuery}"
        </p>
      )}
      {!isLoading && !error && genes.length === 0 && (!searchQuery || searchQuery.trim() === "") && (
        <p className="mt-4 text-gray-500">
          Introduce un término de búsqueda para ver resultados.
        </p>
      )}

    </div>
  );
};

export default GenesSearchPage;

