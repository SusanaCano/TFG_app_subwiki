// src/ app/ layout.tsx

/**
 * @file layout.tsx
 * @description Componente raíz del layout de la aplicación Next.js.
 * Define la estructura HTML base (<html>, <body>) y envuelve todo el contenido
 * de la aplicación.
 * 
 * Responsabilidades:
 * - Configurar metadatos globales para la aplicación.
 * - Aplicar fuentes y estilos globales al `<body>`.
 * - Envolver el contenido principal (`children`) con `AppProviders` para asegurar
 *   que todos los contextos globales (como `SearchQueryContext`) estén disponibles
 *   para las páginas y componentes de la aplicación.
 * - Renderizar componentes estructurales comunes como `Header`, `Navigation` y `Footer`
 *   que aparecerán en todas las páginas.
 * - `children` representa el contenido específico de la página que se está renderizando.
 */

import type { Metadata } from 'next'; 
import { siteMetadata } from './metadata'; 
import localFont from 'next/font/local';
import '@/styles/globals.css';
import {Navigation} from '@/components/layout/Navigation';
import Footer from '@/components/layout/Footer';
import Header from  '@/components/layout/Header';
import { AppProviders } from '@/providers/AppProviders';

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export const metadata: Metadata = siteMetadata;

export default function RootLayout({
  children, // Este 'children' es el contenido de la página actual (ej. app/page.tsx)
}: Readonly<{
  children: React.ReactNode;
}>) {

  return (
    <html lang="es" suppressHydrationWarning>
      
       {/*
      <head>
        <title> App web </title>
      </head>
      */}
      <body
        className={`${geistSans.variable} ${geistMono.variable}  antialiased flex flex-col min-h-screen bg-background text-foreground`} 
      >
        <AppProviders> 

          <div className="flex flex-col min-h-screen">
          
            <Header />
            <Navigation />

            <main className="flex-grow container mx-auto p-4 w-full">
            
              {children}
          
            </main>

            <Footer />
        
          </div>

        </AppProviders>
       
       {/* subWiki */}

      </body>
    </html>
  );
}
