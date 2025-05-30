# Kegg/test_descargas_kegg.py

'''
Tests para el script de descarga y procesamiento de datos de rutas metabólicas KEGG.

Este archivo contiene pruebas unitarias diseñadas para verificar la funcionalidad
del script 'Kegg/descargas_definiciones_rutas_kegg_kgml.py'. Las pruebas simulan
interacciones con la API de KEGG y operaciones de sistema de archivos para asegurar
que el script maneja correctamente diversos escenarios, incluyendo respuestas exitosas,
errores de red, errores HTTP y el procesamiento y guardado de datos.

Clases y tests principales incluidos:
- TestKeggDownloader:
    - Pruebas para `fetch_kegg_data_with_retry`:
        - test_fetch_kegg_data_with_retry_success: Verifica la obtención exitosa de datos.
        - test_fetch_kegg_data_with_retry_http_404: Comprueba el manejo de errores 404 (No encontrado).
        - test_fetch_kegg_data_with_retry_http_400_ignored_for_genes: Comprueba el manejo específico de errores 400.
        - test_fetch_kegg_data_with_retry_retries_on_other_http_error: Verifica la lógica de reintentos ante errores HTTP genéricos.
        - test_fetch_kegg_data_with_retry_network_error: Prueba la lógica de reintentos ante errores de red.
        - test_fetch_kegg_data_empty_response: Verifica el manejo de respuestas vacías de la API.
    - Pruebas para `get_organism_pathway_metadata`:
        - test_get_organism_pathway_metadata_success: Comprueba la correcta extracción y formato de metadatos de rutas.
        - test_get_organism_pathway_metadata_fetch_fails: Verifica el comportamiento cuando la obtención de metadatos falla.
    - Pruebas para `get_genes_for_pathway_from_kegg`:
        - test_get_genes_for_pathway_from_kegg_success: Comprueba la correcta extracción de IDs de genes de KEGG.
        - test_get_genes_for_pathway_from_kegg_fetch_fails: Verifica el comportamiento si la obtención de genes falla.
    - Pruebas para la función `main` (flujo principal):
        - test_main_flow_success: Simula un flujo completo exitoso, incluyendo la creación de directorios,
          descarga de datos KGML, obtención de genes y guardado de archivos JSON.
        - test_main_no_pathways_found: Verifica el comportamiento del script cuando no se encuentran rutas para el organismo.
        - test_main_file_write_error: Comprueba el manejo de errores durante la escritura de archivos JSON.
'''

import unittest
from unittest.mock import patch, MagicMock, mock_open, call
from pathlib import Path
import requests
from Kegg import descargas_definiciones_rutas_kegg_kgml as kegg_downloader_module


