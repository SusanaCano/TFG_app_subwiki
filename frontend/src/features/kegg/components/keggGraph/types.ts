// src/app/features/kegg/components/keggGraph/types.ts

/**
 * @file types.ts
 * @description Define las interfaces TypeScript para las estructuras de datos utilizadas
 *              en la representación y manejo de grafos de rutas metabólicas de KEGG.
 *              Incluye tipos para nodos, aristas (conexiones), datos completos de un grafo
 *              de ruta y una estructura de datos más simple para pasar información inicial.
 *
 * Interfaces Exportadas:
 * - `KeggNode`: Representa un nodo individual dentro de un grafo de KEGG (por ejemplo,
 *               un gen, un compuesto). Incluye propiedades como `id`, `label` (etiqueta),
 *               `type` (tipo de nodo) y coordenadas opcionales `x`, `y`.
 * - `KeggEdge`: Define una arista o conexión entre dos nodos (`KeggNode`) en el grafo.
 *               Especifica el `source` (nodo origen) y `target` (nodo destino),
 *               y puede incluir una `label` o `type` opcionales.
 * - `KeggPathwayGraphData`: Estructura de datos completa para un grafo de ruta metabólica
 *                           específico de KEGG. Contiene metadatos de la ruta (como `_id`,
 *                           `name`, `pathwayName`, `organism_code`, `image_url`) junto con
 *                           arrays de `KeggNode` (nodos) y `KeggEdge` (aristas) que componen
 *                           el grafo.
 * - `KeggData`: Una estructura de datos más simple, utilizada por componentes como
 *               `KeggGraph` (y obtenida por `KeggGraphContainer`). Contiene un `genId`
 *               (identificador del gen) y una `ruta` (string que probablemente representa
 *               un identificador de ruta o información relacionada para ese gen).
 */


export interface KeggNode {
  id: string;
  label: string;
  type: string;
  x?: number; 
  y?: number; 
}

export interface KeggEdge {
  source: string;
  target: string;
  label?: string; 
  type?: string;  
}

export interface KeggPathwayGraphData {
  _id: string; 
  name?: string; // Nombre principal
  pathwayName?: string;
  organism_code?: string;
  image_url?: string; 
  nodes: KeggNode[];
  edges: KeggEdge[];
}

export interface KeggData {
  genId: string;
  ruta: string;  
}

