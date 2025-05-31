// frontend/scr/app/api/pathway_graph/[pathwayId]/route.ts

/**
 * @file route.ts
 * @summary Next.js API Route Handler para obtener datos de grafos de rutas metabólicas de KEGG.
 *
 * @description
 * Este script define un endpoint GET para el App Router de Next.js en la ruta dinámica
 * `/api/pathway_graph/[pathwayId]`.
 *
 * Recibe un `pathwayId` como segmento dinámico de la ruta.
 * La función principal es:
 * 1. Validar el `pathwayId` entrante.
 * 2. Construir una URL de solicitud a un servicio FastAPI externo (`${FASTAPI_URL}/api/kegg/pathways_graph/pathways_graph/${pathwayId}`).
 * 3. Obtener los datos del grafo de la ruta metabólica desde el servicio FastAPI.
 * 4. Manejar posibles errores del servicio FastAPI (ej. respuestas no exitosas, JSON malformado).
 * 5. Analizar (parsear) la respuesta exitosa (que se espera sea `KeggPathwayGraphData`) desde FastAPI.
 * 6. Devolver los datos como una respuesta JSON al cliente.
 * 7. Manejar errores de red u otras excepciones durante el proceso.
 *
 * @param {NextRequest} request - El objeto de solicitud entrante de Next.js (no se usa directamente su cuerpo en este handler GET, pero es estándar).
 * @param {{ params: { pathwayId: string } }} { params } - Objeto que contiene los parámetros dinámicos de la ruta.
 *   - `params.pathwayId`: El ID de la ruta metabólica de KEGG a obtener.
 *
 * @returns {Promise<NextResponse>}
 *   - En caso de éxito: Un `NextResponse` con un cuerpo JSON que contiene `KeggPathwayGraphData`.
 *   - En caso de fallo: Un `NextResponse` con un cuerpo JSON que detalla el error y un código de estado HTTP apropiado (400, 500, 502, etc.).
 */

import { NextRequest, NextResponse } from 'next/server';
import { KeggPathwayGraphData } from '@/features/kegg/types/keggTypes';

const FASTAPI_URL = process.env.FASTAPI_BASE_URL || 'http://localhost:8000';

export async function GET(
  request: NextRequest,
  { params }: { params: { pathwayId: string } } // Forma estándar y tipada de acceder a los params
) {
  const rawPathwayId = params.pathwayId; // Acceso directo al pathwayId desde params

  // Validación
  if (typeof rawPathwayId !== 'string' || !rawPathwayId.trim()) {
    console.warn(
      '[Route Handler] rawPathwayId no es un string válido o está ausente. Value:',
      rawPathwayId,
      'Params:',
      JSON.stringify(params) // Loguear el objeto params completo
    );
    return NextResponse.json(
      { error: 'Pathway ID es inválido, no es un string, o está ausente' },
      { status: 400 }
    );
  }

  // Si llegamos aquí, rawPathwayId es un string válido y no vacío.
  // Lo limpiamos (trim) y lo asignamos a nuestra constante final.
  const pathwayId: string = rawPathwayId.trim();

  console.log(`[Route Handler] pathwayId procesado: ${pathwayId}`);

  const targetUrl = `${FASTAPI_URL}/api/kegg/pathways_graph/pathways_graph/${encodeURIComponent(pathwayId)}`;
  
  console.log(`[Next API /pathway_graph] Attempting to fetch pathway graph for ID: ${pathwayId} from URL: ${targetUrl}`);

  try {
    const fastApiResponse = await fetch(targetUrl, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
      // cache: 'no-store', // Considera si lo necesitas para evitar caché
    });

    console.log(`[Next API /pathway_graph] FastAPI response status for ${pathwayId}: ${fastApiResponse.status}`);

    const responseBodyText = await fastApiResponse.text(); // Leer el cuerpo UNA VEZ

    if (responseBodyText) {
        console.log(`[Next API /pathway_graph] FastAPI response body (text) for ${pathwayId}: ${responseBodyText}`);
    } else {
        console.log(`[Next API /pathway_graph] FastAPI response body (text) for ${pathwayId} was empty.`);
    }

    if (!fastApiResponse.ok) {
      console.error(`[Next API /pathway_graph] FastAPI error for ${pathwayId}. Status: ${fastApiResponse.status}. Body: ${responseBodyText}`);

      let detailErrorMessage = responseBodyText;

      try {
        if (responseBodyText) {
            const errorJson = JSON.parse(responseBodyText);
            detailErrorMessage = errorJson.detail || JSON.stringify(errorJson) || responseBodyText;
        } else {
            detailErrorMessage = `FastAPI returned status ${fastApiResponse.status} with an empty response body.`;
        }
      } catch (e) {
        console.warn(`[Next API /pathway_graph] Could not parse FastAPI error response body as JSON. Using raw text or status. Error: ${e}`);
        
      }

      return NextResponse.json(
        { error: 'Failed to fetch data from KEGG service', detail: detailErrorMessage },
        { status: fastApiResponse.status }
      );
    }

    // Si la respuesta es OK, ahora parseamos el responseBodyText que ya leímos
    let data: KeggPathwayGraphData;
    try {
      if (!responseBodyText) { // Añadir check por si el cuerpo OK está vacío
        console.error(`[Next API /pathway_graph] FastAPI response was OK but body was empty for ${pathwayId}.`);
        return NextResponse.json(
          { error: 'Failed to parse data from KEGG service', detail: 'Received empty successful response from upstream' },
          { status: 502 } // Bad Gateway
        );
      }
      data = JSON.parse(responseBodyText);
    } catch (parseError) {
      console.error(`[Next API /pathway_graph] Failed to parse FastAPI response as JSON for ${pathwayId}:`, parseError);
      console.error(`[Next API /pathway_graph] Raw text that failed to parse:`, responseBodyText);
      return NextResponse.json(
        { error: 'Failed to parse data from KEGG service', detail: 'Received malformed JSON from upstream' },
        { status: 502 } 
      );
    }

    console.log(`[Next API /pathway_graph] Successfully fetched and parsed KeggPathwayGraphData for ${pathwayId}.`);
    return NextResponse.json(data);

  } catch (error: any) {
    console.error(`[Next API /pathway_graph] Network or other critical error fetching pathway graph ${pathwayId}:`, error);
    let errorMessage = "An unknown error occurred during fetch operation.";
    let errorCause = undefined;

    if (error instanceof Error) {
        errorMessage = error.message;
        if (error.cause) {
            errorCause = error.cause;
            console.error('[Next API /pathway_graph] Cause of error:', error.cause);
            errorMessage += ` Cause: ${(error.cause as any).code || JSON.stringify(error.cause)}`;
        }
    }
    return NextResponse.json({ error: 'Internal Server Error', detail: errorMessage, cause: errorCause }, { status: 500 });
  }
}


