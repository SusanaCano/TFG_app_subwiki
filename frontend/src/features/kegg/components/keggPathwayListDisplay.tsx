// src/features/kegg/components/KeggPathwayListDisplay.tsx

/**
 * @file KeggPathwayListDisplay.tsx
 * @description Componente de React (Next.js 'use client') que renderiza una lista
 *              interactiva de rutas metabólicas de KEGG (`KeggPathwayEntry`).
 *              Permite al usuario seleccionar una ruta de la lista.
 *
 * Props:
 * - `pathways` (KeggPathwayEntry[]): Un array de objetos `KeggPathwayEntry`,
 *   cada uno representando una ruta metabólica con su ID y nombre.
 *
 * Funcionalidad:
 * - Muestra un mensaje "No hay rutas para mostrar" si el array `pathways`
 *   está vacío o no se proporciona.
 * - Renderiza cada ruta metabólica como un botón clickeable.
 * - Al hacer clic en un botón de ruta:
 *   - Llama a `setPathwayId` del `PathwayContext` (obtenido mediante `usePathway`)
 *     para actualizar el ID de la ruta seleccionada globalmente.
 *   - Llama a `setPathwayName` del `PathwayContext` (si está disponible) para
 *     actualizar el nombre de la ruta seleccionada globalmente.
 * - Estiliza visualmente la ruta actualmente seleccionada (basándose en `selectedPathwayId`
 *   del contexto) para diferenciarla de las demás.
 * - Muestra el nombre y el ID de cada ruta.
 *
 * Este componente es clave para la interacción del usuario, permitiéndole elegir qué
 * ruta metabólica desea visualizar en detalle en otros componentes que
 * consumen el `PathwayContext`.
 */

'use client';

import React from 'react';
import { KeggPathwayEntry } from '../types/keggTypes';
import { usePathway } from '../context/PathwayContext'; // Importa el hook 

interface KeggPathwayListDisplayProps {
    pathways: KeggPathwayEntry[];
}

const KeggPathwayListDisplay: React.FC<KeggPathwayListDisplayProps> = ({ pathways }) => {
    const { setPathwayId, pathwayId: selectedPathwayId, setPathwayName } = usePathway(); // Usa el contexto
    const handlePathwaySelect = (pathway: KeggPathwayEntry) => {
        console.log('[KeggPathwayListDisplay] Pathway selected: ${pathway.pathway_id} - ${pathway.pathway_name}');

        setPathwayId(pathway.pathway_id);

        if (setPathwayName) setPathwayName(pathway.pathway_name); // Guarda el nombre 
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