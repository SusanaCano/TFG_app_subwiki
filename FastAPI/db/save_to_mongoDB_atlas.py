import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv

def save_to_mongoDB_atlas():
    # Cargar variables de entorno desde el archivo .env
    load_dotenv()

    # Conectar a MongoDB Atlas
    mongo_uri = os.getenv("MONGO_URI")
    client = MongoClient(mongo_uri)
    db = client["BacillusCereus"]
    #collection = db["claster0"]
    collection = db["buscarGenes"]

    # Directorio donde están los archivos .json
    #json_directory = "./descargas"
    #json_directory = "/FastAPI/descargasUniprot"
    #json_directory = "descargasUniprot"

    json_directory = os.path.abspath(os.path.join(os.getcwd(), "descargas_json"))

    # Procesar cada archivo .json en el directorio
    for filename in os.listdir(json_directory):
        if filename.endswith(".json"):
            file_path = os.path.join(json_directory, filename)
            print(f"Procesando archivo: {file_path}")

            try:
                # Leer datos del archivo JSON
                with open(file_path) as json_file:
                    data = json.load(json_file)

                # Asegurarse de que los datos son una lista, si no lo son, convertirlos a una lista
                if not isinstance(data, list):
                    data = [data]
                
                # Insertar datos en MongoDB
                collection.insert_many(data)
                print(f"Datos de {filename} subidos a MongoDB Atlas correctamente.")

            except Exception as e:
                print(f"Error al procesar el archivo {filename}: {e}")
            
    print("Proceso completo.")
