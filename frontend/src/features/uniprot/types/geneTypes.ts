/**
 * Definicion de interfaces TypeScript para de datos de genes. 
 * 'GeneEntry': describe la estructura de una entrada individual de datos genéticos.
 * 'GenesTableProps: describe las props requeridas por el componente 'GenesTable.
 */

export interface Gene {
    orderedLocusNames?: string;
  }
  
export interface Sequence {
  value?: string;
  length?: number;
}
  
export interface GeneEntry {
  genes?: Gene[];
  proteinDescription?: string;
  sequence?: Sequence;
}
  
export interface GenesTableProps {
  data_genes: GeneEntry[];
  resultsPerPage?: number;
}
  