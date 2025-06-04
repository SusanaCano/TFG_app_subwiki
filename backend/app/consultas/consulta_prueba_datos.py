# backend/app/consultas/consulta_prueba_datos.property

'''
    Recupera de forma asíncrona un conjunto limitado de documentos de la
    colección 'UniProt' en MongoDB.

    Esta función accede a la colección 'UniProt' a través del cliente `db`
    configurado globalmente. Intenta obtener hasta los primeros 2 documentos
    de esta colección usando `.limit(2)`. La parte `await ...to_list(length=10)`
    se usa para convertir el cursor a una lista; aunque se especifica `length=10`,
    el número efectivo de documentos estará restringido por el `.limit(2)`
    precedente, lo que significa que `to_list` procesará como máximo 2 documentos.

    La función también incluye sentencias `print` a la consola:
    - "No se encontraron datos en la colección UniProt" si la consulta no devuelve documentos.
    - "Datos obtenidos: {datos}" mostrando los documentos recuperados si se encuentra alguno.
'''

from app.config.db import db

async def obtener_datos():
    try:
        # Obtener la colección UniProt
        collection = db["UniProt"]
        
        # Obtener los primeros 5 documentos de la colección UniProt
        datos = await collection.find().limit(2).to_list(length=5)
        if not datos:
            print("No se encontraron datos en la colección UniProt")
        else:
            print(f"Datos obtenidos: {datos}")
        return datos
    except Exception as e:
        raise Exception(f"Error al obtener datos: {e}")
