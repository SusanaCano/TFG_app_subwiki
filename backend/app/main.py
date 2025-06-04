from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from app.config.db import db, get_database
#get_database, get_collection_dependency # Importamos la conexión a MongoDB
from app.routers.router_uniprot import router as uniprot_router # protein_router para id, para orderedLocusName
from app.routers.router_kegg import kegg_router
from app.routers.router_kegg_graph import kegg_graph_router
from fastapi_pagination import Page, add_pagination, paginate
import os
from motor.motor_asyncio import AsyncIOMotorClient
#from app.models.models_page_consultas import Page
#from typing import List, Dict
from pydantic import BaseModel
from app.consultas.consultaUniprot import obtener_resultados
from app.utils.transformador import transformar_documento
#from app.consultas.consulta4 import obtener_resultados # Esta funciona pero le faltan algunos campos
from app.models.models_data_mongo import QueryResponse  
from app.services.kegg_service import obtener_ruta_metabolica

load_dotenv()  # Cargar variables de entorno desde .env

app = FastAPI()

app.include_router(uniprot_router, prefix="/api", tags=["Uniprot"])
app.include_router(kegg_router, prefix="/api/kegg")
app.include_router(kegg_graph_router, prefix="/api/kegg")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Origen del frontend (ajusta si es otro)
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los headers
)

# Obtener las variables de entorno
mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB_BACILLUS_CEREUS")
collection_uniprot = os.getenv("COLLECTION_UNIPROT")
collection_kegg = os.getenv("COLLECTION_KEGG")
collection_kegg_rutas = os.getenv("COLLECTION_KEGG_RUTAS")
collection_kegg_rutas_graficas = os.getenv("COLLECTION_KEGG_RUTAS_GRAFICAS")

# Conectar a MongoDB
client = AsyncIOMotorClient(mongo_uri)
db = client[db_name]

# Seleccionar las colecciones
uniProt_collection = db[collection_uniprot]
kegg_collection = db[collection_kegg]
kegg_rutas_collection = db[collection_kegg_rutas]
kegg_rutas_graficas_collection = db[collection_kegg_rutas_graficas]

@app.get("/")
def read_root():
    return {"message": "API del Backend funcionando correctamente"}

'''
# Probar la conexión a MongoDB
@app.get("/ping-db")
async def ping_db():
    try:
        #await db.command("ping")  # Verifica si MongoDB responde
        await get_database.command("ping")
        return {"message": "MongoDB conectado correctamente"}
    except Exception as e:
        return {"error": str(e)}
'''
    
#app.include_router(protein_router.router)  # Incluye el router en la aplicación
#app.include_router(get_protein)  # Incluye el router en la aplicación

# PRUEBA DE CONEXION MONGO CONSULTA BASICA
'''
@app.get("/api/genes", response_model=Page[dict])
async def get_genes(query: str = Query(..., alias="query")):
    try:
        # Ejecutar la consulta y convertir el cursor a lista
        data = await collection.find({"evidences.value": query}).to_list(None)

        if not data:
            return {"message": "No se encontraron datos para el query"}
        
        # Crear la respuesta con la estructura correcta
        return {
            "items": data,
            "total": len(data),
            "page": 1,  # Puede ajustarlo según la paginación que desees
            "size": len(data)
        }
    except Exception as e:
        return {"message": "Error al conectar a la base de datos", "error": str(e)}
'''
'''
@app.get("/api/genes", response_model=List[Dict])
async def get_genes(query: str):
    # Datos de ejemplo
    example_data = [
        {"gene": "BC_2340", "description": "Gene description for BC_2340"},
        {"gene": "BC_2341", "description": "Gene description for BC_2341"},
        {"gene": "BC_2342", "description": "Gene description for BC_2342"},
    ]

    # Filtro básico por query
    results = [item for item in example_data if query.lower() in item["gene"].lower()]

    # Retorna los resultados filtrados
    return results
'''

'''
@app.get("/api/genes", response_model=Page[dict])
async def get_genes(query: str = Query(..., alias="query")):
    """Consulta la base de datos de genes filtrando por un término."""
    data = list(collection.find({"gene_id": query}, {"_id": 0}))  # Ajusta el campo según tus datos
    if not data:
        print("No se encontraron resultados.")
        return paginate([])
    else:
        print("Datos encontrados:", data)
    return paginate(data)

add_pagination(app)
'''

'''
@app.get("/api/genes", response_model=GeneResponse)
async def get_genes(query: str, page: int = 1, size: int = 50):
    # Simulando una respuesta de búsqueda de genes (aquí deberías hacer la lógica de búsqueda real)
    genes = [
        {"gene": "BC_2340", "description": "Descripción del gen"},
        {"gene": "BC_2341", "description": "Otra descripción"}
    ]

    return GeneResponse(
        resultados=genes,
        total=len(genes),  # Aquí, en un caso real, sería el total de resultados de la búsqueda
        page=page,
        size=size
    )
'''

# PARA COMPROBAR LA ESTRUUCTURA DE LOS DATOS QUE SE OBTIENEN DESDE MONGODB
@app.get("/verificar_estructura")
async def verificar_estructura():
    # Obtener la colección
    collection = db['UniProt']
    
    cursor = collection.find({})
    documentos = await cursor.to_list(length=2)
    
    # Imprimir los documentos para verificar la estructura
    print("Documentos encontrados:", documentos)
    documentos = [transformar_documento(doc) for doc in documentos]
    return documentos

'''
# @app.get("/buscar", response_model=List[QueryResponse])
@app.get("/buscar", response_model=Dict[str, List[QueryResponse]])
async def buscar(query: str):
    resultados = await obtener_resultados(query)
    #return resultados
    #if resultados.count() == 0:
     #   return {"message": "No se encontraron resultados para la consulta"}, 404
    return {"result": list(resultados)}
'''

class GenIdRequest(BaseModel):
    entry: str

@app.get("/kegg/{entry}")
async def get_kegg_route(entry: str, db = Depends(get_database)):
    try:
        ruta_metabolica = await obtener_ruta_metabolica(entry, db)  # Usamos 'await' aquí
        
        if ruta_metabolica:
            # Si es un objeto de MongoDB o algo que no es serializable, convierte a diccionario
            if hasattr(ruta_metabolica, 'to_dict'):
                ruta_metabolica = ruta_metabolica.to_dict()
            return JSONResponse(content=ruta_metabolica)
        
        return {"error": "Ruta metabólica no encontrada"}
    except Exception as e:
        return {"error": str(e)}
    
'''
    # Ejemplo de mock data en FastAPI
@app.get("/kegg/pathway_graph_data/{pathway_id}")
async def get_pathway_graph_details_mock(pathway_id: str):
    print(f"[FastAPI MOCK] Received request for pathway graph: {pathway_id}")
    # Devolver datos falsos con la estructura correcta
    return {
        "pathwayId": pathway_id,
        "pathwayName": f"Mock Pathway {pathway_id}",
        "pathwayImageUrl": "https://via.placeholder.com/600x400.png?text=Pathway+Diagram",
        "nodes": [
            {"id": "1", "label": "Gene A", "type": "gene"},
            {"id": "2", "label": "Compound X", "type": "compound"},
            {"id": "3", "label": "Gene B", "type": "gene"}
        ],
        "edges": [
            {"source": "1", "target": "2", "label": "produces"},
            {"source": "2", "target": "3", "label": "input for"}
        ]
    }
    
'''  
   
 
