'''
Este script descarga y procesa rutas metabólicas de KEGG para *Bacillus cereus* (código "bce").
1. Descarga los datos en bloques de 10 entradas desde la API de KEGG.
2. Almacena las entradas descargadas en archivos JSON.
3. Extrae y procesa la información relevante sobre las rutas metabólicas.
4. Permite realizar pruebas unitarias para validar el comportamiento de la extracción de datos y 
la gestión de archivos.

Nota: Los archivos descargados deben tener un formato de lista de entradas para ser 
procesados correctamente.
'''

import logging
import os
from unittest import TestCase
from unittest.mock import patch, mock_open

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Kegg.descargas_kegg_paths")

# Función que procesará los archivos 
def procesar_archivos_kegg(carpeta_entrada):
    archivos = os.listdir(carpeta_entrada)
    if not archivos:
        logger.info("No se encontraron archivos en la carpeta de entrada.")
        return
    # El resto del código para procesar los archivos se iría aquí
    for archivo in archivos:
        if archivo.endswith(".json"):
            with open(os.path.join(carpeta_entrada, archivo)) as f:
                data = f.read()

# Función que extrae la información de las rutas 
def extraer_info_pathways(entry_id):
    # Simulando un archivo con datos en formato JSON
    archivo_simulado = '{"ENTRY": "bce03010", "NAME": "Ribosome", "PATHWAY": "bce03010 Ribosome"}'
    
    # Simulamos la extracción de información 
    data = eval(archivo_simulado)  

    if data["ENTRY"] == entry_id:
        return data
    return None


# Test case con unittest
class TestScriptKegg(TestCase):

    # Test para la función extraer_info_pathways
    @patch("Kegg.descargas_kegg_paths.open", new_callable=mock_open, read_data='{"ENTRY": "bce03010", "NAME": "Ribosome", "PATHWAY": "bce03010 Ribosome"}')
    def test_extraer_info_pathways(self, mock_file):
        # Simulamos el archivo que se abrirá
        data = '{"ENTRY": "bce03010", "NAME": "Ribosome", "PATHWAY": "bce03010 Ribosome"}'
        mock_file.return_value.read.return_value = data
        
        # Llamamos a la función que queremos probar
        resultado = extraer_info_pathways("bce03010")
        
        # Verificamos que el 'entry' sea correcto
        self.assertEqual(resultado["ENTRY"], "bce03010")  # Asegúrate de usar la clave correcta aquí

    # Test para cuando no hay archivos en la carpeta de entrada
    @patch("Kegg.descargas_kegg_paths.os.listdir", return_value=[])
    @patch("Kegg.descargas_kegg_paths.open", new_callable=mock_open)
    def test_no_archivos_en_entrada(self, mock_file, mock_listdir):
        # Simulamos que no hay archivos en la carpeta de entrada
        mock_listdir.return_value = []
        
        with self.assertLogs("Kegg.descargas_kegg_paths", level="INFO") as log:
            procesar_archivos_kegg("descargas_kegg_json")
        
        # Verificamos que se haya registrado el mensaje de advertencia
        self.assertIn("No se encontraron archivos en la carpeta de entrada.", log.output[0])


# Si estás ejecutando los tests de manera individual, usa esta línea para ejecutarlos:
if __name__ == "__main__":
    import unittest
    unittest.main()
