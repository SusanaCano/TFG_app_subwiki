# tests/test_descarga_uniprot.py

'''
Tests para el módulo de descarga de datos desde UniProt.

- test_obtener_numero_entradas: Verifica que se obtiene correctamente el número total de entradas
  disponibles para una consulta específica a UniProt.

- test_descargar_datos_uniprot: Comprueba que se descargan correctamente un número determinado
  de entradas (en este caso 500 entradas por bloque) desde la API de UniProt en formato JSON.
'''

import unittest
from Uniprot.descargas_datos_uniprot import descargar_datos_uniprot, obtener_numero_entradas


class TestDescargaUniProt(unittest.TestCase):

    def test_obtener_numero_entradas(self):
        query = "organism_id:226900"
        total = obtener_numero_entradas(query)
        self.assertIsInstance(total, int)
        self.assertGreater(total, 0)

    def test_descargar_datos_uniprot(self):
        query = "organism_id:226900"
        datos = descargar_datos_uniprot(query, limit=2, offset=0)
        self.assertIsNotNone(datos)
        self.assertIn('results', datos)
        self.assertIsInstance(datos['results'], list)
        self.assertLessEqual(len(datos['results']), 2)

if __name__ == '__main__':
    unittest.main()
