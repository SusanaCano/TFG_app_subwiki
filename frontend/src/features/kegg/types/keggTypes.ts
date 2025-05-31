// src/features/kegg/types/keggTypes.ts 

/*
* @file keggTypes.ts
* @description Define las estructuras de tipo para los datos relacionados con KEGG.
*/

// Representa una entrada en la lista de pathways asociados a un gen
export interface KeggPathwayEntry {
    pathway_id: string;   // ej. "bce00010" (organism specific) or "map00010" (reference)
    pathway_name: string; // ej. "Glycolysis / Gluconeogenesis"
    pathways: KeggPathwayEntry[]; 
    
}

    // Datos completos para un gen de KEGG, incluyendo la lista de sus pathways
export interface KeggGeneWithpathways {
    geneId: string; // El ID del gen que se buscó (ej. "BC_0002" o "bce:BC_0002")
    geneName?: string;
    geneDefinition?: string;
    pathways: KeggPathwayEntry[]; // Lista de pathways en los que participa
}

    // Datos para visualizar un gráfico de pathway específico
export interface KeggNode {
    id: string;
    label: string;
    type?: 'gene' | 'compound' | 'map' | 'ortholog' | string; // string para flexibilidad
    
}

export interface KeggEdge {
    id?: string;
    source: string;  // id de un KeggNode
    target: string;  // id de un KeggNode
    label?: string; // ej. nombre de la reacción
    type?: 'reaction' | 'interaction' | 'link' | string; // string para flexibilidad
    
}

export interface KeggPathwayGraphData {
    //pathwayId: string;
    _id: string; 
    name: string;
    pathwayName: string;
    organism_code?: string;
    pathwayImageUrl?: string; // URL a la imagen oficial de KEGG del pathway
    image_url?: string; 
    nodes: KeggNode[];
    edges: KeggEdge[];
   
}