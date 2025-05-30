# FICHERO TODO EN UNO
'''
Script para descargar datos de proteínas desde UniProt en formato JSON.

Funcionalidades:
- Realiza búsquedas en UniProt por una consulta (query) y descarga los resultados en bloques.
- Guarda los datos descargados en archivos `.json` dentro de una carpeta local.
- Muestra el número total de entradas disponibles en UniProt para la consulta.
- Cuenta las entradas descargadas por bloque y el total acumulado.
- Al finalizar, compara las entradas descargadas con el total disponible en UniProt.


- La variable `query` especificar el organismo o taxón.
- Definir el tamaño de los bloques (`limit`) y el número máximo de entradas a descargar (`total`).
- Se puede usar el total real de UniProt como límite para descargar todas las entradas disponibles.
'''
import requests
import time
import json
import os


# Crear una carpeta para almacenar los archivos .json si no existe
carpeta_descargas = "descargas_Uniprote_json"
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
    
# Función para obtener el número total de entradas para la consulta
def obtener_numero_entradas(query):
    url = "https://rest.uniprot.org/uniprotkb/search"
    params = {
        'query': query,
        'format': 'json',
        'size': 1  # Solo metadatos
    }
    headers = {
        'Accept': 'application/json'
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        
        print(f"Solicitando el número total de entradas con la consulta: {query}")
        print(f"Estado de la respuesta: {response.status_code}")
        
        if response.status_code == 200:
           
            total_entradas = response.headers.get("x-total-results")
            if total_entradas is not None:
                print(f"Total de entradas disponibles en UniProt para la consulta '{query}': {total_entradas}")
                return int(total_entradas)
            else:
                print("No se encontró el encabezado 'x-total-results'.")
                print("Respuesta completa:", response.json())
                return 0
        
        else:
            print(f"Error al obtener el número de entradas. Código de estado: {response.status_code}")
            return 0
    except Exception as e:
        print(f"Error al realizar la solicitud: {e}")
        return 0


# Función para gestionar la descarga por bloques desde una búsqueda general
def proceso_descarga(query, limit=100, total=1000, delay=2):
    offset = 0
    while offset < total:
        print(f"Descargando bloque desde {offset} hasta {offset + limit}...")
        datos = descargar_datos_uniprot(query, limit=limit, offset=offset)
              
        if datos and 'results' in datos:

            # Guardar los datos en un archivo JSON dentro de la carpeta "descargas_Uniprot_json"
            archivo_json = os.path.join(carpeta_descargas, f"datos_uniprot_{offset}_{offset + limit}.json")
            with open(archivo_json, 'w') as archivo:
                json.dump(datos['results'], archivo, indent=4)

            # Para visualizar los descargando
            print(f"Resultados descargados: {len(datos['results'])} proteínas.")
            for resultado in datos['results']:
                print(f"ID UniProt: {resultado.get('primaryAccession', 'No disponible')} - Nombre: {resultado.get('proteinDescription', {}).get('recommendedName', {}).get('fullName', 'No disponible')}")
            yield datos['results']  #
            print("No se encontraron más datos o ocurrió un error.")
            break

        offset += limit
        time.sleep(delay)  # Pausa para evitar sobrecargar la API



def main():
      # EN UNIPROT HAY  20,421 RESULTS
    #query = "organism_id:9606 AND reviewed:true"
    
    # EN UNIPROT HAY 5,343 RESULTS
    #query = "ATCC 14579"
    
    # EN UNIPROT HAY 1,107,343 RESULTS
    #query = "Bacillus cereus"
    
     # EN UNIPROT HAY 393,496  RESULTS
    #query = "1396"
    
    #query = "organism:\"Bacillus cereus (ATCC 14579)\" AND reviewed:true"
    #query = "taxonomy_id:226900 AND reviewed:true"
    
    # EN UNIPROT HAY 676 RESULTS
    #query = "organism:ATCC 14579 AND reviewed:true"

    # EN UNIPROT HAY 5260 RESULTS    
    query = 'organism_id:226900'

    limit = 500
    total = obtener_numero_entradas(query)  # Obtener el número total de entradas
    delay = 2  # Para evitar demasiadas peticiones rápidas
   
    # Verificar si se pudo obtener el número total
    if total == 0:
        print("No se pudo obtener el número total desde UniProt. Se usará el total descargado como referencia.")
        total = 0  # Usar 0 como un valor de fallback en caso de error al obtener el total.

    # Obtener el número total disponible en UniProt
    print(f"Total de entradas disponibles en UniProt para la consulta '{query}': {total}\n")

    entradas_descargadas = 0  # Contador total real

    # Descargar en bloques
    for datos in proceso_descarga(query=query, limit=limit, total=total, delay=delay):
        cantidad_bloque = len(datos)
        entradas_descargadas += cantidad_bloque
        print(f"Entradas descargadas en este bloque: {cantidad_bloque}")
        print(f"Total acumulado hasta ahora: {entradas_descargadas}\n")

    print("Descarga completada.")
    print(f"Total de entradas descargadas: {entradas_descargadas}")
    print(f"Total disponible en UniProt: {total}")

    # Verificar si hemos descargado todas las entradas disponibles
    if entradas_descargadas >= total:
        print("Se han descargado todas las entradas disponibles.")
    else:
        print("Faltan entradas por descargar. Revisa el límite definido o posibles errores en la descarga.")

    

if __name__ == "__main__":
    main()
