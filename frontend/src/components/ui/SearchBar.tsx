// src/components/ui/SearchBar.tsx

/**
 * @file SearchBar.tsx
 * @description Componente de interfaz de usuario que proporciona una caja de búsqueda
 * con un campo de entrada y un botón de envío.
 * 
 * Funcionalidad:
 * - Mantiene un estado local (`localQuery`) para el valor del campo de entrada.
 * - Al enviar el formulario (presionar "Buscar" o Enter):
 *   - Previene el comportamiento por defecto del formulario.
 *   - Obtiene el término de búsqueda (`localQuery.trim()`).
 *   - Utiliza el hook `useSearchQuery` para actualizar el estado global `searchQuery`
 *     en `SearchQueryContext` con el nuevo término.
 * 
 * Este componente no realiza la búsqueda directamente, sino que delega la actualización
 * del término de búsqueda al contexto global, permitiendo que otros componentes
 * (como `GenesSearchPage`) reaccionen a este cambio.
 */

'use client'

import { useState } from 'react';
import { useSearchQuery } from '@/contexts/SearchQueryContext'; 


const SearchBar = () => {
  const [localQuery, setLocalQuery] = useState('');
  const { setSearchQuery } = useSearchQuery(); 

  const handleSubmit = async (e: React.FormEvent) => { // Inicio del ámbito de handleSubmit
    e.preventDefault();
    // USO de localQuery dentro de handleSubmit
    const searchTerm = localQuery.trim(); 

    if (searchTerm) {
      console.log(`SearchBar: Setting global searchQuery to: ${searchTerm}`);
      setSearchQuery(searchTerm); // <--- ESTO ACTUALIZA EL CONTEXTO PARA UNIPROT/GenesSearchPage

    // Opcional: Si la misma búsqueda debe aplicar a KEGG
    // console.log(`SearchBar: Setting global genId (KEGG) to: ${searchTerm}`);
    // setGenId(searchTerm);
    } else {
      console.log('La búsqueda está vacía');
      setSearchQuery(''); // Limpia el contexto de UniProt
    // setGenId(null); // Limpia el contexto de KEGG
    }
  };




  return (
    <form onSubmit={handleSubmit} className="flex items-center">
      <input
        type="text"
        value={localQuery}
        onChange={(e) => setLocalQuery(e.target.value)}
        placeholder="Buscar genes (ej. BC_0002, Q814F1,....)"
        className="w-full sm:w-96 p-3 border border-gray-300 rounded-lg text-lg"
      />
      <button
        type="submit"
        className="ml-2 p-3 bg-blue-500 text-white rounded-lg text-lg" // Ajuste de padding y font size
      >
        Buscar
      </button>
    </form>
  );
};

export default SearchBar;
/** 
import { useState } from 'react';
import { useGen } from '../features/kegg/context/GenContext';
import { useRouter } from 'next/navigation';


type SearchBarProps = {
  onSearch: (query: string) => void;
};

const SearchBar = ({ onSearch }: SearchBarProps) => {
  const [query, setQuery] = useState('');
  const { setGenId } = useGen(); 
  const router = useRouter();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault(); // Prevenimos que el formulario recargue la página
    
    if (query.trim()) {
      setGenId(query); // Verificamos si la búsqueda no está vacía
      onSearch(query);  // Llamamos a la función onSearch pasándole la query
      router.push(`/features/kegg/${query.trim()}`); 
    } else {
      console.log('La búsqueda está vacía'); // Si está vacía, mostramos un mensaje
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex items-center">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}  // Actualizamos el estado con lo que se escribe en el input
        placeholder="Buscar..."
        //className="border p-2 rounded"
        className="w-full sm:w-96 p-3 border border-gray-300 rounded-lg text-lg"
      />
      <button 
        type="submit"
        className="ml-2 p-2 bg-blue-500 text-white rounded"
      >
        Buscar
      </button>
    </form>
  );
};

export default SearchBar;

*/