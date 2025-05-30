# PARA NO TENER QUE LLAMAR A URI_NAME, NOMBRE BD, SOLO ESPECIFICAMOS LA COLLECCION
# HAY QUE RETOCAR CONSULTA MIRANDO CONSULTA2.PY
from app.config.db import get_database

db = get_database()

# Función de búsqueda por ID
async def buscar_por_id(collection_name: str, id: str):
    collection = db["UniProt"]  # Aquí defines la colección que necesitas
    result = await collection.find_one({"_id": id})
    return result

# Función de búsqueda por nombre
async def buscar_por_nombre(collection_name: str, nombre: str):
    collection = db["UniProt"]  # Aquí defines la colección que necesitas
    result = await collection.find_one({"nombre": nombre})
    return result
