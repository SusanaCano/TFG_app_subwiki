from pymongo import MongoClient
#from fastapi import FastAPI
from pymongo.errors import ServerSelectionTimeoutError  # Usamos esta excepción para errores de conexión
#from dotenv import load_dotenv
import os
from app.config.db import get_database



#app = FastAPI()

#load_dotenv()  # Cargar variables de entorno del archivo .env

# Conectar a MongoDB Atlas
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
#client = MongoClient("mongodb+srv://<usuario>:<contraseña>@<cluster>.mongodb.net/<nombre_db>?retryWrites=true&w=majority")

# Seleccionar la base de datos y colección
db = client["BacillusCereus"]
#collection = db["buscarGenes"]

def obtener_datos():
    collection = db["buscarGenes"] 
    try:
        # Realizar consulta con limit y proyección
        resultado = collection.find(
            {},  # Esto selecciona todos los documentos (puedes añadir filtros si es necesario)
            {
                "proteinDescription": 1,
                "genes": {
                    "$elemMatch": {
                        "geneName": 1,  # Solo incluir el campo 'gene'
                        "orderedLocusName": {"value": 1},  # Incluir 'orderedLocusName->value'
                    }
                },
                "sequence": {
                    "$elemMatch": {
                        "value": {"value": 1},
                        "length": 1
                    }   
                }
            }
        ).limit(25)  # Limitar a las primeras 25 entradas




        resultado_lista = list(resultado)  # Convertir el cursor en lista
        
        # Imprimir los resultados en la terminal
        print(resultado_lista)
        
        print(collection.count_documents({}))  # Esto imprimirá el número de documentos en la colección
        
        return list(resultado)  # Convertir el cursor en lista
    except ServerSelectionTimeoutError as e:
        return {"error": "No se pudo conectar al servidor de MongoDB. " + str(e)}
    

# Ejecutar la función si el script es ejecutado directamente
if __name__ == "__main__":
    obtener_datos()  # Llamar a la función definida previamente
    
