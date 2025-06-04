// src/ app/ components/GenesTable.jsx

/**
 * @file GenesTable.jsx
 * @description Componente de React (Next.js 'use client') que renderiza una tabla de datos de genes
 * utilizando el componente `DataGrid` de MUI.
 *
 * Funcionalidad:
 * - Recibe un array de `QueryResultItem` (a través de la prop `data_items`) y un número inicial de resultados por página (`resultsPerPage`).
 * - Procesa los `data_items`: si un `QueryResultItem` contiene un array de `genes`, cada uno de estos genes se convierte en una fila separada en la tabla.
 * - Muestra información específica de cada gen en columnas: Accession, Gene Name (basado en orderedLocusNames), Protein Description, Sequence, Length y Mol. Weight.
 * - Implementa paginación del lado del cliente, gestionada por `DataGrid` y estado local.
 * - Permite al usuario cambiar el número de filas por página.
 * - Aplica estilos personalizados a `DataGrid` mediante la prop `sx`.
 *  
 * @param {QueryResultItem[]} data_items - Array de objetos `QueryResultItem`, donde cada objeto
 *                                         puede contener un array de `genes` (tipo `FrontendGene`).
 *                                         Estos datos son procesados para la visualización en tabla.
 * @param {number} [resultsPerPage=10] - El número inicial de filas a mostrar por página.
 */

'use client'

import React from 'react';
import { DataGrid, GridPaginationModel,
  GridRenderCellParams } from '@mui/x-data-grid';
import { ResultsTableProps, FrontendGene } from '../features/uniprot/types/geneTypes';

/** 
const formatGenesDisplay = (genes: FrontendGene[] | undefined): string => {
  if (!genes || !Array.isArray(genes) || genes.length === 0) return 'N/A';
  return genes
    .map(g => `${g.geneName || '(No Name)'} (${g.orderedLocusNames || 'N/A'})`)
    .join('; ');
};
*/

const GenesTable: React.FC<ResultsTableProps> = ({ data_items, resultsPerPage = 10 }) => {
   
  // Procesar los datos recibidos para adaptarlos a los campos de la tabla
   
  const processedGenes = React.useMemo(() => {
    if (!data_items || data_items.length === 0) return [];
    return data_items.flatMap((entry, entryIndex) =>
      (entry.genes || []).map((gene, geneIndex) => ({
        id: `${entryIndex}-${geneIndex}`,
        primaryAccession: entry.primaryAccession ?? 'N/A',
        geneName: gene.orderedLocusNames || '',
        proteinDescription: entry.proteinDescription || '',
        sequence: entry.sequence?.value || '',
        length: entry.sequence?.length || 0,
        molWeight: entry.sequence?.molWeight ?? null
      }))
    );
  }, [data_items]);

    // Definición de columnas de la tabla
  const columns = [
    {field: 'primaryAccession', headerName: 'Accession', width: 140},
    { field: 'geneName', headerName: 'Gene Name', width: 150 },
    { field: 'proteinDescription', headerName: 'Protein Description', flex: 1, minWidth: 200 },
    {
      field: 'sequence',
      headerName: 'Sequence',
      flex: 2,
      minWidth: 300,
      cellClassName: 'sequence-cell',
    },
    { field: 'length', headerName: 'Length', width: 100 },
    { field: 'molWeight', headerName: 'Mol. Weight', width: 100 },
  ];

  const [paginationModel, setPaginationModel] = React.useState<GridPaginationModel>({
    page: 0,
    pageSize: resultsPerPage,
  });

  return (
    <div style={{ width: '100%', marginTop: '20px' }}>

      <DataGrid
        rows={processedGenes}
        columns={columns}
        paginationModel={paginationModel}
        onPaginationModelChange={setPaginationModel}
        pagination
        pageSizeOptions={[5, 10, 20, 50]}
        disableRowSelectionOnClick
        sx={{
          '& .MuiDataGrid-columnHeaders': {
            backgroundColor: '#e0e0e0', // Gris claro constante
          },
          '& .MuiDataGrid-columnHeader': {
            backgroundColor: '#e0e0e0 !important', // Forzar fondo en todos los estados
          },
          '& .MuiDataGrid-columnHeader:hover': {
            backgroundColor: '#e0e0e0 !important', // Sin cambio en hover
          },
          '& .MuiDataGrid-columnHeader:focus, & .MuiDataGrid-columnHeader:focus-within': {
            backgroundColor: '#e0e0e0 !important', // Sin cambio en foco
          },
          '& .MuiDataGrid-columnHeaderTitle': {
            fontWeight: 'bold',
            fontSize: '1rem',
          },
          '& .sequence-cell': {
            whiteSpace: 'normal !important',
            wordBreak: 'break-word !important',
            lineHeight: '1.2 !important',
          },
        }}
      />
    </div>
  );
};


export default GenesTable;
