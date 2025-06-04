# backend/app/models/models_page_consultas.py

'''
# Este módulo define un modelo Pydantic genérico para la paginación,
# diseñado para estandarizar las respuestas de API que devuelven listas
# de datos divididas en páginas.
#
# Modelo Definido:
#   - `Page(BaseModel, Generic[T])`:
#     Un modelo de respuesta genérico para datos paginados. Utiliza `TypeVar`
#     y `Generic` de Python para permitir que el campo `items` contenga una
#     lista de cualquier tipo de modelo Pydantic específico (representado por `T`).
#
#     Atributos:
#       - `result  (List[T])`: La lista de elementos para la página actual.
#                            El tipo `T` será reemplazado por el modelo
#                            específico de los datos.
#       - `total (int)`: El número total de elementos disponibles a través de
#                        todas las páginas.
#       - `page (int)`: El número de la página actual que se está devolviendo
#                       (generalmente 1-indexado).
#       - `size (int)`: El número máximo de elementos por página.
#
# Este modelo es útil para proporcionar una estructura consistente y metadatos
# de paginación claros en las API, facilitando la navegación a través de
# grandes conjuntos de datos por parte de los clientes.
'''

from pydantic import BaseModel
from typing import List, Dict, TypeVar, Generic
from pydantic import BaseModel
from app.models.models_data_mongo import QueryResponse

T = TypeVar('T')

class Page(BaseModel, Generic[T]):
    result: List[T]
    total: int
    page: int
    size: int
