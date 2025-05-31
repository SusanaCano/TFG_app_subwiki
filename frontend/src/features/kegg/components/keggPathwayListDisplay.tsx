// src/features/kegg/components/KeggPathwayListDisplay.tsx

/**
 * @file KeggPathwayListDisplay.tsx
 * @description Muestra una lista de rutas KEGG. Al hacer clic en una,
 * actualiza el PathwayContext para disparar la visualización del gráfico.
*/

'use client';

import React from 'react';
import { KeggPathwayEntry } from '../types/keggTypes';
import { usePathway } from '../context/PathwayContext'; // Importa el hook del PathwayContext

interface KeggPathwayListDisplayProps {
    pathways: KeggPathwayEntry[];
}

const KeggPathwayListDisplay: React.FC<KeggPathwayListDisplayProps> = ({ pathways }) => {
    const { setPathwayId, pathwayId: selectedPathwayId, setPathwayName } = usePathway(); // Usa el contexto
    const handlePathwaySelect = (pathway: KeggPathwayEntry) => {
        console.log('[KeggPathwayListDisplay] Pathway selected: ${pathway.pathway_id} - ${pathway.pathway_name}');

        setPathwayId(pathway.pathway_id);

        if (setPathwayName) setPathwayName(pathway.pathway_name); // Guarda el nombre también
    };

    if (!pathways || pathways.length === 0) {
        return <p>No hay rutas para mostrar.</p>; 
    }

    return (
        <div className="space-y-2">

            {pathways.map((pathway) => (
                <button 
                    key={pathway.pathway_id} 
                    onClick={() => handlePathwaySelect(pathway)}
                    className={`w-full text-left px-4 py-2 border rounded-md transition-colors ${
                        selectedPathwayId === pathway.pathway_id  
                        ? 'bg-blue-500 text-white border-blue-600 ring-2 ring-blue-300' 
                        : 'bg-white hover:bg-gray-100 border-gray-300 text-gray-700'
                    }`}
                    title={`Visualizar detalles de la ruta ${pathway.pathway_name}`}>

                    <span className="font-medium">{pathway.pathway_name}</span>
                    <span className="text-xs ml-2 text-gray-500 group-hover:text-gray-700">({pathway.pathway_id})</span>
                
                </button>
            ))}
        </div>
    );
};

export default KeggPathwayListDisplay;