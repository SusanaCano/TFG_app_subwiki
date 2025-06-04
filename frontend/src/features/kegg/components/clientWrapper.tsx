// src/app/features/kegg/components/ClientWrapper.tsx

/**
 * @file ClientWrapper.tsx
 * @description Componente de React (marcado con 'use client') que actúa como un
 *              envoltorio simple para el componente `KeggGraphContainer`.
 *              Su propósito principal es asegurar que `KeggGraphContainer` y su
 *              lógica de cliente (como la obtención de datos) se ejecuten
 *              en el lado del cliente dentro del ecosistema de Next.js App Router.
 *
 * Props:
 * - `genId` (string): El identificador del gen. Esta prop se pasa directamente
 *                     al componente `KeggGraphContainer` anidado.
 *
 * Funcionalidad:
 * - Recibe la prop `genId`.
 * - Renderiza el componente `KeggGraphContainer`, pasándole el `genId` recibido.
 * - No añade ninguna lógica o UI adicional propia, su función es puramente
 *   de encapsulación y de establecer un límite de cliente.
 */

'use client';

import KeggGraphContainer from "./keggGraph/keggGraphContainer";


interface ClientWrapperProps {
    genId: string;
  }
  
  const ClientWrapper: React.FC<ClientWrapperProps> = ({ genId }) => {
    return <KeggGraphContainer genId={genId} />;
  };
  
  export default ClientWrapper;
