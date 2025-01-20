import { NextResponse } from "next/server";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const query = searchParams.get("query");

  if (!query) {
    return NextResponse.json({ error: "Missing query" }, { status: 400 });
  }

  try {
    const uniProtResponse = await fetch(
      `https://rest.uniprot.org/uniprotkb/search?query=${query}&format=json`
    );
    const data = await uniProtResponse.json();

    // Procesar los resultados para extraer información útil
    const results = data.results.map((item: any) => ({
      name: item.primaryAccession,
      link: `https://www.uniprot.org/uniprot/${item.primaryAccession}`,
    }));

    return NextResponse.json({ results });
  } catch (error) {
    console.error("Error fetching UniProt data:", error);
    return NextResponse.json({ error: "Error fetching UniProt data" }, { status: 500 });
  }
}
