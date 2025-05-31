// src/ app/ components/GenesTable.jsx

/**
 * Componente de React que muestra una tabla con los datos de genes obtenidos de la consulta 
 * a mongoDB, usando MUI DataGrid.
 * Recibe una lista de entrada de genes ('data_genes') y una paginación de estos.
 * Rederidado de la tabla con paginacion del lado del cliente.
 * GenesTableProps estructura de los datos que se reciben.
 */

'use client'

import React from 'react';
import { DataGrid, GridPaginationModel } from '@mui/x-data-grid';
import { GenesTableProps } from '../features/uniprot/types/geneTypes';



const GenesTable: React.FC<GenesTableProps> = ({ data_genes, resultsPerPage = 10 }) => {
   // Procesar los datos recibidos para adaptarlos a los campos de la tabla
  const processedGenes = React.useMemo(() => {
    if (!data_genes || data_genes.length === 0) return [];
    return data_genes.flatMap((entry, entryIndex) =>
      (entry.genes || []).map((gene, geneIndex) => ({
        id: `${entryIndex}-${geneIndex}`,
        geneName: gene.orderedLocusNames || '',
        proteinDescription: entry.proteinDescription || '',
        sequence: entry.sequence?.value || '',
        length: entry.sequence?.length || 0
      }))
    );
  }, [data_genes]);

    // Definición de columnas de la tabla
  const columns = [
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
