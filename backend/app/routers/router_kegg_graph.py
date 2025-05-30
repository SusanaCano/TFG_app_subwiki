# app/routers/router_kegg_graph.py

'''
# Este módulo define un APIRouter de FastAPI específicamente para servir
# datos de rutas metabólicas de KEGG, procesados y estructurados para
# su visualización como grafos.
#
# Funcionalidad Principal:
#   - Define un endpoint (`GET /pathways_graph/{pathway_map_id}`) que:
#     1. Recupera un documento de ruta metabólica (que contiene datos KGML)
#        desde una base de datos MongoDB utilizando un `pathway_map_id`
#        (ej. "bce00010").
#     2. Utiliza un servicio (`app.services.kegg_service.parse_kgml_to_graph`)
#        para parsear la cadena KGML cruda en un formato de grafo estructurado
#        (nodos y aristas).
#     3. Devuelve estos datos del grafo parseado junto con metadatos relevantes
#        de la ruta (nombre, código de organismo, URL de imagen).
#
# Modelos Pydantic:
#   - `GraphNode`, `GraphEdge`: Definen la estructura de los nodos y aristas
#     del grafo para la respuesta.
#   - `ParsedPathwayGraphResponse`: Define el esquema completo de la respuesta JSON,
#     incluyendo metadatos de la ruta y los componentes del grafo.
#
# Dependencias:
#   - Conexión a la base de datos MongoDB (a través de `app.config.db.get_database`).
#   - Servicio de parseo de KGML (`app.services.kegg_service`).
#
# El router utiliza el prefijo "/pathways_graph" y está etiquetado como
# "KEGG Pathway Graphs" para la documentación OpenAPI.
'''

from fastapi import APIRouter, HTTPException, Depends, Path as FastApiPath
from motor.motor_asyncio import AsyncIOMotorDatabase # Para MongoDB asincrono
from app.config.db import get_database # Para obtener la conexion a la DB
from pydantic import BaseModel, Field
from typing import List, Optional, Any
from app.services.kegg_service import parse_kgml_to_graph, KgmlNode, KgmlEdge


kegg_graph_router = APIRouter(
    prefix="/pathways_graph", # Prefijo para todas las rutas en este router
    tags=["KEGG Pathway Graphs"]  # Etiqueta para la documentacion OpenAPI/Swagger
)

# --- Modelo Pydantic para la Respuesta ---
# Debe coincidir con el frontend espera (KeggPathwayGraphData)

class GraphNode(BaseModel): # Equivalente a KgmlNode pero para la respuesta Pydantic
    id: str
    label: str
    type: str
    x: Optional[int] = None
    y: Optional[int] = None

class GraphEdge(BaseModel): # Equivalente a KgmlEdge pero para la respuesta Pydantic
    source: str
    target: str
    label: Optional[str] = None
    

    
class ParsedPathwayGraphResponse(BaseModel):
    # El _id del documento original de MongoDB, que es el pathway_map_id
    # Usamos alias para que en la respuesta JSON se llame "pathwayId" o "_id" según prefieras.
    # Para consistencia con tu frontend, pathwayId parece mejor.
    # _id: str = Field(alias="id_mongo") # Si quieres mantener el _id original de mongo
    pathwayId: str = Field(alias="_id") # Mapea _id de mongo a pathwayId en el JSON
    
    name: str # Nombre de la ruta
    pathwayName: Optional[str] = None # Alias para frontend si es diferente de 'name'
    organism_code: str
    image_url: Optional[str] = None
    
    nodes: List[GraphNode]
    edges: List[GraphEdge]

    class Config:
        populate_by_name = True # Permite usar alias en Field


# --- Lógica de obtención de datos de la BD (dentro del router o en servicio) ---
async def get_pathway_document_from_db(pathway_id: str, db: AsyncIOMotorDatabase) -> Optional[dict]:
    """
    Obtiene el documento completo de una ruta desde la colección 'kegg_rutas_graficas'.
    Este documento debe contener el campo 'kgml_data'.
    """
    # Asegúrate de que 'kegg_rutas_graficas' es el nombre correcto de tu colección
    # donde guardas el KGML y otros metadatos de la ruta.
    collection_name = "kegg_rutas_graficas" 
    pathway_document = await db[collection_name].find_one({"_id": pathway_id})
    return pathway_document

   
@kegg_graph_router.get("/pathways_graph/{pathway_map_id}", response_model=ParsedPathwayGraphResponse)
async def get_pathway_graph_with_parsed_kgml_endpoint(
    pathway_map_id: str = FastApiPath(..., description="ID del mapa de ruta KEGG, ej: bce00010"), 
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Obtiene los detalles de una ruta metabólica y parsea su KGML
    para devolver nodos y aristas listos para graficar.
    """
    pathway_document = await get_pathway_document_from_db(pathway_map_id, db)

    if not pathway_document:
        raise HTTPException(
            status_code=404, 
            detail=f"Documento del pathway con ID '{pathway_map_id}' no encontrado."
        )
    
    kgml_string = pathway_document.get("kgml_data")
    if not kgml_string:
        raise HTTPException(
            status_code=404, # O 500 si consideras que el documento está incompleto
            detail=f"Datos KGML no encontrados en el documento del pathway '{pathway_map_id}'."
        )

    # Llamar a la función de parseo (que es síncrona)
    # FastAPI maneja la ejecución de funciones síncronas en un thread pool si el endpoint es async
    parsed_graph_components = parse_kgml_to_graph(kgml_string, pathway_map_id)

    if parsed_graph_components["error"]:
        # Si hubo un error durante el parseo del KGML
        raise HTTPException(status_code=500, detail=f"Error parseando KGML para '{pathway_map_id}': {parsed_graph_components['error']}")

    # Construir la respuesta usando el modelo Pydantic
    # Pydantic se encargará de la validación y serialización.
    # El alias "_id" en ParsedPathwayGraphResponse se mapeará a pathway_document["_id"]
    response_data = {
        "_id": pathway_document["_id"], # Pydantic lo mapeará a 'pathwayId'
        "name": pathway_document.get("name", "Nombre de Ruta Desconocido"),
        "pathwayName": pathway_document.get("pathway_name", pathway_document.get("name")), # Usar 'name' como fallback
        "organism_code": pathway_document.get("organism_code", "N/A"),
        "image_url": pathway_document.get("image_url"),
        "nodes": parsed_graph_components["nodes"],
        "edges": parsed_graph_components["edges"]
    }
    
    return response_data