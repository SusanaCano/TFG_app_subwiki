'''

import pytest
from app.services.kegg_service import obtener_ruta_metabolica
from unittest.mock import MagicMock

# Simulamos la base de datos de MongoDB
@pytest.fixture
def mock_db():
    # Creamos una conexión falsa a MongoDB usando MagicMock
    mock_db = MagicMock()
    mock_collection = MagicMock()
    mock_db["kegg_rutas"] = mock_collection
    return mock_db

# Prueba para obtener una ruta metabólica
def test_obtener_ruta_metabolica(mock_db, mocker):
    # Simulamos que la función 'db' de app.config.db devuelve el mock
    mocker.patch("app.config.db", mock_db)
    
    # Datos de prueba
    gen_id = "BC_2340"
    ruta_metabolica = {"genId": "BC_2340", "ruta": "Ruta metabólica de prueba"}
    
    # Configuramos el mock para que devuelva la ruta metabólica cuando se haga la consulta
    mock_db["kegg_rutas"].find_one.return_value = ruta_metabolica
    
    # Llamamos a la función obtener_ruta_metabolica
    result = obtener_ruta_metabolica(gen_id)
    
    # Verificamos que el resultado sea correcto
    assert result == ruta_metabolica, f"Se esperaba {ruta_metabolica}, pero se obtuvo {result}"

# Prueba para cuando no se encuentra la ruta metabólica
def test_obtener_ruta_metabolica_no_encontrada(mock_db, mocker):
    # Simulamos que la función 'db' de app.config.db devuelve el mock
    mocker.patch("app.config.db", mock_db)
    
    gen_id = "BC_2340"
    
    # Configuramos el mock para que devuelva None cuando no haya coincidencia
    mock_db["kegg_rutas"].find_one.return_value = None
    
    # Llamamos a la función obtener_ruta_metabolica
    result = obtener_ruta_metabolica(gen_id)
    
    # Verificamos que no se encontró la ruta metabólica
    assert result is None, f"Se esperaba None, pero se obtuvo {result}"
'''