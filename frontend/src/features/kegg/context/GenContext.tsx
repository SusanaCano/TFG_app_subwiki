// frontend/src/features/kegg/contex/GenContext.tsx



'use client';

import React, {
  createContext,
  useContext,
  useState,
  type ReactNode,
} from 'react';



// Información más completa sobre el gen seleccionado/buscado
export interface SelectedGenInfo {
  userInput: string | null;        // Lo que el usuario escribió (ej: "BC_XXXX")
  uniprotId?: string | null;       // ID de UniProt resuelto (ej: "QXXXX")
  keggGeneId: string | null;      // ID de gen KEGG para grafos (ej: "bce:BCXXXXX") 
  displayName?: string | null;     // Nombre para mostrar (ej: "BC_XXXX" o nombre de la proteína)
  
}

interface GenContextType {
  selectedGen: SelectedGenInfo;
  setSelectedGen: (genInfo: SelectedGenInfo | null) => void; //  limpiar todo el objeto
}


const GenContext = createContext<GenContextType | undefined>(undefined);

// Hook personalizado para usar el contexto (recomendado)

export const useSelectedGen = () => {
  const context = useContext(GenContext);
  if (context === undefined) {
    throw new Error('useSelectedGen must be used within a GenProvider');
  }
  return context;
}


export const GenProvider = ({ children }: { children: ReactNode }) => {
  const [selectedGen, setSelectedGenState] = useState<SelectedGenInfo>({
    userInput: null,
    uniprotId: null,
    keggGeneId: null,
    displayName: null,
  });

  const handleSetSelectedGen = (genInfo: SelectedGenInfo | null) => {
    if (genInfo === null) {
      setSelectedGenState({ // Estado inicial/limpio
        userInput: null,
        uniprotId: null,
        keggGeneId: null,
        displayName: null,
      });
    } else {
      setSelectedGenState(genInfo);
    }
  };

  return (
    <GenContext.Provider value={{ selectedGen, setSelectedGen: handleSetSelectedGen }}>
      {children}
    </GenContext.Provider>
  );
};

