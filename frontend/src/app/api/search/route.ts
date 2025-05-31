// frontend/src>/app/api/search/route.ts

/**
 * @file route.ts
 * @description API Route Handler para Next.js (App Router).
 * 
 * Este handler actúa como un proxy para reenviar las solicitudes de búsqueda de genes 
 * desde el frontend de Next.js hacia un backend de FastAPI.
 * 
 * Funcionamiento:
 * 1. Recibe una petición GET en la ruta `/api/kegg/pathway_gor_gene`.
 * 2. Espera un parámetro de consulta (query parameter) llamado `query` en la URL 
 *    (ej: `/api/genes?query=BC_0002`).
 * 3. Si el parámetro `query` no se proporciona, devuelve un error 400.
 * 4. Realiza una llamada fetch al endpoint `/api/genes` del backend de FastAPI 
 *    (configurado en `http://localhost:8000`), pasando el `query` recibido.
 * 5. Si la llamada al backend de FastAPI es exitosa:
 *    - Parsea la respuesta JSON del backend.
 *    - Devuelve los datos JSON al cliente que originó la petición.
 * 6. Si hay algún error durante la llamada al backend de FastAPI o al procesar 
 *    la respuesta:
 *    - Loguea el error en la consola del servidor Next.js.
 *    - Devuelve un error 500 al cliente.
 */

import { NextResponse } from "next/server";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const query = searchParams.get("query");

  if (!query) {
    return NextResponse.json({ error: "Missing query" }, { status: 400 });
  }

  try {
    // Llamada a backend FastAPI 
    const backendResponse = await fetch(`http://localhost:8000/api/genes?query=${query}`);

    if (!backendResponse.ok) {
      throw new Error(`Error del backend: ${backendResponse.statusText}`);
    }

    const data = await backendResponse.json();

    return NextResponse.json(data);
  } catch (error) {
    console.error("Error fetching data from backend:", error);
    return NextResponse.json(
      { error: "Error fetching data from backend" },
      { status: 500 }
    );
  }
}
