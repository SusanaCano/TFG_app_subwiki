/**
* @file geneTypes.ts (o el nombre real del archivo)
 * @description Define las interfaces TypeScript para las estructuras de datos utilizadas
 *              en la funcionalidad de búsqueda y visualización de genes/proteínas de UniProt.
 *              Estos tipos modelan la respuesta del backend, entidades de datos y las
 *              props de los componentes de React.
 *
 * Interfaces exportadas:
 * - `FrontendGene`: Representa la información esencial de un gen, como su nombre
 *                   y los nombres de locus ordenados (orderedLocusNames).
 * - `FrontendSequence`: Describe los detalles de una secuencia (ej. de proteína), incluyendo
 *                       su valor (la secuencia), longitud y, opcionalmente y
 *                       peso molecular.
 * - `QueryResultItem`: Estructura principal para cada ítem de resultado obtenido de la
 *                      búsqueda en el backend. Agrupa el acceso primario, la descripción
 *                      de la proteína, un array de `FrontendGene` asociados y un objeto
 *                      `FrontendSequence`.
 * - `ResultsTableProps`: Define las propiedades (props) requeridas por el componente
 *                        `GenesTable` (componente de tabla de resultados),
 *                        incluyendo el array `data_items` (que son `QueryResultItem`)
 *                        y el número de resultados por página.
 */


export interface FrontendGene {
  geneName: string; 
  orderedLocusNames: string; 
}

export interface FrontendSequence {
  value: string;  
  length: number; 
  molWeight?: number | null; 
  crc64?: string | null;     
  md5?: string | null;       
}

// Tipo principal que representa cada ítem del resultado del backend.

export interface QueryResultItem {
  primaryAccession?: string | null; 
  proteinDescription?: string | null; 
  genes: FrontendGene[]; 
  sequence: FrontendSequence; 
}


export interface ResultsTableProps  {
  data_items: QueryResultItem[]; 
  resultsPerPage?: number;
}
