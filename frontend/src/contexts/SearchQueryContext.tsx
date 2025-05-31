// src/contexts/SearchQueryContext.tsx

/**
 * @file SearchQueryContext.tsx
 * @description Este archivo define un Contexto de React para gestionar globalmente 
 * el término de búsqueda (query) ingresado por el usuario.
 * 
 * Proporciona:
 * - `SearchQueryContext`: El contexto en sí.
 * - `SearchQueryProvider`: Un componente proveedor que envuelve partes de la aplicación
 *   y gestiona el estado de `searchQuery` y la función `setSearchQuery` para actualizarlo.
 * - `useSearchQuery`: Un hook personalizado para que los componentes puedan consumir 
 *   fácilmente el `searchQuery` y la función `setSearchQuery` del contexto.
 *
 * Propósito: Permitir que el componente `SearchBar` actualice el término de búsqueda
 * y que otros componentes, como `GenesSearchPage`, puedan leer este término y reaccionar
 * a sus cambios para realizar búsquedas o mostrar información relevante.
 */

'use client';

import React, { createContext, useState, useContext, ReactNode, Dispatch, SetStateAction } from 'react';

interface SearchQueryContextType {
  searchQuery: string;
  setSearchQuery: Dispatch<SetStateAction<string>>;
}

const defaultState: SearchQueryContextType = {
  searchQuery: '',
  setSearchQuery: () => {},
};

const SearchQueryContext = createContext<SearchQueryContextType>(defaultState);

export const SearchQueryProvider = ({ children }: { children: ReactNode }) => {
  const [searchQuery, setSearchQuery] = useState<string>('');

  return (
    <SearchQueryContext.Provider value={{ searchQuery, setSearchQuery }}>
      {children}
    </SearchQueryContext.Provider>
  );
};

export const useSearchQuery = (): SearchQueryContextType => {
  const context = useContext(SearchQueryContext);

  
  if (context === defaultState || context.setSearchQuery === defaultState.setSearchQuery) {
   
    throw new Error('useSearchQuery must be used within a SearchQueryProvider and not with the default context value');
  
  }

  return context;
};