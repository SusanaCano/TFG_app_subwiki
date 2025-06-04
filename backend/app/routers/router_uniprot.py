# backend/app/routers/router_uniprot.py

"""
Este módulo define un APIRouter de FastAPI para gestionar las funcionalidades
relacionadas con datos de UniProt. Proporciona endpoints para:

 Buscar proteínas en UniProt (con paginación):
    - Endpoint: GET /uniprot/buscar
    - Parámetros de consulta:
        - `query` (str, obligatorio): El término a buscar.
        - `page_num` (int, opcional, por defecto: 1): Número de página deseado.
        - `page_size` (int, opcional, por defecto: 10): Cantidad de resultados por página.
    - Lógica principal: Llama a `obtener_resultados_tabla` (de
      `app.consultas.consulta_uniprot_tabla`) para obtener la lista completa
      de coincidencias y luego aplica paginación internamente.
    - Modelo de respuesta: `Page[QueryResponse]`. Devuelve un objeto que incluye
      la lista de resultados para la página (`result`), el total de ítems
      encontrados (`total`), el número de página actual (`page`) y el tamaño
      de página (`size`).
      
      
"""

from fastapi import APIRouter, HTTPException 
from typing import List
from app.models.models_data_mongo import QueryResponse 
from app.models.models_page_consultas import Page
from app.consultas.consulta_uniprot_tabla import obtener_resultados_tabla 
from app.models.models_page_consultas import Page
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/uniprot",
    tags=["UniProt"] 
)

@router.get("/buscar", response_model=Page[QueryResponse])
async def search_uniprot_data(query: str, page_num: int = 1, page_size: int = 10):
    """
    Busca proteínas en la base de datos UniProt utilizando un término de consulta.
    Esta ruta utiliza la función `obtener_resultados_tabla`.
    """
    logger.info(f"Router: Solicitud a /uniprot/buscar con query='{query}'")
    
    try:

        todos_los_resultados: List[QueryResponse] = await obtener_resultados_tabla(query)
        
        total_items: int = len(todos_los_resultados)
        
        # Lógica de paginación 
        start_index = (page_num - 1) * page_size
        end_index = start_index + page_size
        resultados_paginados: List[QueryResponse] = todos_los_resultados[start_index:end_index]
        
        logger.info(f"Router: Devolviendo {len(resultados_paginados)} de {total_items} resultados para query='{query}' (página {page_num}, tamaño {page_size}).")
        
       
        return {
            "result": resultados_paginados,  # La lista de ítems para la página actual
            "total": total_items,            # El número total de ítems
            "page": page_num,                # El número de página actual
            "size": page_size                # El tamaño de la página
        }
        
    except HTTPException as http_exc:
        logger.info(f"Router: Propagando HTTPException desde /uniprot/buscar: Status={http_exc.status_code}, Detail='{http_exc.detail}' para query='{query}'")
        raise http_exc

    except ValueError as ve: 
        logger.error(f"Router: Error de validación (ValueError) en /uniprot/buscar con query='{query}': {str(ve)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        logger.error(f"Router: Error INESPERADO en /uniprot/buscar con query='{query}': {type(e).__name__} - {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno del servidor al procesar la búsqueda.")
