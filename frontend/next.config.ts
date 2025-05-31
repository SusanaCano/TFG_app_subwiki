import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  eslint: {
    // ADVERTENCIA: Esto desactiva ESLint durante el build.
    // Úsalo solo para depuración o si estás seguro de que el linting se hace en otro paso.
    ignoreDuringBuilds: true,
  },

  reactStrictMode: true, // o lo que tengas
  images: {
    remotePatterns: [
      {
        protocol: 'http', // KEGG usa http para sus imágenes de pathways
        hostname: 'www.kegg.jp',
        port: '', // Dejar vacío si es el puerto por defecto (80 para http)
        pathname: '/kegg/pathway/**', // Permite cualquier ruta dentro de /kegg/pathway/
      },
    ],
  },
};

export default nextConfig;
