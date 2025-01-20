// app/resultadosProteinas/page.jsx

/*
El servidor (backend) realiza la consulta a la BD y devuelve un .json al frotend
*/
/*
import { GetServerSideProps } from 'next';

export default function ResultadosProteinasPage({ proteinas }) {
    return (
        <div>
            <h1>Proteinas resultantes de la busqueda </h1>
            {proteinas.length > 0 ? (
                <ul>
                    {proteinas.map((proteina) => (
                        <li key={proteina._id}>
                            <h2>{proteina.name}</h2>
                            <p>{proteina.body}</p>
                        </li>
                    ))}
                </ul>
            ) : (
                <p>No se han obtenido resultados </p>
            )}
        </div>
    );
}

// Esto se ejecuta en el servidor antes de renderizar el componente
export const getServerSideProps: GetServerSideProps = async () => {
    try {
        const response = await fetch('http://localhost:3000/api/posts');  // Realiza la consulta al backend
        const proteinas = await response.json();  // Obtiene las proteinas en formato JSON

        return { props: { proteinas } };  // Pasa los datos como props al componente
    } catch (error) {
        console.error(error);
        return { props: { proteinas: [] } };  // Si hay un error, pasa un arreglo vacío
    }
};
*/// Ejemplo de un componente en Next.js que obtiene datos del backend
import { useEffect, useState } from 'react';

const Resultados = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    // Hacer una solicitud a la API de FastAPI para obtener los resultados
    const obtenerDatos = async () => {
      const response = await fetch('http://localhost:8000/consulta');
      const result = await response.json();
      setData(result.data);  // Suponiendo que FastAPI devuelve la respuesta en un campo 'data'
    };

    obtenerDatos();
  }, []);

  if (!data) {
    return <div>Cargando...</div>;
  }

  return (
    <div>
      <h1>Resultados</h1>
      <table>
        <thead>
          <tr>
            <th>Protein Description</th>
            <th>Gene Name</th>
            <th>Ordered Locus Name</th>
            <th>Sequence Value</th>
            <th>Length</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={index}>
              <td>{item.proteinDescription}</td>
              <td>{item.genes.map(gene => gene.gene?.name).join(', ')}</td>
              <td>{item.genes.map(gene => gene.orderedLocusName?.value).join(', ')}</td>
              <td>{item.genes.map(gene => gene.sequence?.value).join(', ')}</td>
              <td>{item.genes.map(gene => gene.length).join(', ')}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Resultados;
