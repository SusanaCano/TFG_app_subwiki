//  src/features/kegg/components/KeggPathwayGraphDisplay.tsx

//Este es el que realmente dibuja el gráfico. Se puede usar Cytoscape.js o mostrar una imagen  de API /api/kegg/pathway_graph/[pathwayId] devuelve una pathwayImageUrl.

/**
 * @file KeggPathwayGraphDisplay.tsx
 * @description  Componente de React (Next.js 'use client') que renderiza la visualización
 *              de una ruta metabólica específica de KEGG. Puede mostrar un grafo interactivo
 *              usando Cytoscape.js si se proporcionan datos de nodos y aristas, y/o una imagen
 *              estática de la ruta.
 *
 * Props:
 * - `graphData` (KeggPathwayGraphData | null | undefined): Un objeto que contiene los datos
 *   de la ruta metabólica. Este objeto puede incluir:
 *     - `nodes` y `edges`: Para renderizar el grafo con Cytoscape.js.
 *     - `image_url` o `pathwayImageUrl`: URL de una imagen estática de la ruta.
 *     - `name`, `pathwayName`, `_id`: Para mostrar un nombre de la ruta.
 *
 * Lógica de Renderizado:
 * 1. Si `graphData` es nulo o indefinido: Muestra un mensaje "Esperando datos del pathway...".
 * 2. Si `graphData` contiene `image_url` (o `pathwayImageUrl`) y NO contiene `nodes` (o están vacíos):
 *    Renderiza únicamente la imagen estática usando `<img>`.
 * 3. Si `graphData` contiene `nodes` (y opcionalmente `edges`):
 *    - Renderiza un grafo interactivo utilizando `CytoscapeComponent`.
 *    - Si `graphData` también contiene `image_url` (o `pathwayImageUrl`), esta imagen se
 *      muestra encima del grafo interactivo como referencia, utilizando `next/image`.
 * 4. Si `graphData` existe pero no se cumplen las condiciones anteriores para mostrar una imagen
 *    o un grafo (ej. no hay `nodes` ni `image_url` válidos): Muestra un mensaje
 *    "No hay datos de gráfico para mostrar...".
 *
 * Características Adicionales:
 * - Determina un `pathwayDisplayName` a partir de las propiedades de `graphData`.
 * - Aplica estilos personalizados a los nodos y aristas del grafo de Cytoscape.js.
 */

'use client';
import React from 'react';
import Image from 'next/image';
import { KeggPathwayGraphData } from '../types/keggTypes';
import CytoscapeComponent from 'react-cytoscapejs'; 

interface KeggPathwayGraphDisplayProps {
    graphData: KeggPathwayGraphData | null | undefined;
}

