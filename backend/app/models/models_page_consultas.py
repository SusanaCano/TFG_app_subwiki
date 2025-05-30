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
#       - `items (List[T])`: La lista de elementos para la página actual.
#                            El tipo `T` será reemplazado por el modelo
#                            específico de los datos (ej. `List[User]`, `List[Product]`).
#       - `total (int)`: El número total de elementos disponibles a través de
#                        todas las páginas.
#       - `page (int)`: El número de la página actual que se está devolviendo
#                       (generalmente 1-indexado).
#       - `size (int)`: El número máximo de elementos por página.
#
# Este modelo es útil para proporcionar una estructura consistente y metadatos
# de paginación claros en las API, facilitando la navegación a través de
# grandes conjuntos de datos por parte de los clientes.
#
# Ejemplo de Uso (en un endpoint FastAPI):
#
#   from pydantic import BaseModel
#   # from .pagination import Page # Suponiendo que este archivo es pagination.py
#
#   class Item(BaseModel):
#       id: int
#       name: str
#
#   @router.get("/items", response_model=Page[Item])
#   async def list_items(page: int = 1, size: int = 10):
#       # ... lógica para obtener items_on_page y total_items ...
#       return Page[Item](items=items_on_page, total=total_items, page=page, size=size)
'''

from pydantic import BaseModel
from typing import List, Dict, TypeVar, Generic

T = TypeVar('T')

class Page(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
