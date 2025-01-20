import { useState } from 'react';
import Header from '../../../components/Header';
import SearchBar from '../../../components/SearchBar';
import ResultList from '../../../components/ResultList';

export default function Home() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (query) => {
    setLoading(true); //activar el indicador de carga
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
    //setResponse(data);  // Almacenar la respuesta para mostrarla
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
  /*
    // segun chatgpt
      return (
    <div>
      <h1>Buscar en UniProt</h1>
      <input
        type="text"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        placeholder="Introduce tu búsqueda"
      />
      <button onClick={handleSearch}>Buscar</button>

      <div>
        {response && <pre>{JSON.stringify(response, null, 2)}</pre>}
      </div>
    </div>
  );
};

export default Home;
  */
}
