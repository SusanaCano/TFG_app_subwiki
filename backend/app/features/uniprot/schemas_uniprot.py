# backend/app/festures/uniprot/shemas_uniprot.py

'''
# Este módulo define los modelos de datos utilizando Pydantic (`BaseModel`)
# para estructurar, validar y serializar la información relacionada con
# proteínas, genes y secuencias. Modelos típicos, utilizados
# en una aplicación FastAPI para definir los esquemas de las solicitudes
# y respuestas de la API.
#
# Modelos definidos:
#   - `Gene`: Representa la información de un gen, incluyendo su nombre
#             (`geneName`) y, opcionalmente, un nombre de locus ordenado
#             (`orderedLocusName`).
#   - `Sequence`: Define una secuencia biológica con su valor de cadena
#                 (`value`) y su longitud (`length`).
#   - `ProteinResponse`: Es un modelo compuesto que representa la respuesta
#                        detallada de una proteína. Agrupa la descripción de
#                        la proteína (`proteinDescription`), una lista de
#                        objetos `Gene` y una lista de objetos `Sequence`.
#                        Incluye una configuración Pydantic (`Config`) para
#                        manejar la serialización de `ObjectId` de MongoDB
#                        a cadenas en las respuestas JSON.

'''

from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

class Gene(BaseModel):
    geneName: str
    orderedLocusName: Optional[str] = None

class Sequence(BaseModel):
    value: str
    length: int

class ProteinResponse(BaseModel):
    proteinDescription: str
    genes: List[Gene]
    sequence: List[Sequence]
    
    class Config:
        # Esto convierte los valores de ObjectId a string cuando se responde a una solicitud
        json_encoders = {
            ObjectId: str
        }
