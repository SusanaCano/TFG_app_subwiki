# Kegg/descargas_definiciones_rutas_kegg_kgml.py

'''
Script para descargar datos de rutas metabólicas de KEGG y sus archivos KGML.

Este script se conecta a la API REST de KEGG para obtener información sobre las
rutas metabólicas de un organismo específico. Para cada ruta, descarga:
1. Metadatos de la ruta (ID, nombre, URL de la imagen).
2. El contenido del archivo KGML (KEGG Markup Language) que describe la ruta.
3. Una lista de genes asociados a la ruta, obtenidos directamente de la API de KEGG.

Los datos recopilados para cada ruta se guardan en archivos individuales en formato JSON
dentro de un directorio de salida especificado. El script maneja reintentos para
las peticiones a la API y errores comunes.

Funciones principales:
- fetch_kegg_data_with_retry: Realiza peticiones a la API de KEGG con una lógica
  de reintentos robusta para manejar errores temporales de red o de la API.
- get_organism_pathway_metadata: Obtiene y parsea la lista de todas las rutas
  metabólicas para un organismo dado.
- get_genes_for_pathway_from_kegg: Obtiene la lista de genes de KEGG asociados
  a una ruta específica.
- main: Orquesta el proceso completo de obtención de metadatos de rutas, descarga
  de datos KGML y genes, y guardado de la información en archivos JSON.
'''


import os
import time
import requests
import json 
from pathlib import Path # Para manejo de rutas y creacion de carpetas
from dotenv import load_dotenv


load_dotenv() # Carga variables desde el archivo .env

KEGG_API_BASE_URL = "http://rest.kegg.jp"
ORGANISM_CODE = os.getenv("KEGG_ORGANISM_CODE", "bce")
REQUEST_DELAY_SECONDS = float(os.getenv("KEGG_REQUEST_DELAY", 0.34))

# Carpeta donde se guardaran los archivos JSON de las rutas
OUTPUT_JSON_DIR = "descargas_kegg_rutas_graficas_json" 


def fetch_kegg_data_with_retry(endpoint, retries=3, delay_multiplier=2, ignore_400_for_genes=False):
    
    url = f"{KEGG_API_BASE_URL}/{endpoint}"
    current_delay = REQUEST_DELAY_SECONDS
    for attempt in range(retries):
        try:
            time.sleep(current_delay)
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            if not response.text.strip():
                print(f"Advertencia: Respuesta vacia desde {url} en intento {attempt + 1}")
                if attempt < retries - 1:
                    current_delay *= delay_multiplier
                    continue
                return None
            return response.text
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"Recurso no encontrado (404) en {url}")
                return None
            
            if e.response.status_code == 400 and ignore_400_for_genes:
                print(f"Error HTTP 400 (Bad Request) en {url}. Se asume que no hay lista de genes disponible via este endpoint para esta ruta.")
                return None 
            
            print(f"Error HTTP {e.response.status_code} en {url}, intento {attempt + 1}/{retries}.")
        except requests.exceptions.RequestException as e:
            print(f"Error de red/peticion en {url}: {e}, intento {attempt + 1}/{retries}.")
        if attempt < retries - 1:
            current_delay *= delay_multiplier
        else:
            print(f"Fallo la obtencion de datos desde {url} despues de {retries} intentos.")
            return None
    return None


def get_organism_pathway_metadata(org_code):
    
    print(f"Obteniendo metadatos de rutas para el organismo: {org_code}")
    endpoint = f"list/pathway/{org_code}"
    data = fetch_kegg_data_with_retry(endpoint)
    pathways_metadata = []
    if data:
        for line in data.strip().split('\n'):
            if not line.strip(): continue
            parts = line.split('\t')
            if len(parts) >= 2:
                path_id_full_colon = parts[0]
                path_id_for_db = path_id_full_colon.replace("path:", "")
                pathways_metadata.append({
                    "pathway_id": path_id_for_db,
                    "name": parts[1],
                    "organism_code": org_code,
                    "image_url": f"http://www.kegg.jp/kegg/pathway/{org_code}/{path_id_for_db}.png"
                })
            else:
                print(f"Advertencia: No se pudo parsear la linea de metadatos de ruta: {line}")
    return pathways_metadata