const KeggPathwayGraphDisplay: React.FC<KeggPathwayGraphDisplayProps> = ({ graphData }) => {

    if (!graphData) {
        return <p className="p-4 text-gray-500 text-center">Esperando datos del pathway...</p>;
    }

    const pathwayDisplayName = graphData.name || graphData.pathwayName || graphData._id || 'Pathway Desconocido';
    
    const imageUrlToDisplay = graphData.image_url || graphData.pathwayImageUrl;

    const hasCytoscapeData = graphData.nodes && graphData.nodes.length > 0;

    if (graphData.image_url && (!graphData.nodes || graphData.nodes.length === 0)) {
        return (
            <div>
                <img 
                    src={graphData.image_url} 
                    alt={`KEGG Pathway: ${graphData.name || graphData._id}`}
                    className="w-full h-auto border rounded"
                />
            </div>
        );
    }

    
    if (graphData.pathwayImageUrl && (!graphData.nodes || graphData.nodes.length === 0)) {
    
        // Mostrar imagen si está disponible 
        return (
            <div>
                <img src={graphData.pathwayImageUrl} alt={`KEGG Pathway: ${graphData.pathwayName}`}
className="w-full h-auto border rounded"/>

            </div>
        );
    }

    // Usar Cytoscape si hay datos de nodos y ejes
    if (graphData.nodes && graphData.nodes.length > 0) {
        const elements = CytoscapeComponent.normalizeElements({
            nodes: graphData.nodes.map(node => ({ data: { id: node.id, label: node.label, type: node.type } })),
            edges: graphData.edges.map(edge => ({ data: { source: edge.source, target: edge.target, label: edge.label, type: edge.type } })),
        });

        // Estilos para Cytoscape 
        const stylesheet = [
            {
                selector: 'node',
                style: {
                    'label': 'data(label)',
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'font-size': '10px',
                    'width': '60px',
                    'height': '30px',
                    'shape': 'round-rectangle',
                    'background-color': '#ADD8E6', // Light blue
                    'border-width': '1px',
                    'border-color': '#0074D9'    // Darker blue
                },
            },
            { //      Estilos para diferentes tipos de nodos
                selector: 'node[type="gene"]',
                style: { 'background-color': '#90EE90' } // Light green for genes
            },
            {
                selector: 'node[type="compound"]',
                style: { 'background-color': '#FFB6C1', 'shape': 'ellipse', 'width': '20px', 'height': '20px' } // Light pink for compounds
            },
            {
                selector: 'node[type="map"]',
                style: { 'background-color': '#FFFFE0', 'border-style': 'dashed' } // Light yellow for map links
            },
            {
                selector: 'edge',
                style: {
                    'width': 1,
                    'line-color': '#ccc',
                    'target-arrow-color': '#ccc',
                    'target-arrow-shape': 'triangle',
                    'curve-style': 'bezier',
                    'label': 'data(label)', // Mostrar etiqueta de la arista si existe
                    'font-size': '8px',
                    'text-rotation': 'autorotate',
                    'text-margin-y': -5
                },
            },
        ];
   
    return (
        <div className="pathway-visualization space-y-6 p-1"> {/* Añadí un pequeño padding general */}
        {/* Sección para la Imagen Estática de KEGG */}
        {imageUrlToDisplay && (
            <section className="kegg-static-image-section">
                <h3 className="text-lg font-semibold text-gray-800 mb-2">Imagen de Referencia KEGG</h3>
                <div className="border border-gray-300 rounded-lg overflow-hidden shadow-md bg-white">
                    <Image
                        src={imageUrlToDisplay}
                        alt={`Imagen de KEGG para el pathway ${pathwayDisplayName}`}
                        width={800} 
                        height={600} 
                        layout="responsive" 
                    />
                </div>
                <p className="text-xs text-gray-500 mt-1 text-center">
                    <a 
                        href={imageUrlToDisplay} 
                        target="_blank" 
                        rel="noopener noreferrer" 
                        className="text-blue-600 hover:text-blue-800 hover:underline"
                    >
                        Ver imagen original en KEGG
                    </a>
                </p>
            </section>
        )}

        {/* Separador si ambas visualizaciones están presentes y hay datos para ambas */}
        {imageUrlToDisplay && hasCytoscapeData && <hr className="my-6 border-gray-300"/>}

        {/* Sección para el Grafo Interactivo Cytoscape */}
                
       {hasCytoscapeData && (
            <section className="kegg-interactive-graph-section">
                <h3 className="text-lg font-semibold text-gray-800 mb-2">Grafo Interactivo</h3>
                <div 
                    style={{ height: '600px', width: '100%', border: '1px solid #cbd5e1', borderRadius: '0.5rem' }} 
                    className="shadow-md bg-white overflow-hidden" // overflow-hidden para que Cytoscape no se salga
                >

                    <CytoscapeComponent
                        elements={elements}
                        style={{ width: '100%', height: '100%' }}
                        layout={{ name: 'cose', idealEdgeLength: 100, nodeRepulsion: 400000, animate: true }} // 'cose' es un buen layout general
                        stylesheet={stylesheet}
                    />
                </div>
            </section>   
       )}
    </div>    
    );

    }
    return <p>No hay datos de gráfico para mostrar para {graphData.pathwayName}.</p>;
};

export default KeggPathwayGraphDisplay;

