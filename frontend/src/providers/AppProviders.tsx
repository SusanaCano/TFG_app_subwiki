// src/providers/AppProviders.tsx

/**
 * @file AppProviders.tsx
 * @description Componente que agrupa y proporciona todos los contextos globales
 * necesarios para la aplicación.
 * 
 * Funcionalidad:
 * - Envuelve a sus `children` (componentes hijos) con los proveedores de contexto.
 * - Actualmente incluye:
 *   - `SearchQueryProvider`: Para hacer disponible el contexto de búsqueda
 *     (`searchQuery` y `setSearchQuery`) a toda la aplicación o a las partes
 *     que lo necesiten.
 *   - `GenProvider`: (Asumo que es para otra funcionalidad, como KEGG)
 *     Proporciona el contexto relacionado con la información de genes de KEGG.
 * 
 * Propósito: Centralizar la provisión de contextos para mantener el `layout.tsx`
 * y la estructura general de la aplicación más limpios y organizados. Los componentes
 * anidados dentro de `AppProviders` podrán acceder a los contextos que este provee.
 */

'use client';

import { SearchQueryProvider } from '@/contexts/SearchQueryContext';
import { GenProvider } from '@/features/kegg/context/GenContext';
import { PathwayProvider } from '@/features/kegg/context/PathwayContext';

export function AppProviders({ children }: { children: React.ReactNode }) {
  console.log("AppProviders: Rendering");

  return (
    <SearchQueryProvider>
      <GenProvider> 
        <PathwayProvider> 

          {children}
        
        </PathwayProvider> 
      </GenProvider> 
    </SearchQueryProvider>
  );
}