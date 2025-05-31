// src/app/rutas-metabolicas/[geneId]/page.tsx

import Link from 'next/link';
import KeggPathwayListFetcher from '@/features/kegg/components/keggPathwayListFetcher';
import KeggPathwayGraphFetcher from '@/features/kegg/components/keggPathwayGraphFetcher';

export async function generateMetadata({ params }: { params: { geneId: string } }) {
  return {
    title: `Rutas Metabólicas para ${params.geneId}`,
  };
}

export default function RutasMetabolicasPage({ params }: { params: { geneId: string } }) {
  const { geneId } = params; // Este es el ID de KEGG, ej: "hsa:672"

  return (
    <div className="flex flex-col items-center min-h-screen p-4 ...">
      <header className="text-center w-full mb-4 ...">
        <h1 className="text-2xl ...">
          Rutas Metabólicas KEGG para: <span className="font-mono ...">{geneId}</span>
        </h1>
        {/* ... Link de volver ... */}
      </header>
      
      <main className="w-full max-w-7xl space-y-8">
        <section id="kegg-pathways" className="space-y-6">
          <h2 className="text-xl ...">Explorador de Rutas Metabólicas</h2>
    
          {/* Pasa el geneId de la URL directamente como prop */}
          <KeggPathwayListFetcher  />
    
          {/*
            KeggPathwayGraphFetcher sigue funcionando con PathwayContext.
            Si KeggPathwayGraphFetcher TAMBIÉN necesita el geneId (para resaltar el gen en el grafo),
            y lo obtenía de GenContext, entonces tenemos dos opciones:
            1. KeggPathwayListFetcher, además de actualizar PathwayContext, también actualiza GenContext con el `targetGeneId`.
            2. KeggPathwayGraphFetcher también se modifica para aceptar `targetGeneId` como prop,
               y se lo pasamos aquí: <KeggPathwayGraphFetcher targetGeneId={geneId} />
            La opción 1 es más limpia si KeggPathwayGraphFetcher ya usa GenContext.
          */}
          <KeggPathwayGraphFetcher />
        </section>
      </main>
    </div>
  );
}