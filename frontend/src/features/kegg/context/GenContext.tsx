// frontend/src/features/kegg/contex/GenContext.tsx

/**
 * @file GenContext.tsx
 * @description Define un contexto de React (`GenContext`) y su proveedor (`GenProvider`)
 *              para gestionar el estado de un "gen seleccionado" a través de la aplicación.
 *              Este contexto permite compartir información detallada sobre un gen específico
 *              entre diferentes componentes.
 *
 * Funcionalidad:
 * - `SelectedGenInfo` (interfaz): Define la estructura de la información del gen seleccionado,
 *   incluyendo el input del usuario, ID de UniProt (opcional), ID de gen KEGG y un nombre
 *   para mostrar (displayName).
 * - `GenContext`: El objeto de contexto de React.
 * - `GenProvider` (componente): Proveedor que encapsula la lógica de estado para `selectedGen`.
 *   - Mantiene el estado `selectedGen` (un objeto `SelectedGenInfo`).
 *   - Expone `selectedGen` (el estado actual) y `setSelectedGen` (una función para actualizarlo).
 *   - `setSelectedGen` puede recibir un objeto `SelectedGenInfo` para establecer un nuevo gen,
 *     o `null` para restablecer el estado a sus valores iniciales/nulos.
 * - `useSelectedGen` (hook personalizado): Hook para consumir fácilmente el `GenContext`.
 *   Asegura que el hook se utiliza dentro de un `GenProvider` y lanza un error si no es así.
 *
 * Uso:
 * Envolver los componentes que necesitan acceso al gen seleccionado con `<GenProvider>`.
 * Luego, usar el hook `useSelectedGen()` dentro de esos componentes para acceder a
 * `selectedGen` y `setSelectedGen`.
 */

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

