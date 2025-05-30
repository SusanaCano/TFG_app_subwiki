# backend/app/models/models_data_mongo.py

'''
# Este módulo define varios modelos de datos utilizando Pydantic (`BaseModel`)
# para estructurar, validar y serializar información biológica, principalmente
# relacionada con proteínas, genes y sus secuencias. Estos modelos están
# diseñados para ser utilizados, por ejemplo, en una API FastAPI para definir
# los esquemas de las solicitudes y respuestas.
#
# Modelos principales definidos:
#   - `Sequence`: Describe una secuencia biológica, incluyendo su valor de cadena,
#                 longitud, y opcionalmente su peso molecular y checksums
#                 (CRC64, MD5).
#   - `Gene`: Representa la información de un gen, con su nombre (`geneName`)
#             y una cadena para los nombres de locus ordenados
#             (`orderedLocusNames`).
#   - `Protein`: Un modelo más completo para una proteína, que incluye su
#                acceso primario (`primaryAccession`), una lista de objetos
#                `Gene`, un único objeto `Sequence` asociado, y una descripción
#                opcional de la proteína.
#   - `QueryResponse`: Define la estructura de una respuesta a una consulta,
#                      conteniendo información potencialmente parcial de una
#                      proteína, como su acceso primario y descripción (ambos
#                      opcionales), una lista de genes y una secuencia.
#
# Estos modelos aprovechan las capacidades de Pydantic para la validación
# automática de tipos y la serialización/deserialización de datos.
'''


from pydantic import BaseModel, Field
from typing import Optional, List

class Sequence(BaseModel):
    value: str
    length: int
    molWeight: Optional[int] = None
    crc64: Optional[str] = None
    md5: Optional[str] = None
    
class Gene(BaseModel):
    geneName: str
    orderedLocusNames: str

class Protein(BaseModel):
    primaryAccession: str
    genes: List[Gene]
    sequence: Sequence
    proteinDescription: Optional[str] = None

class QueryResponse(BaseModel):
    primaryAccession: Optional[str]= None
    proteinDescription: Optional[str]
    genes: List[Gene]
    sequence: Sequence
    

    
'''
ANTES EN EL MAIN
class Gene(BaseModel):
    gene: str
    description: str

class GeneResponse(BaseModel):
    resultados: List[Gene]
    total: int
    page: int
    size: int
'''