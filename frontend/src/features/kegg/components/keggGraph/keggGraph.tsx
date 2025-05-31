// src/features/kegg/components/keggGraph/keggGraph.tsx

import React from "react";
import { KeggData } from "./types"; 
import Link from 'next/link';

interface KeggGraphProps {
  data: KeggData;
}

const KeggGraph: React.FC<KeggGraphProps> = ({ data }) => {
  return (
    <div>
      <h3>Ruta Metabólica de {data.genId}</h3>
   
      <Link href={`/features/kegg/${data.genId}`}>
         Ver ruta metabólica
      </Link>
    </div>
  );
};

export default KeggGraph;


/*
'use client'

import CytoscapeComponent from 'react-cytoscapejs';
// import { useEffect, useState } from 'react';

import { KeggGraphProps } from './types'; // Asegúrate de importar el tipo correctamente

// Aquí KeggGraph recibe los props definidos en KeggGraphProps
export default function KeggGraph({ nodes, edges }: KeggGraphProps) {
  const elements = [
    ...nodes.map((node) => ({ data: { id: node.id, label: node.label } })),
    ...edges.map((edge) => ({ data: { source: edge.source, target: edge.target } })),
  ];

  return (
    <div style={{ height: '600px', width: '100%' }}>
      <CytoscapeComponent
        elements={elements}
        style={{ width: '100%', height: '100%' }}
        layout={{ name: 'cose' }}
        stylesheet={[
          {
            selector: 'node',
            style: {
              label: 'data(label)',
              'background-color': '#0074D9',
              color: '#fff',
              'text-valign': 'center',
              'text-halign': 'center',
            },
          },
          {
            selector: 'edge',
            style: {
              'line-color': '#aaa',
              'target-arrow-color': '#aaa',
              'target-arrow-shape': 'triangle',
              'curve-style': 'bezier',
            },
          },
        ]}
      />
    </div>
  );
}
*/