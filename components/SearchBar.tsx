'use client';

import { useState } from 'react';

interface SearchBarProps {
  onSearch: (query: string) => void; 
}

const SearchBar = ({ onSearch }: SearchBarProps) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(query);  // Llamamos a la función onSearch pasándole la query
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}  // Actualizamos el estado con lo que se escribe en el input
        placeholder="Ingresa tu búsqueda"
        className="border p-2 rounded"
      />
      <button type="submit">Buscar</button>
    </form>
  );
};

export default SearchBar;