def get_genes_for_pathway_from_kegg(pathway_id_with_org_prefix):
    
    print(f"Obteniendo genes de KEGG para la ruta: {pathway_id_with_org_prefix}")
    endpoint = f"get/{pathway_id_with_org_prefix}/genes"
    data = fetch_kegg_data_with_retry(endpoint, ignore_400_for_genes=True)
    gene_kegg_ids = []
    if data:
        for line in data.strip().split('\n'):
            if not line.strip(): continue
            parts = line.split('\t')
            if len(parts) >= 1:
                gene_kegg_id = parts[0]
                gene_kegg_ids.append(gene_kegg_id)
            else:
                print(f"Advertencia: No se pudo parsear la linea de gen para la ruta {pathway_id_with_org_prefix}: {line}")
    return gene_kegg_ids


def main():
    
    print(f"--- Iniciando descarga de datos graficos de rutas KEGG a archivos JSON ---")
    print(f"Organismo KEGG: {ORGANISM_CODE}")
    print(f"Archivos JSON se guardaran en: ./{OUTPUT_JSON_DIR}/")

    # Crear la carpeta de salida si no existe
    Path(OUTPUT_JSON_DIR).mkdir(parents=True, exist_ok=True)

    all_pathways_meta = get_organism_pathway_metadata(ORGANISM_CODE)

    if not all_pathways_meta:
        print(f"No se encontraron rutas para {ORGANISM_CODE} o hubo un error en la obtencion.")
        return

    print(f"Se encontraron {len(all_pathways_meta)} rutas para {ORGANISM_CODE}.")
    successful_downloads = 0
    failed_downloads = 0

    for i, p_meta in enumerate(all_pathways_meta):
        path_id = p_meta["pathway_id"] # ej: bce00010
        
        file_path = Path(OUTPUT_JSON_DIR) / f"{path_id}.json"
        print(f"\nProcesando ruta ({i+1}/{len(all_pathways_meta)}): {path_id} - {p_meta['name']}")


        pathway_data_to_save = {
            "_id": path_id, 
            "name": p_meta["name"],
            "organism_code": p_meta["organism_code"],
            "image_url": p_meta["image_url"],
            "kgml_data": None,
            "kegg_genes_in_pathway": []
        }
        
        print(f"Descargando KGML para {path_id}...")
        kgml_endpoint = f"get/{path_id}/kgml"
        kgml_content = fetch_kegg_data_with_retry(kgml_endpoint)
        
        if kgml_content:
            pathway_data_to_save["kgml_data"] = kgml_content
            print(f"KGML para {path_id} descargado.")
        else:
            print(f"Fallo la descarga de KGML para {path_id}.")

        
        genes_from_kegg_api = get_genes_for_pathway_from_kegg(path_id)
        if genes_from_kegg_api:
            pathway_data_to_save["kegg_genes_in_pathway"] = genes_from_kegg_api
            print(f"Se encontraron {len(genes_from_kegg_api)} genes de KEGG para la ruta {path_id}.")
        else:
           
            print(f"No se obtuvieron genes de KEGG API para la ruta {path_id} (o el endpoint no es aplicable). Los genes especificos se buscaran en el KGML si es necesario.")

        # Guardar el diccionario como un archivo JSON
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(pathway_data_to_save, f, indent=2, ensure_ascii=False)
            print(f"Datos de la ruta {path_id} guardados en {file_path}")
            successful_downloads += 1
        except IOError as e:
            print(f"Error al guardar el archivo {file_path}: {e}")
            failed_downloads += 1
        except Exception as e:
            print(f"Un error inesperado ocurrio al guardar {file_path}: {e}")
            failed_downloads += 1


    print("\n--- Proceso de descarga de datos graficos de rutas KEGG a JSON completado ---")
    print(f"Total de rutas procesadas: {len(all_pathways_meta)}")
    print(f"Archivos JSON guardados/actualizados exitosamente: {successful_downloads}")
    print(f"Archivos JSON con fallos al guardar: {failed_downloads}")

if __name__ == "__main__":
    main()