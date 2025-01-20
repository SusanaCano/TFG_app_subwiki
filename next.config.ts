//import type { NextConfig } from "next";

//const nextConfig: NextConfig = {
  /* config options here */
 // reactStrictMode: true
//};

//export default nextConfig;]

// frontend/next.config.js

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/:path*', // Redirige /api a FastAPI
      },
    ];
  },
};

module.exports = nextConfig;
