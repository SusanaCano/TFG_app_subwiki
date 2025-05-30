# backend/app/routers/router_uniprot.py

'''
# Este módulo define un APIRouter de FastAPI para gestionar las funcionalidades
# relacionadas con datos de UniProt. Proporciona endpoints para:
#
# 1.  Obtener una proteína específica por su ID:
#     - Endpoint: `GET /uniprot/{protein_id}`
#     - Llama a `get_protein_by_id` para la lógica de base de datos.
#     - Utiliza `ProteinResponse` como modelo de respuesta.
#
# 2.  Obtener proteínas basadas en un valor de "locus name":
#     - Endpoint: `GET /uniprot/proteins/by-locus/{locus_value}`
#     - Llama a `get_proteins_by_locus_name`.
#
# 3.  Realizar una búsqueda general de proteínas utilizando un término de consulta:
#     - Endpoint: `GET /uniprot/buscar`
#     - Llama a `obtener_resultados` (de `app.consultas.consulta2`).
#     - Utiliza `List[QueryResponse]` como modelo de respuesta.
#
# Todas las rutas definidas aquí están bajo el prefijo `/uniprot`.
# El módulo implementa manejo de errores con `HTTPException` para casos como
# "no encontrado" (404) o errores internos (500), e incorpora logging
# para registrar eventos relevantes.
'''

from fastapi import APIRouter, HTTPException, Depends
from app.features.uniprot.schemas_uniprot import ProteinResponse
from app.features.uniprot.models_uniprot import get_protein_by_id
from app.features.uniprot.models_uniprot import get_proteins_by_locus_name
from app.consultas.consulta2 import obtener_resultados
from app.models.models_data_mongo import QueryResponse 
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/uniprot")

@router.get("/{protein_id}", response_model=ProteinResponse)
async def get_protein(protein_id: str):
    """Busca una proteína en MongoDB por su ID"""
    protein = await get_protein_by_id(protein_id)
    
    if not protein:
        raise HTTPException(status_code=404, detail="Proteína no encontrada")
    
    return protein

@router.get("/proteins/by-locus/{locus_value}")
async def get_proteins_by_locus(locus_value: str):
    proteins = await get_proteins_by_locus_name(locus_value)
    if not proteins:
        raise HTTPException(status_code=404, detail="No se encontraron proteínas")
    return proteins

'''
@router.get("/buscar", response_model=List[QueryResponse])
async def buscar(query: str):
    # Aquí debes realizar la consulta utilizando el 'query' recibido
    # Puedes usar la lógica de búsqueda que ya has creado
    #resultados = await obtener_resultados(query)  # O la función que use para obtener datos
    resultados = obtener_resultados(query)

    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron resultados")
    
    #return {"resultados": resultados}
    #return [QueryResponse(**dato) for dato in resultados]
        return [
        {"id": "P12345", "name": "Test Protein", "function": "Test Func", "organism": "Homo sapiens"}
    ]
'''

@router.get("/buscar", response_model=List[QueryResponse])
async def buscar(query: str):
    try:
        resultados = await obtener_resultados(query)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
    
    if not resultados:
        logger.warning("No se encontraron documentos que coincidan con la consulta.")
        raise HTTPException(status_code=404, detail="No se encontraron resultados")
    
    return resultados
