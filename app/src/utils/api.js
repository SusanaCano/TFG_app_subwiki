import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL, // Configurado desde .env.local
  headers: { Authorization: `Bearer ${process.env.NEXT_PUBLIC_API_KEY}` },
});

export default api;
