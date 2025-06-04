// src/features/uniprot/components/GenesSearchPage.tsx
/**
 * @file GenesSearchPage.tsx (o UniprotSearchPage.tsx)
 * @description Componente encargado de buscar y mostrar resultados de UniProt.
 *
 * Funcionalidad:
 * - Obtiene el término de búsqueda (`searchQuery`) del contexto  `SearchQueryContext`.
 * - Realiza una petición al endpoint `/api/uniprot/buscar` del backend cuando `searchQuery` cambia.
 * - Muestra un indicador de carga ("Cargando...").
 * - Muestra un mensajes de errorutilizando el componente `ErrorMessage` si la petición falla o el backend devuelve un error.
 * - Utiliza el tipo `QueryResultItem` para los datos de respuesta.
 */

'use client'

import React, { useState, useEffect, useCallback } from 'react';
import GenesTable from '@/components/GenesTable'; 
import ErrorMessage from '@/components/ErrorMessage';
import { QueryResultItem } from '../types/geneTypes'; 
import { useSearchQuery } from '../context/SearchQueryContext'; 

const GenesSearchPage = () => {
  const { searchQuery } = useSearchQuery();
  const [results, setResults] = useState<QueryResultItem[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  
  const fetchApiData = useCallback(async () => {
    
    console.log(`[GenesSearchPage] SIMPLIFIED fetchApiData: CALLED. Current searchQuery: "${searchQuery}"`);

    // Si no hay searchQuery, limpiar y salir 
    if (!searchQuery || searchQuery.trim() === "") {
      console.log("[GenesSearchPage] SIMPLIFIED fetchApiData: searchQuery is empty, clearing results.");
      setResults([]);
      setError(null);
      setIsLoading(false);
      return;
    }

    console.log(`[GenesSearchPage] SIMPLIFIED fetchApiData: searchQuery is "${searchQuery}", proceeding with fake data.`);
    setIsLoading(true);
    setError(null);


    try {
      const response = await fetch(`http://localhost:8000/api/uniprot/buscar?query=${encodeURIComponent(searchQuery.trim())}`);
      console.log("[GenesSearchPage] fetchApiData: Backend response status:", response.status, response.statusText);

      if (!response.ok) {
        let errorMessage = `Error ${response.status}: ${response.statusText}`;
        try {
          const errorData = await response.json();
          console.log("[GenesSearchPage] fetchApiData: Backend error data (response not ok):", errorData);
          errorMessage = errorData.detail || errorData.error || errorData.message || errorMessage;
        } catch (e) {
          console.warn("[GenesSearchPage] fetchApiData: Could not parse error response JSON.");
        }
        throw new Error(errorMessage);
      }

      const responseData = await response.json();
      console.log("[GenesSearchPage] fetchApiData: Backend response data (full JSON):", responseData);

      // Si el backend devuelve un error en el cuerpo del JSON exitoso (status 200)
      if (responseData.error) {
        console.error("[GenesSearchPage] fetchApiData: Backend returned an 'error' property in JSON:", responseData.error);
        setError(responseData.error);
        setResults([]);
      } else if (responseData.result && Array.isArray(responseData.result)) {
        console.log("[GenesSearchPage] fetchApiData: Successfully received data.result. Count:", responseData.result.length);
        setResults(responseData.result as QueryResultItem[]);
      } else {
        console.error("[GenesSearchPage] fetchApiData: Response data.result is not an array or data is not in expected format. Data received:", responseData);
        setError("La respuesta del backend no tiene el formato esperado (se esperaba 'result' como un array).");
        setResults([]);
      }

    } catch (err: any) {
      const errorMessage = err.message || "Ocurrió un error desconocido durante el fetch.";
      console.error("[GenesSearchPage] fetchApiData: CATCH block error:", err);
      setError(errorMessage);
      setResults([]);
    } finally {
      setIsLoading(false);
      console.log("[GenesSearchPage] fetchApiData: fetch operation finished (finally block).");
    }
  }, [searchQuery]);

  useEffect(() => {
    console.log(`[GenesSearchPage] useEffect: searchQuery changed to "${searchQuery}".`);
    if (searchQuery && searchQuery.trim() !== "") {
      console.log("[GenesSearchPage] useEffect: searchQuery has value, preparing to call fetchApiData with debounce.");
      const delayDebounce = setTimeout(() => {
        console.log("[GenesSearchPage] useEffect: Debounce timer expired, calling fetchApiData.");
        fetchApiData();
      }, 300);
      return () => {
        console.log("[GenesSearchPage] useEffect: Cleanup. Clearing debounce timer.");
        clearTimeout(delayDebounce);
      };
    } else {
      console.log("[GenesSearchPage] useEffect: searchQuery is empty, clearing results.");
      setResults([]);
      setError(null);
      setIsLoading(false);
    }
  }, [searchQuery, fetchApiData]);

  // Lógica de mensajes (adaptada para usar 'results' y ser un poco más concisa)
  let displayMessage = "";
  if (!searchQuery || searchQuery.trim() === "") {
    displayMessage = "Introduce un término de búsqueda para ver resultados.";
  } else if (!isLoading && !error && results.length === 0) {
    // Este mensaje se muestra si la búsqueda se hizo pero no hubo resultados
    displayMessage = `No se encontraron resultados para "${searchQuery}".`;
  }

  return (

    <div>
    <h1>Genes de Bacillus Cereus </h1>

    {isLoading && <p className="mt-4 text-blue-500">Cargando...</p>}
    {error && !isLoading && <ErrorMessage message={error} />}

    {!isLoading && !error && results.length > 0 && (
    
      <GenesTable data_items={results} resultsPerPage={10} />
    )}

    {/* Muestra el mensaje si no hay carga, ni error, y no hay resultados */}
    {!isLoading && !error && results.length === 0 && displayMessage && (
       <p className="mt-4 text-gray-500">{displayMessage}</p>
    )}
  </div>

  );
};

export default GenesSearchPage;