# backend/app/config/db.py

''' 
       Módulo de Configuración y Conexión a la Base de Datos MongoDB

1. Cargar variables de entorno (principalmente la URI de MongoDB y nombres
    de base de datos/colecciones) desde un archivo .env.
2. Establecer una conexión asíncrona a una instancia de MongoDB Atlas
    utilizando la librería `motor`.
3. Validar que la URI de MongoDB esté presente, lanzando una excepción
    HTTPException si no se encuentra.
4. Proporcionar acceso a la instancia de la base de datos (db) y a
    colecciones específicas predefinidas (uniprot_collection, kegg_collection,
    kegg_rutas_collection).
5. Ofrecer una función `check_connection` para verificar el estado de la
    conexión con la base de datos.
6. Proveer funciones helper `get_collection` y `get_database` para acceder
    a colecciones por nombre y a la instancia de la base de datos.
7. Incluir una dependencia de FastAPI `get_collection_dependency` para
    facilitar la inyección de objetos de colección en las rutas de la API.

Variables de entorno esperadas (con valores por defecto si aplica):
   - MONGO_URI: (Obligatoria) URI de conexión a MongoDB Atlas.
   - DB_BACILLUS_CEREUS: Nombre de la base de datos (def: "Bacillus_Cereus").
   - COLLECTION_UNIPROT: Nombre de la colección UniProt (def: "UniProt").
   - COLLECTION_KEGG: Nombre de la colección Kegg (def: "Kegg").
   - COLLECTION_KEGG_RUTAS: Nombre de la colección Kegg Rutas (def: "Kegg_rutas").
   - COLLECTION_KEGG_RUTAS_GRAFICAS: Nombre de la colección de kegg rutas hgml (def:"kegg_rutas_graficas").
'''

import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()  # Cargar variables de entorno desde .env

# Obtener URI de MongoDB Atlas desde las variables de entorno
mongo_uri = os.getenv("MONGO_URI")
if not mongo_uri:
    raise HTTPException(status_code=500, detail="MONGO_URI no está configurado en las variables de entorno")

# Obtener el nombre de la base de datos y colecciones desde las variables de entorno
db_name = os.getenv("DB_BACILLUS_CEREUS", "Bacillus_Cereus")  # Valor por defecto: "Bacillus_Cereus"
collection_uniprot = os.getenv("COLLECTION_UNIPROT", "UniProt")  # Valor por defecto: "UniProt"
collection_kegg = os.getenv("COLLECTION_KEGG", "Kegg")  # Valor por defecto: "Kegg"
collection_kegg_rutas = os.getenv("COLLECTION_KEGG_RUTAS", "Kegg_rutas")  # Valor por defecto: "Kegg"
collection_kegg_rutas_hgml = os.getenv("COLLECTION_KEGG_RUTAS_GRAFICAS", "kegg_rutas_graficas")

# Crear cliente de MongoDB
client = AsyncIOMotorClient(mongo_uri)

# Seleccionar base de datos
db = client[db_name]

# Seleccionar las colecciones
uniprot_collection = db[collection_uniprot]
kegg_collection = db[collection_kegg]
kegg_rutas_collection = db[collection_kegg_rutas]
kegg_rutas_graficas_collection = db[collection_kegg_rutas_hgml]

# Verificar si la conexión es exitosa
async def check_connection():
    try:
        # Realiza un ping a la base de datos
        await client.admin.command('ping')
        print("Conexión exitosa a MongoDB Atlas")
    except Exception as e:
        raise Exception(f"Error al conectar a MongoDB: {e}")

# Obtener una colección por nombre
def get_collection(collection_name: str):
    # Devuelve la colección especificada en la base de datos.
    return db[collection_name]

# Función para obtener la base de datos
def get_database():
    return db

# Dependencia de FastAPI para inyectar una colección específica
def get_collection_dependency(collection_name: str = collection_uniprot):
    return get_collection(collection_name)




