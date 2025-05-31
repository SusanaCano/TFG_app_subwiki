// src/features/kegg/context/PathwayContext.tsx

/**
* @file PathwayContext.tsx
* @description Contexto para gestionar el ID del pathway de KEGG actualmente seleccionado
* para visualización detallada (ej. un gráfico).
*/


'use client';

import React, { createContext, useContext, useState, ReactNode } from 'react';

interface PathwayContextType {
    pathwayId: string | null;
    setPathwayId: (id: string | null) => void;
    pathwayName?: string | null; //  para mostrar el nombre del pathway seleccionado
    setPathwayName?: (name: string | null) => void; 
}

const PathwayContext = createContext<PathwayContextType | undefined>(undefined);

export const usePathway = () => {
    const context = useContext(PathwayContext);
    if (!context) {
        throw new Error('usePathway must be used within a PathwayProvider');
    }
    return context;
};

export const PathwayProvider = ({ children }: { children: ReactNode }) => {
    const [pathwayId, setPathwayId] = useState<string | null>(null);
    const [pathwayName, setPathwayName] = useState<string | null>(null); 
    const handleSetPathwayId = (id: string | null) => {
        setPathwayId(id);
        if (!id) { // Si se limpia el ID, limpiar el nombre también
            setPathwayName(null);
        }
        
    };

    const handleSetPathwayName = (name: string | null) => { 
        setPathwayName(name);
    }

    return (
        <PathwayContext.Provider value={{ pathwayId, setPathwayId: handleSetPathwayId, pathwayName, setPathwayName: handleSetPathwayName }}>
            {children}
        </PathwayContext.Provider>
    );
};