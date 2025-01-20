import os
import time
import json
from db import descargar_datos_uniprot

# Función para gestionar la descarga por bloques desde una búsqueda general

def proceso_descarga(query, limit=500, total=6000, delay=2, descargas_json="descargas"):
    """
    Descarga datos en bloques y los guarda en archivos JSON.

    :param query: Cadena de consulta.
    :param limit: Número de resultados por bloque.
    :param total: Número total de resultados a descargar.
    :param delay: Tiempo de espera entre solicitudes.
    :param descargas_json: Carpeta donde se guardarán los archivos.
    """
    if not os.path.exists(descargas_json):
        os.makedirs(descargas_json)

    offset = 0

    while offset < total:
        print(f"Descargando bloque desde {offset} hasta {offset + limit}...")
        datos = descargar_datos_uniprot(query, limit=limit, offset=offset)

        if datos and 'results' in datos:

            # Guardar los datos en un archivo JSON dentro de la carpeta "descargas"
            archivo_json = os.path.join(descargas_json, f"datos_uniprot_{offset}_{offset + limit}.json")
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
