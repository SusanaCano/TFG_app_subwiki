// pages/api/descargar.ts (o .js si no usas TypeScript)
import { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    // Aquí va tu lógica de descarga
    res.status(200).json({ message: 'Descarga iniciada' });
  } else {
    res.status(405).json({ message: 'Método no permitido' });
  }
}
