// src/app/features/kegg/components/ClientWrapper.tsx
'use client';

import KeggGraphContainer from "./keggGraph/keggGraphContainer";


interface ClientWrapperProps {
    genId: string;
  }
  
  const ClientWrapper: React.FC<ClientWrapperProps> = ({ genId }) => {
    return <KeggGraphContainer genId={genId} />;
  };
  
  export default ClientWrapper;
