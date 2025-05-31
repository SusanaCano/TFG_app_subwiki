// src/components/layout/Navigation.tsx

'use client'

import Link from 'next/link'
import styles from './Navigation.module.css'
//import PropTypes from 'prop-types'; // Importa PropTypes
//import { useRouter } from 'next/navigation';
//import { useState } from 'react';
import { useSelectedGen  } from '@/features/kegg/context/GenContext'; 



/*
const links = [{
    label: 'Home',
    route: '/'
}, {
    label: 'Home',
    route: '/src/app/home'
}, {
    label: 'Proteinas',
    route: '/src/proteinas'
}, {
    label: 'Resultados Proteinas',
    route: '/src/resultadosProteinas'
}]
*/

// Define el tipo para las props
/*interface NavigationProps {
    children?: React.ReactNode;
  }*/
  
  interface NavigationProps {
    children?: React.ReactNode;
  }
  

export function Navigation ({ children }: NavigationProps) {
    // Usa el hook renombrado y desestructura 'selectedGen'
    const { selectedGen } = useSelectedGen();

    // El 'genId' para el enlace será el 'userInput' del contexto, que era como "BC_0002"
    const genIdForLink = selectedGen.userInput;

    const baseLinks = [
        { label: 'Home', route: '/' },
       // { label: 'Home', route: '/src/app/home' },
        { label: 'Proteinas', route: '/proteinas' },
        //{ label: 'Rutas metabólicas', route: `/features/kegg/s$[genId]` },
      ];
// 
    return (
        <nav className={styles.container || ''}>
      
          <ul className={styles.navigationList || ''}>
            {baseLinks.map(({ label, route }) => (
              <li key={route} className={styles.navigationItem || ''}>
 
                <Link href={route} className={styles.link || ''}>
                  {label}
                </Link>
              </li>
            ))}

            {/* Renderiza el enlace a Rutas Metabólicas CONDICIONALMENTE y DINÁMICAMENTE */}
            {/* {genId && (
              <li>
                <Link href={`/features/kegg/${genId}`}>Rutas metabólicas</Link>
              </li>
            )}
           */}
                
            {genIdForLink ? ( // Solo muestra este enlace si genIdForLink (selectedGen.userInput) tiene un valor
              <li key={`kegg-${genIdForLink}`} className={styles.navigationItem || ''}>
                <Link href={`/features/kegg/${encodeURIComponent(genIdForLink)}`} className={styles.link || ''}>
                  Rutas Metabólicas ({selectedGen.displayName || genIdForLink}) {/* Muestra un nombre legible o el ID */}
                </Link>
              </li>

            ) : (
              // Opcional: mostrar algo si no hay genId seleccionado
              <li key="kegg-disabled" className={styles.navigationItem || ''}>
                <span className={styles.disabledLink || ''} style={{ color: 'grey', cursor: 'not-allowed' }}>
                
                  Rutas Metabólicas (seleccione gen)
              
                </span>
              </li>
            )}

          </ul>
            
          {children && <div>{children}</div>} {/* Renderiza children si están presentes */}
        </nav>
    );
    
}

