# backend/feature/uniprot/tests/test_buscar.py

'''
# Este archivo contiene pruebas unitarias asíncronas utilizando Pytest para la
# función `obtener_resultados` del módulo `app.consultas.consulta4`.
#
# Las pruebas utilizan `unittest.mock.patch` y `unittest.mock.AsyncMock` para
# simular las interacciones con la base de datos MongoDB (`db`), permitiendo
# testear la lógica de la función de forma aislada.
#
# Se cubren los siguientes escenarios principales:
# 1. Recuperación exitosa de resultados válidos.
# 2. Manejo del caso en que no se encuentran resultados (esperando HTTPException 404).
# 3. Manejo de errores inesperados durante la interacción con la base de datos
#    (esperando una HTTPException, implícitamente 500).
#
# Incluye una fixture (`setup_event_loop`) para gestionar el bucle de eventos
# asyncio durante la sesión de prueba, asegurando la correcta ejecución de
# las pruebas asíncronas.
'''

import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
from app.consultas.consulta4 import obtener_resultados
from fastapi import HTTPException
#from bson import ObjectId
from app.models.models_data_mongo import QueryResponse, Gene
from app.config.db import db

@pytest.fixture(scope="session", autouse=True)
def setup_event_loop():
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        oop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    yield loop
    loop.close()

@pytest.mark.asyncio
@patch("app.consultas.consulta4.db")  # Este es el db importado en consulta4.py
async def test_obtener_resultados_valido(mock_db):
    # Simulación del resultado esperado
    resultado_simulado = [{
        "_id": "fakeid123",
        "primaryAccession": "Q81DL9",
        "genes": [
            {
                "geneName": "fakeGene",
                "orderedLocusNames": [{"value": "BC_2340"}]
            }
        ],
        "sequence": {
            "value": "ATGC",
            "length": 4,
            "molWeight": 12345,
            "crc64": "ABC123",
            "md5": "md5hash"
        },
        "proteinDescription": {
            "submissionNames": [
                {
                    "fullName": {
                        "value": "Some Protein"
                    }
                }
            ]
        }
    }]

    # Mock de find().to_list()
    mock_cursor = AsyncMock()
    mock_cursor.to_list.return_value = resultado_simulado
    mock_db.__getitem__.return_value.find.return_value = mock_cursor

    resultados = await obtener_resultados("BC_2340")
    
    assert isinstance(resultados, list)
    assert len(resultados) == 1
    #assert resultados[0].primaryAccession == "Q81DL9"
    assert isinstance(resultados[0], QueryResponse)
    assert resultados[0].proteinDescription == "Some Protein"
    assert resultados[0].genes[0].orderedLocusNames == "BC_2340"
    assert resultados[0].sequence.value == "ATGC"
    
'''   
@pytest.mark.asyncio
async def test_obtener_resultados_valido():
    # Aquí puedes usar un ciclo de eventos de manera explícita si es necesario
    loop = asyncio.get_event_loop()
    
    # Crear un mock para la colección de MongoDB
    db_mock = MagicMock()
    db_mock['UniProt'].find.return_value.to_list.return_value = [
        {
            #"_id": ObjectId(),
            "_id": "60d0fe4f5311236168a109f1",
            "proteinDescription": {"submissionNames": [{"fullName": {"value": "Protein 1"}}]},
            "genes": [{"geneName": "Gene1", "orderedLocusNames": [{"value": "Ordered Name 1"}]}],
            "sequence": {"value": "ATCG", "length": 4}
        }
    ]

    # Inyectamos el mock en la función
    resultados = await obtener_resultados("Protein 1")

    assert len(resultados) > 0  # Asegúrate de que los resultados sean correctos
    #assert len(resultados) == 1  # Esperamos 1 resultado
    #assert resultados[0].proteinDescription == "Protein 1"
    #assert len(resultados[0].genes) == 1  # Esperamos 1 gen
    #assert resultados[0].sequence == "ATCG"
    #assert resultados[0].sequenceLength == 4
''' 

@pytest.mark.asyncio
@patch("app.consultas.consulta4.db")  # Mock de la base de datos
async def test_obtener_resultados_no_encontrado(db_mock):
    # Simulamos que no se encuentran resultados
    to_list_mock = AsyncMock(return_value=[])

    # Parcheamos la variable db que se importa en consulta4
    #with patch("app.consultas.consulta4.db") as db_mock:
    
        # db['UniProt'].find().to_list() -> []
    db_mock.__getitem__.return_value.find.return_value.to_list = to_list_mock

        # Llamamos a la función normalmente (sin pasar `db`)
    with pytest.raises(HTTPException) as exc_info:
        await obtener_resultados("Nonexistent Protein")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "No se encontraron resultados"

@pytest.mark.asyncio
async def test_obtener_resultados_errores():
    # Simulamos que ocurre un error inesperado
    db_mock = MagicMock()
    db_mock['UniProt'].find.side_effect = Exception("Database error")

    # Inyectamos el mock y verificamos que se lanza un HTTPException
    with pytest.raises(HTTPException):
        await obtener_resultados("BC_2340")
