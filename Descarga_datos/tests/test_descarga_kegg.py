# tests/test_descarga_kegg.py

'''
Tests para el módulo de descarga de datos desde KEGG.

Este archivo contiene pruebas unitarias para comprobar el correcto funcionamiento
de las funciones del módulo 'descargas_datos_kegg.py'.

Clases y tests incluidos:
- TestKeggDownloader:
    - test_obtener_ids_kegg: Verifica que se obtienen correctamente los IDs de rutas
      KEGG desde una consulta de organismo.
    - test_descargar_entradas_kegg: Comprueba que se descargan correctamente las
      entradas asociadas a los IDs y que se almacenan en archivos JSON.
'''

import unittest
from unittest.mock import patch, MagicMock
import os
import shutil
import json
from Kegg.descargas_datos_kegg import obtener_ids_kegg, descargar_entradas_kegg  
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class TestKeggDownloader(unittest.TestCase):

    def setUp(self):
        self.test_output_dir = "test_kegg_output"
        if os.path.exists(self.test_output_dir):
            shutil.rmtree(self.test_output_dir)

    def tearDown(self):
        if os.path.exists(self.test_output_dir):
            shutil.rmtree(self.test_output_dir)

    @patch("requests.get")
    def test_obtener_ids_kegg(self, mock_get):
        # Simula la respuesta de KEGG
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "bce00010\tGlycolysis / Gluconeogenesis - Bacillus cereus\nbce00020\tCitrate cycle - Bacillus cereus"
        mock_get.return_value = mock_response

        ids = obtener_ids_kegg("bce")
        self.assertEqual(ids, ["bce00010", "bce00020"])
        mock_get.assert_called_once_with("http://rest.kegg.jp/list/bce")

    @patch("requests.get")
    def test_descargar_entradas_kegg(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = (
            "ENTRY       bce00010  Pathway\nNAME        Glycolysis\n///\n"
            "ENTRY       bce00020  Pathway\nNAME        Citrate Cycle\n///\n"
        )
        mock_get.return_value = mock_response

        ids = ["bce00010", "bce00020"]
        descargar_entradas_kegg(ids, self.test_output_dir, batch_size=2, bloque_size=2, delay=0)

        # Verifica que se creó el archivo JSON
        files = os.listdir(self.test_output_dir)
        json_files = [f for f in files if f.endswith(".json")]
        self.assertEqual(len(json_files), 1)

        with open(os.path.join(self.test_output_dir, json_files[0]), "r") as f:
            data = json.load(f)
            self.assertEqual(len(data), 2)
            self.assertIn("raw_text", data[0])

if __name__ == "__main__":
    unittest.main()
