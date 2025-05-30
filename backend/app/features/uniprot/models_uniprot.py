# backend/app/features/uniprot/models_uniprot.py

'''
# Este módulo proporciona funciones asíncronas para interactuar con la colección
# 'Uniprot' de la base de datos MongoDB. Contiene lógica para:
#
# 1.  `get_protein_by_id(protein_id: str)`:
#     Recupera un único documento de proteína basado en su `_id` de MongoDB.
#     Maneja la conversión de la cadena `protein_id` a `ObjectId` para la
#     consulta y convierte el `_id` del resultado de nuevo a cadena.
#     Devuelve el documento de la proteína o `None` si no se encuentra o
#     si ocurre un error (imprimiendo el error en consola).
#
# 2.  `get_proteins_by_locus_name(locus_value: str)`:
#     Busca y recupera múltiples documentos de proteína que coincidan con un
#     valor específico de `orderedLocusName` (p.ej., "BC_xxxx") anidado dentro
#     del campo `genes`. Utiliza `$elemMatch` para consultas en arrays anidados.
#     Convierte el `_id` de cada documento resultante a cadena.
#     Devuelve una lista de documentos de proteínas o una lista vacía si no se
#     encuentran coincidencias o si ocurre un error (imprimiendo el error
#     en consola).
#
# Ambas funciones dependen del objeto `db` importado desde `app.config.db`
# para realizar las operaciones en la base de datos.
'''

from bson import ObjectId
from app.config.db import db

# Para buscar por id o _id
async def get_protein_by_id(protein_id: str):
    """Obtiene una proteína desde MongoDB por su ID"""
    # Convertimos el protein_id a ObjectId
    try:
        protein = await db.uniprot.find_one({"_id": ObjectId(protein_id)})
        
        if not protein:
            return None
        
        # Convertir ObjectId a string para la respuesta
        protein["_id"] = str(protein["_id"])
        return protein
    
    except Exception as e:
        print(f"Error al obtener la proteína: {e}")
        return None

# Para buscar orderedLocusName "BC_xxxx"

async def get_proteins_by_locus_name(locus_value: str):
    try:
        cursor = db.uniprot.find({
            "genes": {
                "$elemMatch": {
                    "orderedLocusNames": {
                        "$elemMatch": {
                            "value": locus_value
                        }
                    }
                }
            }
        })
        proteins = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            proteins.append(doc)
        return proteins

    except Exception as e:
        print(f"Error al obtener las proteínas: {e}")
        return []

