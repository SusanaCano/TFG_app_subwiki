# backend/app/routers/api_uniprot.py

'''
Este módulo define un endpoint de API utilizando FastAPI (`APIRouter`)
# para la funcionalidad de búsqueda de proteínas.
#
# Endpoint Definido:
#   - GET `/buscar`:
#     - Responsable de recibir un término de búsqueda (`query`) como parámetro.
#     - Invoca la función asíncrona `obtener_resultados` del módulo
#       `app.consultas.consulta2` para realizar la lógica de consulta
#       a la base de datos.
#     - Utiliza el modelo Pydantic `Protein` (de `app.models`) como
#       `response_model` para validar y serializar la respuesta.
#     - Devuelve los resultados obtenidos de la función de consulta.

'''

from fastapi import APIRouter
from app.models import Protein
from app.consultas.consulta2 import obtener_resultados

router = APIRouter()

@router.get("/buscar", response_model=Protein)
async def buscar(query: str):
    # Llamada a la función que hace la consulta
    resultados = await obtener_resultados(query)
    return resultados
