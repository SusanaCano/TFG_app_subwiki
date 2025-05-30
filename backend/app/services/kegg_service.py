# backend/app/services/kegg_service.py

'''
# Este módulo proporciona servicios para manejar datos de KEGG (Kyoto Encyclopedia
# of Genes and Genomes). Centraliza la lógica para:
#
# 1.  `obtener_ruta_metabolica(entry, db_motor)`:
#     - Recupera documentos de rutas metabólicas desde una colección de MongoDB
#       (presumiblemente 'kegg_rutas').
#     - Realiza una búsqueda flexible, insensible a mayúsculas/minúsculas y
#       guiones bajos, para las entradas de rutas utilizando las capacidades
#       de $expr y regex de MongoDB.
#     - Serializa el `_id` de MongoDB (ObjectId) a una cadena para facilitar
#       su consumo.
#
# 2.  `parse_kgml_to_graph(kgml_string, pathway_map_id)`:
#     - Parsea cadenas XML crudas en formato KGML (KEGG Markup Language).
#     - Transforma los datos KGML en una representación de grafo estructurada,
#       consistente en nodos (derivados de los elementos `<entry>` de KGML) y
#       aristas (derivadas de los elementos `<relation>` de KGML).
#     - Extrae atributos como ID del nodo, etiqueta, tipo, coordenadas, y
#       origen, destino y etiqueta de las aristas.
#     - Devuelve un diccionario que contiene listas de nodos, aristas y cualquier
#       error de parseo.
#
# El módulo también define estructuras `TypedDict` personalizadas (`KgmlNode`,
# `KgmlEdge`, `ParsedKgmlGraph`) para representar los componentes del grafo
# KGML parseado.
#
# En general, este servicio tiene como objetivo abstraer y proporcionar información
# procesada de rutas KEGG para su uso en otras partes de la aplicación, como
# endpoints de API o componentes de visualización de datos.
'''

from app.config.db import db  # Asegúrate de que tienes una conexión con tu base de datos
from motor.motor_asyncio import AsyncIOMotorDatabase
import re
import xml.etree.ElementTree as ET
from typing import Dict, List, TypedDict # Para type hinting

# Tipos para el parser KGML
class KgmlNode(TypedDict):
    id: str
    label: str
    type: str
    x: int | None
    y: int | None

class KgmlEdge(TypedDict):
    source: str
    target: str
    label: str

class ParsedKgmlGraph(TypedDict):
    nodes: List[KgmlNode]
    edges: List[KgmlEdge]
    error: str | None


# Función para convertir el ObjectId a cadena
def serialize_document(doc):
    if doc is not None:
        doc["_id"] = str(doc["_id"])  # Convertir ObjectId a string
    return doc

async def obtener_ruta_metabolica(entry: str, db_motor: AsyncIOMotorDatabase):
    try:
        # Suponiendo que tienes una colección 'kegg_rutas' en tu base de datos
        collection = db_motor["kegg_rutas"]
        
                # Normaliza la entrada: quita guiones bajos, pasa a minúsculas
        entrada_normalizada = entry.replace("_", "").lower()

        # Crea una expresión regular que ignore mayúsculas/minúsculas y guiones bajos
        regex = re.compile(f"^{entrada_normalizada}$", re.IGNORECASE)
        
         # Buscar la ruta metabólica por el genId de forma asincrónica
        #ruta_metabolica = await collection.find_one({"entry": entry})  # 'await' para consultas asincrónicas

        # Haz que MongoDB normalice también el campo 'entry' en la misma forma
        ruta_metabolica = await collection.find_one({
            "$expr": {
                "$regexMatch": {
                    "input": {"$replaceAll": {"input": "$entry", "find": "_", "replacement": ""}},
                    "regex": f"^{entrada_normalizada}$",
                    "options": "i"
                }
            }
        })
        
        if ruta_metabolica:
            # Devolver la ruta metabólica o procesar los datos según sea necesario
            return serialize_document(ruta_metabolica)
        else:
            return None
    except Exception as e:  # Usar una excepción genérica si no deseas capturar solo PyMongoError
        # Manejo de errores de la base de datos
        print(f"Error de conexión a MongoDB: {e}")
        return None
    
# --- PARSEO KGML ---
def parse_kgml_to_graph(kgml_string: str, pathway_map_id: str) -> ParsedKgmlGraph:
    """
    Parsea una cadena KGML y la convierte en una estructura de nodos y aristas
    compatible con Cytoscape.
    """
    nodes: List[KgmlNode] = []
    edges: List[KgmlEdge] = []
    
    if not kgml_string:
        return ParsedKgmlGraph(nodes=[], edges=[], error=f"No KGML data provided for {pathway_map_id}")

    try:
        root = ET.fromstring(kgml_string)
    except ET.ParseError as e:
        return ParsedKgmlGraph(nodes=[], edges=[], error=f"Failed to parse KGML XML for {pathway_map_id}: {e}")

    kgml_id_to_node_id_map: Dict[str, str] = {}

    # Primera pasada: crear nodos y mapear IDs internos de KGML a IDs de Cytoscape
    for entry in root.findall(".//entry"):
        internal_kgml_id = entry.get("id")
        # Usar el atributo 'name' como ID principal para el nodo en Cytoscape
        # ej: "bce:BC5335", "cpd:C00231", "path:bce00020"
        node_id_for_cytoscape = entry.get("name") 
        
        if not internal_kgml_id or not node_id_for_cytoscape:
            # Manejar entradas KGML incompletas si es necesario
            continue 
            
        kgml_id_to_node_id_map[internal_kgml_id] = node_id_for_cytoscape
        
        entry_type = entry.get("type", "unknown") # Default si type no está
        graphics = entry.find("graphics")
        label = node_id_for_cytoscape # Etiqueta por defecto es el ID del nodo
        x, y = None, None

        if graphics is not None:
            # Tomar el primer nombre de graphics.get("name") como etiqueta si existe
            # Limpiar "..." y posibles múltiples nombres separados por coma
            graphic_label_parts = graphics.get("name", "").split(",")[0].strip()
            if graphic_label_parts and graphic_label_parts != "...":
                label = graphic_label_parts
            
            try:
                x_str, y_str = graphics.get("x"), graphics.get("y")
                # Asegurarse de que sean números válidos antes de convertir
                x = int(x_str) if x_str and x_str.strip().lstrip('-').isdigit() else None
                y = int(y_str) if y_str and y_str.strip().lstrip('-').isdigit() else None
            except (ValueError, TypeError):
                x, y = None, None # Si la conversión falla, quedan como None
        
        nodes.append(KgmlNode(id=node_id_for_cytoscape, label=label, type=entry_type, x=x, y=y))

    # Segunda pasada: crear aristas usando el mapeo de IDs
    for relation in root.findall(".//relation"):
        entry1_kgml_id = relation.get("entry1")
        entry2_kgml_id = relation.get("entry2")
        
        # Obtener los IDs de Cytoscape correspondientes a los IDs internos de KGML
        source_node_id = kgml_id_to_node_id_map.get(entry1_kgml_id or "")
        target_node_id = kgml_id_to_node_id_map.get(entry2_kgml_id or "")

        if source_node_id and target_node_id:
            relation_label_parts: List[str] = []
            for subtype in relation.findall("subtype"):
                subtype_name = subtype.get("name")
                if subtype_name:
                    relation_label_parts.append(subtype_name)
            
            relation_label = ", ".join(relation_label_parts)
            
            edges.append(KgmlEdge(source=source_node_id, target=target_node_id, label=relation_label))
            
    return ParsedKgmlGraph(nodes=nodes, edges=edges, error=None)