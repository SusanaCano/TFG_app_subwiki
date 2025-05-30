# backend/tests/test_mongo_connection.py 

'''
# Este archivo contiene una prueba Pytest diseñada para verificar la conexión
# a la base de datos MongoDB.
#
# La prueba (`test_mongo_connection`):
#   - Es asíncrona (`@pytest.mark.asyncio`).
#   - Utiliza `dotenv` para cargar variables de entorno, que presumiblemente
#     contienen la configuración necesaria para la conexión a la base de datos
#     (por ejemplo, la URI de MongoDB).
#   - Llama a la función `check_connection` del módulo `app.config.db`.
#     Se espera que esta función intente establecer o verificar una conexión
#     a MongoDB y lance una excepción si falla.
#   - La prueba se considera exitosa si la llamada a `check_connection`
#     no produce ninguna excepción.
#   - Si se captura alguna excepción, la prueba falla, indicando un problema
#     con la conexión a MongoDB.
#
# El objetivo principal es asegurar que la aplicación puede establecer
# comunicación con la instancia de MongoDB configurada.
'''

import pytest
from dotenv import load_dotenv
from app.config.db import check_connection

load_dotenv() 

@pytest.mark.asyncio
async def test_mongo_connection():   
    # Llamar a la función que verifica la conexión
    try:
        # Verificamos la conexión a MongoDB
        await check_connection()
        assert True  # Si no se lanza ninguna excepción, la prueba pasa
    except Exception as e:
        assert False, f"Conexión a MongoDB falló: {e}"
    
    

