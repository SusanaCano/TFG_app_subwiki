# backend/app/routers/router_kegg.py

'''
# Este módulo define un APIRouter de FastAPI (`kegg_router`) dedicado a
# gestionar solicitudes relacionadas con datos de KEGG.
#
# Funcionalidad Principal:
#   - Establece un prefijo de ruta `/kegg_data` y una etiqueta "KEGG Data"
#     para la documentación OpenAPI.
#   - Define un modelo Pydantic `GenIdRequest` para posibles cuerpos de
#     solicitud (aunque no se utiliza en el endpoint actualmente visible).
#   - Proporciona un endpoint principal:
#     - `GET /kegg/{entry}`:
#       - Diseñado para recuperar información de una ruta metabólica de KEGG
#         basándose en un `entry` ID (ej. "ko00010", "bce00010").
#       - Depende de una conexión a la base de datos MongoDB (`db`) inyectada.
#       - Llama a la función de servicio `obtener_ruta_metabolica` (de
#         `app.services.kegg_service`) para realizar la lógica de obtención
#         de datos.
#       - Devuelve los datos directamente como `JSONResponse` si se encuentran.
#       - Maneja errores y casos de "no encontrado" devolviendo un objeto
#         JSON con una clave "error".
#
# El objetivo es exponer una API para acceder a datos específicos de KEGG
# obtenidos a través de un servicio y una base de datos.
'''

from fastapi import APIRouter, Depends
from app.config.db import get_database
from pydantic import BaseModel
from app.services.kegg_service import obtener_ruta_metabolica
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorDatabase


kegg_router = APIRouter(prefix="/kegg_data", tags=["KEGG Data"])

class GenIdRequest(BaseModel):
    genId: str

@kegg_router.get("/kegg/{entry}")
async def get_kegg_route(entry: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    try:
        print(f"Buscando entrada: {entry}")
        ruta_metabolica =  await obtener_ruta_metabolica(entry, db)
        print(f"Resultado: {ruta_metabolica}")
        if ruta_metabolica:
            return JSONResponse(content=ruta_metabolica)
        return {"error": "Ruta metabólica no encontrada"}
    except Exception as e:
        return {"error": str(e)}
