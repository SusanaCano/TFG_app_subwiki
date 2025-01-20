// frontend/components/DescargarDatos.tsx

/*
Obtenemos la informacion de la caja de busqueda del frontend, en este caso Bacillus cereus, que va a ser 
el parametro que se le pasa al backend.
Luego lo agregamos a la logica del proyecto en page.tsx raiz
*/

/*import React, { useState } from 'react';

const DescargarDatos = ({ onResultado }) => {
  const [query, setQuery] = useState('');
  const [mensaje, setMensaje] = useState('');

  const handleInputChange = (e) => {
    setQuery(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('/descargar_json', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query,
          limit: 100,
          total: 500,
          delay: 2,
        }),
      });

      if (!response.ok) {
        throw new Error('Error en la descarga de los datos');
      }

      const data = await response.json();
      setMensaje(data.message);
      if (onResultado) {
        onResultado(data.message);
      }
    } catch (error) {
      setMensaje('Hubo un error al descargar los datos');
      console.error('Error al descargar los datos:', error);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label htmlFor="query">Buscar Query:</label>
        <input
          type="text"
          id="query"
          value={query}
          onChange={handleInputChange}
          placeholder="Ingresa el query"
        />
        <button type="submit">Descargar</button>
      </form>

      {mensaje && <p>{mensaje}</p>}
    </div>
  );
};

export default DescargarDatos;
*/
// frontend/components/DescargarDatos.tsx

'use client';
import React from 'react';

interface DescargarDatosProps {
  onResultado: (mensaje: string) => void;
}

const DescargarDatos: React.FC<DescargarDatosProps> = ({ onResultado }) => {
  const manejarDescarga = async () => {
    try {
      const respuesta = await fetch('/api/descargar', {
        method: 'POST',
      });

      if (respuesta.ok) {
        const data = await respuesta.json();
        onResultado(`Datos descargados correctamente: ${data.mensaje}`);
      } else {
        onResultado('Error al descargar los datos.');
      }
    } catch (error) {
      console.error('Error:', error);
      onResultado('Error al conectar con el servidor.');
    }
  };

  return (
    <button onClick={manejarDescarga} className="bg-blue-500 text-white px-4 py-2 rounded">
      Descargar Datos
    </button>
  );
};

export default DescargarDatos;
