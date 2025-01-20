'use client'

import Image from "next/image";
import Link from "next/link";
import { useState, useEffect } from 'react';
import styles from '../styles/SearchBar.module.css';
import SearchBar from "../components/SearchBar";
import Resultados from '../components/Resultados';
import DescargarDatos from '../components/DescargarDatos';  // Importar el componente

export default function Home() {
  /*
   // Definimos la función `handleSearch` que será pasada como `onSearch`.
  const handleSearch = (query: string) => {
    console.log("Realizando búsqueda con:", query);
    // Aquí puedes realizar la lógica de búsqueda, como una solicitud a tu backend.
  };

  */

 
    const [resultado, setResultado] = useState('');  // Estado para mostrar el mensaje de resultado
     
    // Definimos la función `handleSearch` que será pasada como `onSearch`
    const handleSearch = (query: string) => {
      console.log("Realizando búsqueda con:", query);
      // Aquí puedes realizar la lógica de búsqueda, como una solicitud a tu backend.
    };

    // Definimos la función `manejarResultado` que será pasada como `onResultado`
     const manejarResultado = (mensaje) => {
      setResultado(mensaje);  // Guardar el mensaje de respuesta para mostrarlo en la UI
    };

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
        <div style={{ padding: "20px" }}>
          <h1>Bienvenido a la Página Principal</h1>
          <Link href="/about">Ir a About</Link>
        </div>

        <div className={styles.shape} />

        <div>
          <h1>Buscar en UniProt</h1>

          {/* Pasamos `handleSearch` como prop `onSearch` */}
          
          {/*<SearchBar onSearch={handleSearch} />*/}
          
          {/* Caja roja para verificar si el componente se renderiza */}
          {/*<div style={{ backgroundColor: 'red' }}>*/}
            <SearchBar onSearch={handleSearch} />
          {/*</div>*/}

          {/* Llamada al componente para realizar la descarga */}
          <DescargarDatos onResultado={manejarResultado} />

          {/* Mostrar el mensaje de resultado */}
          {resultado && <p>{resultado}</p>} 
        
        </div>
      </main>
      <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center">
            RESULTADOS
            <div>

            </div>
      </footer>
    </div>
  );
}
