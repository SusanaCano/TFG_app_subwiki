# backend/feature/uniprot/tests/test_buscar.py

'''
# Este archivo contiene pruebas de integración asíncronas utilizando Pytest
# para el endpoint `/buscar` de la funcionalidad UniProt de la aplicación FastAPI.
#
# Las pruebas se realizan directamente contra la aplicación ASGI (`app`)
# utilizando `httpx.AsyncClient` y `ASGITransport`. También incluye
# una fixture (`event_loop`) para gestionar el bucle de eventos asyncio
# durante la sesión de prueba y asegurar la estabilidad en entornos asíncronos.
# El objetivo principal es verificar la respuesta exitosa (código 200)
# del endpoint `/buscar` ante una consulta de ejemplo.

'''

import pytest
import asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient
from httpx import ASGITransport
from app.main import app

# Para evitar problemas de "loop is closed" en Python 3.8
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.mark.asyncio
async def test_buscar_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/buscar", params={"query": "BC_2340"})
        assert response.status_code == 200
        print(response.json())
