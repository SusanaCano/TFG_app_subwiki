# backend/app/test_mongo_connection_con_datos.py

'''
# Este archivo contiene pruebas Pytest diseñadas para verificar la conexión
# a la base de datos MongoDB y la capacidad de recuperar datos utilizando
# la función `obtener_datos` del módulo `app.consultas.consulta_prueba_datos`.
#
# La prueba principal (`test_mongo_connection_con_datos`):
#   - Es asíncrona (`@pytest.mark.asyncio`).
#   - Carga variables de entorno usando `dotenv` (presumiblemente para
#     configurar la conexión a la base de datos).
#   - Llama a `obtener_datos()` para intentar obtener datos de MongoDB.
#   - Verifica que se haya devuelto al menos un documento (es decir, `len(datos) > 0`).
#   - Falla si se produce cualquier excepción durante el proceso, indicando
#     un problema con la conexión o la obtención de datos.
#
# El objetivo es asegurar que la configuración de la base de datos es correcta
# y que la función `obtener_datos` puede interactuar exitosamente con ella.
# Es una prueba de integración básica para la capa de acceso a datos.
'''

import pytest
from dotenv import load_dotenv
from app.consultas.consulta_prueba_datos import obtener_datos

load_dotenv() 

@pytest.mark.asyncio
async def test_mongo_connection_con_datos():
    try:
    # Intentamos obtener los documentos, como en la función del endpoint
        datos = await obtener_datos()  # Llamamos a la función que obtiene los datos
        print(f"Datos obtenidos: {datos}")  # Imprimir para depuración
     
        # Verificamos que se obtuvieron datos
        assert len(datos) > 0, "No se obtuvieron datos de la base de datos"
        
        # Si no se lanza ninguna excepción, la prueba pasa
        assert True
    except Exception as e:
        assert False, f"Conexión a MongoDB falló: {e}"