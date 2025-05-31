// src/app/features/kegg/components/keggGraph/types.ts

// en keggTypes.ts
export interface KeggNode {
  id: string;
  label: string;
  type: string;
  x?: number; // Opcional si no siempre viene
  y?: number; // Opcional
}

export interface KeggEdge {
  source: string;
  target: string;
  label?: string; // Opcional
  type?: string;  // Opcional
}

export interface KeggPathwayGraphData {
  _id: string; // Cambiado de pathwayId a _id si así lo devuelve FastAPI
  name?: string; // Nombre principal
  pathwayName?: string; // Puede ser redundante si 'name' ya existe
  organism_code?: string;
  image_url?: string; // Cambiado de pathwayImageUrl
  nodes: KeggNode[];
  edges: KeggEdge[];
}

export interface KeggData {
  genId: string;
  ruta: string;  // o cualquier otra estructura que defina tu ruta metabólica
}

/*
export interface GraphData {
  // Define los tipos según los datos que recibes de tu API
  nodes: Array<{ id: string; label: string }>;
  edges: Array<{ from: string; to: string }>;
}
*/