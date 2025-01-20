from fastapi import FastAPI
from fastapi.responses import JSONResponse
import requests
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse  # Importar RedirectResponse
from db.save_to_mongoDB_atlas import save_to_mongoDB_atlas
from db.uniprote_descargas import proceso_descarga
from fastapi import HTTPException
from db.consulta1 import obtener_datos
load_dotenv()  # Cargar variables de entorno desde .env

'''
# Cargar datos de conexión a MongoDB desde variables de entorno
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['uniprot_data']
collection = db['search_results']
'''

app = FastAPI()

# Definir los orígenes permitidos para las solicitudes CORS
origins = [
    "http://localhost:3000",  # Frontend en Next.js
    "http://localhost",       # Si también se ejecuta en localhost
    "http://127.0.0.1:3000",  # En caso de estar usando 127.0.0.1
]

# Agregar el middleware de CORS a la aplicación FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir solicitudes de estos orígenes
    allow_credentials=True,
    allow_methods=["*"],    # Permitir todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],    # Permitir todos los encabezados
)


app = FastAPI()

# Endpoint para otras consultas o pruebas
@app.get("/", operation_id="root_get")
async def root():
    return {"message": "Bienvenido a la API de Bacillus Cereus"}


# Directorio donde están los archivos .json
#json_directory = 'descargasUniprot'  # Ruta relativa o absoluta del directorio con los archivos JSON

# Llamar a la función que guarda los archivos en MongoDB
#save_to_mongoDB_atlas(json_directory)


# Ruta para servir el favicon
@app.get("/favicon.ico")
async def favicon():
    return RedirectResponse(url="/static/favicon.ico")

# Montar la carpeta static
#app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/other", operation_id="other_get")
async def root():
    return {"mensage": "Hola mundo"}

@app.get("/api/message")
async def get_message():
    return {"message": "¡Hola desde el backend!"}

# Este endpoint acepta una consulta de búsqueda como parámetro (query).
#Realiza la consulta a UniProt usando su API.
#Almacena los resultados en MongoDB Atlas.
#Responde al frontend con los datos descargados.
#Consulta a UniProt: El endpoint hace una solicitud GET a la API pública de UniProt para obtener datos en formato JSON.
#Almacenamiento en MongoDB: Los resultados de la consulta de UniProt se insertan en la colección de MongoDB denominada search_results.

@app.get("/search")
async def search_uniprot(query: str):
    # Realizar la búsqueda en UniProt
    url = f"https://rest.uniprot.org/uniprotkb/search?query={query}&format=json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        
        # Guardar los datos en MongoDB
        collection.insert_many(data['results'])  # Asumiendo que 'results' contiene los datos que deseas guardar
        
        # Devolver los resultados al frontend
        return JSONResponse(content=data)
    else:
        return JSONResponse(status_code=400, content={ "message": "Error al consultar UniProt" })
    
#@app.post("/descargar_json")
#async def descargar_datos():
    # Aquí va tu lógica para manejar la descarga
#    return {"message": "Descarga iniciada"}

# Endpoint para recibir la consulta y descargar los datos
@app.post("/descargar_json")
async def descargar_y_guardar_datos(query: str, limit: int = 100, total: int = 500, delay: int = 2):
    """
    Recibe un query desde el frontend, descarga los datos desde UniProt y los guarda en MongoDB.
    """
    # Definir el directorio donde se guardarán los archivos JSON
    json_directory = 'descargasUniprot'
    
    # Descargar los datos desde UniProt y guardarlos como archivos JSON
    try:
        proceso_descarga(query=query, limit=limit, total=total, delay=delay, json_directory=json_directory)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la descarga de datos: {str(e)}")
    
    # Guardar los datos descargados en MongoDB
    try:
        save_to_mongoDB_atlas(json_directory)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar en MongoDB: {str(e)}")
    
    return {"message": f"Datos de '{query}' descargados y cargados en MongoDB Atlas correctamente."}

@app.get("/consulta1")
async def consulta():
    resultado = obtener_datos()  # Llamada a la función de consulta
    return {"data": resultado}