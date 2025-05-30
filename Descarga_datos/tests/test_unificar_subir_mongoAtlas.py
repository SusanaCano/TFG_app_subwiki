'''
Este script unifica y sube datos desde múltiples archivos JSON ubicados en una carpeta especificada
a una colección de MongoDB Atlas. El nombre de la colección y la ruta a la carpeta de archivos se
proporcionan como argumentos al ejecutar el script. La conexión a MongoDB Atlas se gestiona mediante
variables de entorno almacenadas en un archivo .env (MONGO_URI y DB_NAME).

Uso:
    python subir_a_mongodb.py <ruta_a_la_carpeta_json> <nombre_coleccion>

'''

import os
import json
import tempfile
import shutil
import mongomock
from unittest import mock, TestCase
from unificar_ficheros_json_subir_mongoAtlas import save_to_mongoDB_atlas  # Asegúrate de que el nombre del archivo sea correcto

class TestSaveToMongoDBAtlas(TestCase):
    
    def setUp(self):
        # Crea un directorio temporal con archivos JSON
        self.temp_dir = tempfile.mkdtemp()

        # Archivo con una lista de documentos
        with open(os.path.join(self.temp_dir, "data1.json"), "w") as f:
            json.dump([{"name": "A"}, {"name": "B"}], f)

        # Archivo con un solo diccionario
        with open(os.path.join(self.temp_dir, "data2.json"), "w") as f:
            json.dump({"name": "C"}, f)

    def tearDown(self):
        # Limpia después del test
        shutil.rmtree(self.temp_dir)

    @mock.patch("unificar_ficheros_json_subir_mongoAtlas.MongoClient") 
    @mock.patch.dict(os.environ, {"MONGO_URI": "mongodb://fakeuri", "DB_NAME": "testdb"})
    def test_save_to_mongoDB_atlas(self, mock_mongo_client):
        # Simula MongoDB con mongomock
        mock_client = mongomock.MongoClient()
        mock_mongo_client.return_value = mock_client

        # Ejecuta la función
        save_to_mongoDB_atlas(self.temp_dir, "test_collection")

        # Verifica que los documentos se insertaron
        db = mock_client["testdb"]
        collection = db["test_collection"]
        documents = list(collection.find())

        self.assertEqual(len(documents), 3)  # 2 + 1 documentos
        names = sorted(doc["name"] for doc in documents)
        self.assertEqual(names, ["A", "B", "C"])


