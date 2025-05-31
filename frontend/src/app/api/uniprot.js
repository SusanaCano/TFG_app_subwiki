export default async function handler(req, res) {
    if (req.method !== 'GET') {
        return res.status(405).json({ error: 'Método no permitido' });
    }

    const { query } = req.query;
    if (!query) {
        return res.status(400).json({ error: 'Falta el parámetro de búsqueda' });
    }

    try {
        // URL de la API de UniProt
        const url = `https://rest.uniprot.org/uniprotkb/search?query=${encodeURIComponent(query)}&format=json`;

        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Error en la API de UniProt: ${response.statusText}`);
        }

        const data = await response.json();
        res.status(200).json(data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
}
