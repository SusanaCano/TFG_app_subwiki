// src/app/api/kegg/[genId]/route.ts
//import { NextRequest } from "next/server";

// import { NextResponse } from "next/server";
//import type { NextApiRequest } from "next";
//import type { NextFetchEvent } from "next/server";

/**
export async function GET(
  request: Request,
  context: { params : { genId: string } }
) {
  const { genId } = await context.params;

  try {
    const backendResponse = await fetch(`http://backend:8000/kegg/${genId}`);
    const data = await backendResponse.json();

    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: 'Error al obtener los datos de KEGG' },
      { status: 500 }
    );
  }
}
*/

/** 
type Params = {
  params: { genId: string };
};

export async function GET(
  request: NextRequest,
  context: Params)
  {
  //const { params } = await context;
  const { genId } = context.params;

  try {
    const backendResponse = await fetch(`http://backend:8000/kegg/${genId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      // Si usas ISR, opcional
      next: { revalidate: 60 },
    });

    if (!backendResponse.ok) {
      return new Response(JSON.stringify({ error: "Ruta metabólica no encontrada" }), {
        status: backendResponse.status,
        headers: { "Content-Type": "application/json" },
      });
    }

    const data = await backendResponse.json();

    return new Response(JSON.stringify(data), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  } catch (error) {
    console.error("Error al contactar al backend:", error);
    return new Response(JSON.stringify({ error: "Error al conectar con el backend" }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }
}
*/

/** 
type Params = {
  params: {
    genId: string;
  };
};
*/

/** 
export async function GET(request: NextRequest, context: { params: { genId: string } }) {
  const { genId } = context.params;
*/

/** 
export async function GET(request: NextRequest, { params }: Params) {
  const { genId } = params;
  try {
    const backendResponse = await fetch(`http://backend:8000/kegg/${genId}`, {
      // Puedes agregar headers si necesitas autenticación, por ejemplo
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      // Tiempo de espera recomendado para evitar cuelgues
      next: { revalidate: 60 }, // Opcional: Cacheo por 60 segundos si lo usas con ISR
    });

    if (!backendResponse.ok) {
      return new Response(JSON.stringify({ error: "Ruta metabólica no encontrada" }), {
        status: backendResponse.status,
        headers: { "Content-Type": "application/json" },
      });
    }

    const data = await backendResponse.json();

    return new Response(JSON.stringify(data), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  } catch (error) {
    console.error("Error al contactar al backend:", error);
    return new Response(JSON.stringify({ error: "Error al conectar con el backend" }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }
}*/