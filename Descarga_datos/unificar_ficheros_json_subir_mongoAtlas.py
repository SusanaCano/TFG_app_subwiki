'''
Este script unifica y sube datos desde múltiples archivos JSON ubicados en una carpeta especificada
a una colección de MongoDB Atlas. El nombre de la colección y la ruta a la carpeta de archivos se
proporcionan como argumentos al ejecutar el script. La conexión a MongoDB Atlas se gestiona mediante
variables de entorno almacenadas en un archivo `.env` (MONGO_URI y DB_NAME).

Uso:
    unificar_ficheros_json_subir_mongoAtlas.py <ruta_a_la_carpeta_json> <nombre_coleccion>

'''

import json
import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv

def save_to_mongoDB_atlas(json_directory, collection_name):
    # Cargar variables de entorno desde el archivo .env
    load_dotenv()

    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("DB_NAME")
    #collection_name = db[collection_name]
    
    # Verifica si las variables están disponibles
    if not mongo_uri or not db_name or not collection_name:
        print("Faltan variables en el archivo .env")
        return  
    
    try:
        # Conexión a MongoDB Atlas
        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]
        print(f"Conectado a la base de datos '{db_name}', colección '{collection_name}'")
    except Exception as e:
        print(f"Error al conectar a MongoDB Atlas: {e}")
        return
    
    # Verifica si el directorio existe
    if not os.path.exists(json_directory):
        print(f"El directorio {json_directory} no existe.")
        return
    
    archivos = [f for f in os.listdir(json_directory) if f.endswith(".json")]
    if not archivos:
        print(f"No se encontraron archivos .json en '{json_directory}'")
        return

    # Procesar cada archivo .json en el directorio
    for filename in archivos:
        file_path = os.path.join(json_directory, filename)
        print(f"Procesando archivo: {file_path}")
        
        try:
                # Leer datos del archivo JSON
            with open(file_path, "r", encoding="utf-8") as json_file:
                    data = json.load(json_file)

                # Asegurarse de que los datos son una lista, si no lo son, convertirlos a una lista
            if not isinstance(data, list):
                print(f"El archivo {filename} no tiene una lista de datos. Convertido a lista.")
                data = [data]
                
                # Insertar datos en MongoDB
            if data:
                result = collection.insert_many(data)
                print(f"Insertados {len(result.inserted_ids)} documentos desde {filename}")
            else:
                print(f"El archivo {filename} está vacío.")
            
        except Exception as e:
            print(f"Error al procesar el archivo {filename}: {e}")
            
    print("Proceso completo.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python subir_a_mongodb.py <ruta_a_la_carpeta_json> <nombre_coleccion>")
    else:
        json_directory = sys.argv[1]
        collection_name = sys.argv[2]
        save_to_mongoDB_atlas(json_directory, collection_name)

