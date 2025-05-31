import { useState } from 'react';
import Header from '..//components/Header';
import SearchBar from '..//components/SearchBar';
import ResultList from '../components/ResultList';

export default function Home() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (query) => {
    setLoading(true); 
    /*
    handleSearch se encarga de hacer la solicitud al backend (FastAPI) cuando el usuario presiona el botón de búsqueda.
    */
    try {
      //const response = await fetch(`/api/search?query=${query}`); // enviar solicitud al backend
      const response = await fetch(`http://localhost:8000/search?query=${searchTerm}`);
      const data = await response.json();
      setResults(data.results);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
   
  };

  return (
    <>
      <Header />
      <main style={{ padding: '20px' }}>
        <SearchBar onSearch={handleSearch} />
        {loading ? <p>Cargando...</p> : <ResultList results={results} />}
      </main>
    </>
  );

}
