# app/consultas/consulta2.py
from app.config.db import db

async def obtener_resultados(query_dict):
    try:
     # Imprimir la consulta para verificar que el formato es correcto
        #print(f"Consulta: '{query_dict}' (tipo: {type(query_dict)})")
       
    # Realiza la consulta en la colección UniProt usando el query_dict que se pasa como parámetro
        resultados_cursor = db['UniProt'].find(query_dict, {
            "proteinDescription": 1,
            "genes.geneName.value": 1,
            "genes.orderedLocusNames.value": 1,
            "sequence.value": 1,
            "sequence.length": 1
        })

    # Convertir el cursor en una lista de resultados
        resultados = await resultados_cursor.to_list(length=None)

    # Verificar si los resultados están vacíos
        if not resultados:
            print("No se encontraron resultados.")
        
        return resultados

    except Exception as e:
        print(f"Error en la consulta: {str(e)}")
        return []  # Retornar una lista vacía en caso de error





#from pymongo import MongoClient

# Conectar a MongoDB (asegúrate de que tu conexión a MongoDB esté configurada correctamente)
#client = MongoClient('mongodb://localhost:27017/')  # Asegúrate de que la URL y puerto coincidan con los de tu servidor MongoDB
#db = client['TuBaseDeDatos']  # Reemplaza 'TuBaseDeDatos' con el nombre de tu base de datos

# Realizar la consulta
'''
resultados = db['UniProt'].find({
    "$or": [
        {"_id": "Q81DL9"},  # Reemplaza con el id, si es necesario
        {"genes.geneName.value": "BC_2340"},
        {"genes.orderedLocusNames.value": "BC_2340"}
    ]
}, {
    "proteinDescription": 1,
    "genes.geneName.value": 1,
    "genes.orderedLocusNames.value": 1,
    "sequence.value": 1,
    "sequence.length": 1
})

# Mostrar los resultados
for resultado in resultados:
    print(resultado)
'''