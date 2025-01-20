# FICHERO TODO EN UNO

import requests
import time
import json
import os
# from src.uniprot_downloader import numeroEntradas(query)
#from src.descargas.uniprot_downloader import numeroEntradas
#import sys
# sys.path.append('/ruta/a/mi_proyecto/src')
#sys.path.append('/src/descargas/numeroEntradas')

# Crear una carpeta para almacenar los archivos .json si no existe
carpeta_descargas = "descargas_json"
if not os.path.exists(carpeta_descargas):
    os.makedirs(carpeta_descargas)

# Función para hacer consultas a UniProt y obtener los datos en bloques
def descargar_datos_uniprot(query, limit=100, offset=0, format='json'):
    url = "https://rest.uniprot.org/uniprotkb/search"
    params = {
        'query': query, # Organismo
        'format': format,
        'size': limit,
        'offset': offset # Desplazamiento
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al descargar datos de UniProt: {response.status_code}")
        return None


# Función para buscar proteínas revisadas (validadas) por taxón específico
def buscar_proteinas_revisadas_por_taxon(taxon_id):
    # URL para buscar solo proteínas validadas (reviewed) asociadas a un taxón específico
    url = f"https://rest.uniprot.org/uniprotkb/search?query=organism_id:{taxon_id}+AND+reviewed:true&format=json"

    # Realizar la solicitud GET a la API
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        datos = response.json()

        # Verificar si hay resultados
        if 'results' in datos and datos['results']:
            print(f"Proteínas validadas asociadas al taxón {taxon_id}:")
            # Recopilar los IDs de proteínas revisadas
            ids_proteinas = []
            for resultado in datos['results']:
                id_uniprot = resultado.get('primaryAccession', 'No disponible')
                nombre = resultado.get('proteinDescription', {}).get('recommendedName', {}).get('fullName', 'No disponible')
                ids_proteinas.append(id_uniprot)
                print(f"ID UniProt: {id_uniprot} - Nombre: {nombre}")
            return ids_proteinas
        else:
            print(f"No se encontraron proteínas validadas para el taxón {taxon_id}.")
            return []
    else:
        print(f"Error en la búsqueda del taxón {taxon_id}. Estado: {response.status_code}")
        return []


# Función para descargar toda la información de una proteína específica por su ID
def descargar_toda_la_informacion_proteina(id_proteina):
    # URL de la API de UniProt para obtener toda la información de la proteína
    url = f"https://rest.uniprot.org/uniprotkb/{id_proteina}.json"

    # Realizar la solicitud GET a la API
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Parsear el contenido JSON de la respuesta
        datos = response.json()

        # Imprimir información relevante (puedes personalizar esto según tus necesidades)
        print(f"\nID Proteína: {id_proteina}")
        print(json.dumps(datos, indent=4))  # Muestra toda la información en formato JSON

        # Devolver todos los datos
        return datos
    else:
        print(f"Error al descargar la información de la proteína {id_proteina}. Estado: {response.status_code}")
        return None
'''
# Función para obtener el número total de entradas para la consulta
def obtener_numero_entradas(query):
    url = "https://rest.uniprot.org/uniprotkb/search"
    params = {
        'query': query,
        'format': 'json',
        'size': 0  # Solo metadatos, no descargaremos resultados completos
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            datos = response.json()
            total_entradas = datos.get('meta', {}).get('totalResults', 0)
            print(f"Total de entradas encontradas: {total_entradas}")
            return total_entradas
        else:
            print(f"Error al obtener el número de entradas. Código de estado: {response.status_code}")
            return 0
    except Exception as e:
        print(f"Error al realizar la solicitud: {e}")
        return 0
'''

# Función para gestionar la descarga por bloques desde una búsqueda general
def proceso_descarga(query, limit=100, total=1000, delay=2):
    offset = 0
    while offset < total:
        print(f"Descargando bloque desde {offset} hasta {offset + limit}...")
        datos = descargar_datos_uniprot(query, limit=limit, offset=offset)

        if datos and 'results' in datos:

            # Guardar los datos en un archivo JSON dentro de la carpeta "descargas"
            archivo_json = os.path.join(carpeta_descargas, f"datos_uniprot_{offset}_{offset + limit}.json")
            with open(archivo_json, 'w') as archivo:
                json.dump(datos['results'], archivo, indent=4)

            # Para visualizar lo que estamos descargando
            print(f"Resultados descargados: {len(datos['results'])} proteínas.")
            for resultado in datos['results']:
                print(f"ID UniProt: {resultado.get('primaryAccession', 'No disponible')} - Nombre: {resultado.get('proteinDescription', {}).get('recommendedName', {}).get('fullName', 'No disponible')}")
            yield datos['results']  # Usamos yield para devolver bloques de datos en lugar de todo de una vez
        else:
            print("No se encontraron más datos o ocurrió un error.")
            break

        offset += limit
        time.sleep(delay)  # Pausa para evitar sobrecargar la API



def main():

    #query = "organism_id:9606 AND reviewed:true"
    query = "ATCC 14579"
    # query = "Bacillus cereus"
    # query = "1396"
    limit = 100
    total = 500  # Ajusta según lo que se quiera descargar
    delay = 2  # Para evitar demasiadas peticiones rápidas

    # Proceso de descarga de datos
    for datos in proceso_descarga(query=query, limit=limit, total=total, delay=delay):
        print("Bloque descargado:")
        print(datos)  # Imprimir cada bloque de datos descargados


if __name__ == "__main__":
    main()