class TestKeggDownloader(unittest.TestCase):

    def setUp(self):
       
        self.patcher_sleep = patch('time.sleep', return_value=None)
        self.mock_sleep = self.patcher_sleep.start()
        
        self.patcher_organism_code = patch.object(kegg_downloader_module, 'ORGANISM_CODE', "testorg")
        self.patcher_delay = patch.object(kegg_downloader_module, 'REQUEST_DELAY_SECONDS', 0.01)
        self.patcher_output_dir = patch.object(kegg_downloader_module, 'OUTPUT_JSON_DIR', "test_output_json")
        self.patcher_base_url = patch.object(kegg_downloader_module, 'KEGG_API_BASE_URL', "http://fake-kegg-api")

        self.mock_organism_code = self.patcher_organism_code.start()
        self.mock_delay = self.patcher_delay.start()
        self.mock_output_dir = self.patcher_output_dir.start()
        self.mock_base_url = self.patcher_base_url.start()

    def tearDown(self):
        self.patcher_sleep.stop()
        self.patcher_organism_code.stop()
        self.patcher_delay.stop()
        self.patcher_output_dir.stop()
        self.patcher_base_url.stop()

    @patch('requests.get')
    def test_fetch_kegg_data_with_retry_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "some data"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        result = kegg_downloader_module.fetch_kegg_data_with_retry("test/endpoint")
        self.assertEqual(result, "some data")
        mock_get.assert_called_once_with("http://fake-kegg-api/test/endpoint", timeout=30)

    @patch('requests.get')
    def test_fetch_kegg_data_with_retry_http_404(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        http_error = requests.exceptions.HTTPError("404 Client Error", response=mock_response)
        mock_response.raise_for_status = MagicMock(side_effect=http_error)
        mock_get.return_value = mock_response
        result = kegg_downloader_module.fetch_kegg_data_with_retry("test/endpoint")
        self.assertIsNone(result)
        mock_get.assert_called_once()

    @patch('requests.get')
    def test_fetch_kegg_data_with_retry_http_400_ignored_for_genes(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        http_error = requests.exceptions.HTTPError("400 Client Error", response=mock_response)
        mock_response.raise_for_status = MagicMock(side_effect=http_error)
        mock_get.return_value = mock_response
        result = kegg_downloader_module.fetch_kegg_data_with_retry("get/path/genes", ignore_400_for_genes=True)
        self.assertIsNone(result)
        mock_get.assert_called_once()

    @patch('requests.get')
    def test_fetch_kegg_data_with_retry_retries_on_other_http_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        http_error = requests.exceptions.HTTPError("500 Server Error", response=mock_response)
        mock_response.raise_for_status = MagicMock(side_effect=http_error)
        mock_get.return_value = mock_response
        result = kegg_downloader_module.fetch_kegg_data_with_retry("test/endpoint", retries=2)
        self.assertIsNone(result)
        self.assertEqual(mock_get.call_count, 2)

    @patch('requests.get')
    def test_fetch_kegg_data_with_retry_network_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Network error")
        result = kegg_downloader_module.fetch_kegg_data_with_retry("test/endpoint", retries=2)
        self.assertIsNone(result)
        self.assertEqual(mock_get.call_count, 2)

    @patch('requests.get')
    def test_fetch_kegg_data_empty_response(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "  \n  "
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        result = kegg_downloader_module.fetch_kegg_data_with_retry("test/endpoint", retries=2)
        self.assertIsNone(result)
        self.assertEqual(mock_get.call_count, 2)

   
    @patch.object(kegg_downloader_module, 'fetch_kegg_data_with_retry')
    def test_get_organism_pathway_metadata_success(self, mock_fetch):
        mock_fetch.return_value = (
            "path:testorg00001\tPathway 1\n"
            "path:testorg00002\tPathway 2 Name with spaces"
        )
        expected_metadata = [
            {"pathway_id": "testorg00001", "name": "Pathway 1", "organism_code": "testorg", "image_url": "http://www.kegg.jp/kegg/pathway/testorg/testorg00001.png"},
            {"pathway_id": "testorg00002", "name": "Pathway 2 Name with spaces", "organism_code": "testorg", "image_url": "http://www.kegg.jp/kegg/pathway/testorg/testorg00002.png"}
        ]
        result = kegg_downloader_module.get_organism_pathway_metadata("testorg")
        self.assertEqual(result, expected_metadata)
        mock_fetch.assert_called_once_with("list/pathway/testorg")

    @patch.object(kegg_downloader_module, 'fetch_kegg_data_with_retry')
    def test_get_organism_pathway_metadata_fetch_fails(self, mock_fetch):
        mock_fetch.return_value = None
        result = kegg_downloader_module.get_organism_pathway_metadata("testorg")
        self.assertEqual(result, [])

    @patch.object(kegg_downloader_module, 'fetch_kegg_data_with_retry')
    def test_get_genes_for_pathway_from_kegg_success(self, mock_fetch):
        mock_fetch.return_value = (
            "testorg:gene1\tDescription 1\n"
            "testorg:gene2\tDescription 2"
        )
        expected_genes = ["testorg:gene1", "testorg:gene2"]
        result = kegg_downloader_module.get_genes_for_pathway_from_kegg("testorg00001")
        self.assertEqual(result, expected_genes)
        mock_fetch.assert_called_once_with("get/testorg00001/genes", ignore_400_for_genes=True)

    @patch.object(kegg_downloader_module, 'fetch_kegg_data_with_retry')
    def test_get_genes_for_pathway_from_kegg_fetch_fails(self, mock_fetch):
        mock_fetch.return_value = None
        result = kegg_downloader_module.get_genes_for_pathway_from_kegg("testorg00001")
        self.assertEqual(result, [])

    @patch.object(kegg_downloader_module, 'Path') # Patch Path donde se usa en el módulo
    @patch.object(kegg_downloader_module, 'get_organism_pathway_metadata')
    @patch.object(kegg_downloader_module, 'fetch_kegg_data_with_retry') # Para las llamadas directas a KGML
    @patch.object(kegg_downloader_module, 'get_genes_for_pathway_from_kegg')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump') # json es importado globalmente en tu script
    def test_main_flow_success(self, mock_json_dump, mock_file_open, mock_get_genes,
                               mock_fetch_kgml, # Renombrado para claridad
                               mock_get_pathway_meta, mock_path_constructor):
        mock_path_instance = MagicMock()
        mock_path_constructor.return_value = mock_path_instance
        mock_path_instance.mkdir = MagicMock()
        def path_div_side_effect(other):
           
            return Path(kegg_downloader_module.OUTPUT_JSON_DIR) / other
        mock_path_instance.__truediv__ = MagicMock(side_effect=path_div_side_effect)

        mock_pathway_list = [
            {"pathway_id": "testorg00001", "name": "Pathway 1", "organism_code": "testorg", "image_url": "url1"},
            {"pathway_id": "testorg00002", "name": "Pathway 2", "organism_code": "testorg", "image_url": "url2"}
        ]
        mock_get_pathway_meta.return_value = mock_pathway_list
        mock_fetch_kgml.side_effect = ["<kgml_data_1/>", "<kgml_data_2/>"]
        mock_get_genes.side_effect = [["geneA", "geneB"], ["geneC"]]

        kegg_downloader_module.main()

        mock_path_instance.mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_get_pathway_meta.assert_called_once_with("testorg")

        expected_kgml_calls = [
            call("get/testorg00001/kgml"),
            call("get/testorg00002/kgml")
        ]
        self.assertEqual(mock_fetch_kgml.call_count, 2)
        mock_fetch_kgml.assert_has_calls(expected_kgml_calls, any_order=False)

        expected_gene_calls = [
            call("testorg00001"),
            call("testorg00002")
        ]
        mock_get_genes.assert_has_calls(expected_gene_calls, any_order=False)
        self.assertEqual(mock_get_genes.call_count, 2)

        expected_open_calls = [
            call(Path('test_output_json/testorg00001.json'), 'w', encoding='utf-8'),
            call(Path('test_output_json/testorg00002.json'), 'w', encoding='utf-8')
        ]

        self.assertEqual(mock_file_open.call_args_list, expected_open_calls)
        
        expected_json_data = [
            call({
                "_id": "testorg00001", "name": "Pathway 1", "organism_code": "testorg",
                "image_url": "url1", "kgml_data": "<kgml_data_1/>",
                "kegg_genes_in_pathway": ["geneA", "geneB"]
            }, mock_file_open.return_value, indent=2, ensure_ascii=False),
            call({
                "_id": "testorg00002", "name": "Pathway 2", "organism_code": "testorg",
                "image_url": "url2", "kgml_data": "<kgml_data_2/>",
                "kegg_genes_in_pathway": ["geneC"]
            }, mock_file_open.return_value, indent=2, ensure_ascii=False)
        ]
        mock_json_dump.assert_has_calls(expected_json_data, any_order=False)
        self.assertEqual(mock_json_dump.call_count, 2)


    @patch.object(kegg_downloader_module, 'Path')
    @patch.object(kegg_downloader_module, 'get_organism_pathway_metadata')
    @patch('builtins.print')
    def test_main_no_pathways_found(self, mock_print, mock_get_pathway_meta, mock_path_constructor):
        mock_path_instance = MagicMock()
        mock_path_constructor.return_value = mock_path_instance
        mock_path_instance.mkdir = MagicMock()
        mock_get_pathway_meta.return_value = []
        kegg_downloader_module.main()
        mock_path_instance.mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_get_pathway_meta.assert_called_once_with("testorg")

    @patch.object(kegg_downloader_module, 'Path')
    @patch.object(kegg_downloader_module, 'get_organism_pathway_metadata')
    @patch.object(kegg_downloader_module, 'fetch_kegg_data_with_retry')
    @patch.object(kegg_downloader_module, 'get_genes_for_pathway_from_kegg')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump', side_effect=IOError("Disk full"))
    @patch('builtins.print')
    def test_main_file_write_error(self, mock_print, mock_json_dump, mock_file_open, mock_get_genes,
                                   mock_fetch_kgml, mock_get_pathway_meta, mock_path_constructor):
        mock_path_instance = MagicMock()
        mock_path_constructor.return_value = mock_path_instance
        mock_path_instance.mkdir = MagicMock()
        def path_div_side_effect(other):
            return Path(kegg_downloader_module.OUTPUT_JSON_DIR) / other
        mock_path_instance.__truediv__ = MagicMock(side_effect=path_div_side_effect)

        mock_get_pathway_meta.return_value = [{"pathway_id": "testorg00001", "name": "Pathway 1", "organism_code": "testorg", "image_url": "url1"}]
        mock_fetch_kgml.return_value = "<kgml_data_1/>"
        mock_get_genes.return_value = ["geneA"]

        kegg_downloader_module.main()

        mock_path_instance.mkdir.assert_called_once()
        expected_file_path_to_open = Path('test_output_json/testorg00001.json')
        mock_file_open.assert_called_once_with(expected_file_path_to_open, 'w', encoding='utf-8')
        mock_json_dump.assert_called_once()

        found_error_message = False
        
        expected_file_path_str = str(Path('test_output_json') / 'testorg00001.json')
        expected_msg_part_1 = f"Error al guardar el archivo {expected_file_path_str}"
        expected_msg_part_2 = "Disk full"

        for call_arg_tuple in mock_print.call_args_list:
            printed_message = call_arg_tuple[0][0]
            if isinstance(printed_message, str) and expected_msg_part_1 in printed_message and expected_msg_part_2 in printed_message:
                found_error_message = True
                break
        self.assertTrue(found_error_message, f"No se imprimió el mensaje de error esperado '{expected_msg_part_1}: {expected_msg_part_2}'")

if __name__ == '__main__':
    unittest.main()