// src/app/api/kegg/pathways_for_gene/[genId]/route.ts

/**
 * @file route.ts
 * @summary Next.js API Route Handler para obtener las rutas metabólicas de KEGG asociadas a un gen específico.
 *
 * @description
 * Este script define un endpoint GET para el App Router de Next.js en la ruta dinámica
 * `/api/kegg/pathways_for_gene/[genId]`.
 *
 * Actualmente, extrae el `genId` (identificador del gen) de los segmentos de la URL
 * (`request.nextUrl.pathname`) como un WORKAROUND debido a problemas de compilación
 * con Docker al usar la desestructuración estándar de `params`. Este método debería
 * revertirse al uso de `{ params }` una vez que se resuelva el problema subyacente.
 *
 * La función principal es:
 * 1. Extraer y validar el `genId` de la URL.
 * 2. Construir una URL de solicitud a un servicio FastAPI externo (`${FASTAPI_URL}/kegg/${genId}`).
 * 3. Obtener los datos del gen y sus rutas asociadas desde el servicio FastAPI.
 * 4. La respuesta de FastAPI (tipo `BackendGenePathwayResponse`) se mapea/transforma
 *    a la estructura `KeggGeneWithpathways` esperada por el frontend.
 * 5. Manejar posibles errores del servicio FastAPI (ej. respuestas no exitosas, JSON malformado).
 * 6. Devolver los datos transformados (`KeggGeneWithpathways`) como una respuesta JSON al cliente.
 * 7. Manejar errores de red u otras excepciones durante el proceso.
 *
 * @param {NextRequest} request - El objeto de solicitud entrante de Next.js. Se utiliza `request.nextUrl.pathname`
 *                                para extraer el `genId` debido al workaround actual.
 *
 * @returns {Promise<NextResponse>}
 *   - En caso de éxito: Un `NextResponse` con un cuerpo JSON que contiene los datos `KeggGeneWithpathways`.
 *   - En caso de fallo: Un `NextResponse` con un cuerpo JSON que detalla el error y un código de estado HTTP apropiado (400, 500, etc.).
 *
 * @todo Revertir la extracción de `genId` para usar `{ params }: { params: { genId: string } }`
 *       en la firma de la función GET una vez que se resuelvan los problemas de compilación
 *       de TypeScript en el entorno Docker.
 */

import { NextRequest, NextResponse } from 'next/server';
import { KeggGeneWithpathways, KeggPathwayEntry } from '@/features/kegg/types/keggTypes'; 

const FASTAPI_URL = process.env.FASTAPI_BASE_URL || 'http://localhost:8000';

// Un tipo para la respuesta cruda del backend 
interface BackendGenePathwayResponse {
  _id: string;
  entry: string;
  name: string;
  pathways: KeggPathwayEntry[]; 
}

export async function GET(
  request: NextRequest,

  ) {
    // ---------------------------------------------------------------------------
    // TODO: WORKAROUND - Revertir a context.params cuando se resuelva el problema
    // de build en Docker con la firma tipada de params.
    // Error original durante 'docker-compose build': Fallo de compilación de TS
    // al intentar usar la forma idiomática de Next.js para acceder a params.
    const pathname = request.nextUrl.pathname;
    const segments = pathname.split('/');
    // Asumimos que la URL es /api/kegg/pathways_for_gene/[genId]

    const genId = segments.pop() || ''; // Obtiene el último segmento, o string vacío
    // ---------------------------------------------------------------------------
  
    console.log(`[API WORKAROUND /pathways_for_gene] genId extraído de URL: ${genId}`);
  
    if (!genId) {
      console.error("[API WORKAROUND /pathways_for_gene] Error: genId no encontrado en la URL o es inválido", { pathname });
      return NextResponse.json({ error: 'genId es requerido y no se pudo extraer de la URL' }, { status: 400 });
    }

  try {
    console.log(`[Next API] Fetching pathways for gene from FastAPI: ${genId}`);
    // Aquí llamas a tu endpoint de FastAPI
    // El endpoint de FastAPI espera un ID de gen (ej: "eco:b0002" o incluso un nombre como "rpoB" si tu backend lo maneja)
    // y devolver la estructura KeggGeneWithpathways
    //const fastApiResponse = await fetch(`${FASTAPI_URL}/kegg/gene_pathways/${encodeURIComponent(genId)}`);
    const fastApiResponse = await fetch(`${FASTAPI_URL}/kegg/${encodeURIComponent(genId)}`);

    if (!fastApiResponse.ok) {
      let errorBody;
      try {
        errorBody = await fastApiResponse.json();
      } catch (e) {
        errorBody = { detail: fastApiResponse.statusText };
      }
      console.error(`[Next API] FastAPI error for gene_pathways/${genId}: ${fastApiResponse.status}`, errorBody);
      return NextResponse.json(
        { error: 'Failed to fetch data from KEGG service', detail: errorBody.detail || 'Unknown error' },
        { status: fastApiResponse.status }
      );
    }

   // const data: KeggGeneWithpathways = await fastApiResponse.json();
    // La API de FastAPI debería devolver un objeto que coincida con KeggGeneWithpathways
    // { geneId: "actual_kegg_id", geneName: "...", geneDefinition: "...", pathways: [{ pathway_id, pathway_name }, ...] }
    // return NextResponse.json(data);

    const rawBackendData: BackendGenePathwayResponse = await fastApiResponse.json();

    // Mapeamos la respuesta del backend a la estructura KeggGeneWithpathways
    const transformedData: KeggGeneWithpathways = {
      geneId: rawBackendData.entry,       //  'entry' = 'geneId'
      geneName: rawBackendData.name,      // 'name' = 'geneName'. 
                                        
      pathways: rawBackendData.pathways, 
    };
    
    console.log("[Next API /pathways_for_gene] Transformed data for frontend:", transformedData);
    return NextResponse.json(transformedData);

  } catch (error) {
    console.error(`[Next API] Error fetching pathways for gene ${genId}:`, error);
    const message = error instanceof Error ? error.message : "An unknown error occurred";
    return NextResponse.json({ error: 'Internal Server Error', detail: message }, { status: 500 });
  }
}