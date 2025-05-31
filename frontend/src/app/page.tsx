// src/app/page.tsx

/**
 * @file page.tsx (para la ruta '/')
 * @description Componente principal de la página de inicio de la aplicación.
 * 
 * Estructura y Contenido:
 * - Muestra un encabezado con el título de la aplicación y una breve descripción.
 * - Incluye un enlace a la página "Acerca de".
 * - Renderiza el componente `SearchBar`, permitiendo al usuario ingresar un término de búsqueda.
 *   `SearchBar` actualizará el `SearchQueryContext`.
 * - Renderiza el componente `GenesSearchPage`, que escuchará los cambios en `SearchQueryContext`
 *   (actualizados por `SearchBar`) y mostrará los resultados de la búsqueda de genes.
 * 
 * Esta página actúa como el contenedor principal para la funcionalidad de búsqueda
 * y visualización de resultados en la ruta raíz de la aplicación.
 */

import Link from "next/link";
import GenesSearchPage from '../features/uniprot/components/GenesSearchPage';
import SearchBar from '@/components/ui/SearchBar';
import KeggPathwayListFetcher from "@/features/kegg/components/keggPathwayListFetcher"; 
import KeggPathwayGraphFetcher from "@/features/kegg/components/keggPathwayGraphFetcher";



export default function Home() {
  
  return (
    <div className="flex flex-col items-center min-h-screen p-4 sm:p-8 md:p-12 lg:p-20 pb-20 gap-8 font-[var(--font-geist-sans)]">
      <header  className="text-center w-full mb-4 md:mb-8">
      <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold mb-2">
        Explorador de Genes
      </h1>

      <p className="text-gray-600 mb-4">
          Busca información detallada sobre genes.
      </p>

      <Link href="/about" className="text-blue-600 hover:underline">
          Acerca de esta aplicación
      </Link>
      
      </header>
      
      {/* SearchBar actualiza el SearchQueryContext */}
      <SearchBar />
      
        <main className="w-full max-w-7xl space-y-8">
          <section id="uniprot-results">
            <h2 className="text-xl sm:text-2xl font-semibold mb-3 text-gray-800">Resultados de Búsqueda de Genes (UniProt)</h2>
      
            <GenesSearchPage />
    
          </section>
    
          <hr className="my-6 border-gray-300" />

          <section id="kegg-pathways" className="space-y-6">
            <h2 className="text-xl sm:text-2xl font-semibold mb-3 text-gray-800">Explorador de Rutas Metabólicas KEGG</h2>
      
            {/* Primero se muestra la lista de pathways para el genId/searchQuery */}
     
            <KeggPathwayListFetcher />
      
            {/* Luego, si se selecciona un pathway de la lista, se muestra su gráfico */}
            <KeggPathwayGraphFetcher />

            </section>
        </main>
      </div>
    );
}
