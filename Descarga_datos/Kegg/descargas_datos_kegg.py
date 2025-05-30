'''
Script para descargar entradas de la base de datos KEGG.

Este script obtiene todos los identificadores KEGG de un organismo específico ('Bacillus cereus' con el código "bce"),
y descarga las entradas correspondientes en bloques. Los datos se guardan en archivos `.json` de tamaño configurable (por defecto, 500 entradas por archivo).

Características:
- Obtiene todos los IDs válidos del organismo desde la API de KEGG.
- Descarga las entradas en lotes pequeños (por defecto, 10 por petición) para evitar errores de red.
- Agrupa las entradas descargadas en bloques de tamaño configurable (por defecto, 500) y las guarda como JSON.
- Añade un breve retardo entre peticiones para evitar saturar el servidor de KEGG.
- Registra los errores HTTP en un archivo `descarga.log` dentro de la carpeta de salida.

'''

import os
import time
import requests
import json
from pathlib import Path

def obtener_ids_kegg(organismo="bce"):
    """Obtiene todos los IDs KEGG para un organismo dado."""
    url = f"http://rest.kegg.jp/list/{organismo}"
    response = requests.get(url)
    response.raise_for_status()
    lines = response.text.strip().split("\n")
    ids = [line.split()[0] for line in lines]
    return ids

def descargar_entradas_kegg(ids, output_dir, batch_size=10, bloque_size=500, delay=2.0):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    log_path = os.path.join(output_dir, "descarga.log")
    total = 0
    bloques_guardados = 0
    acumulador = []

    for i in range(0, len(ids), batch_size):
        batch = ids[i:i + batch_size]
        ids_str = "+".join(batch)
        url = f"http://rest.kegg.jp/get/{ids_str}"
        response = requests.get(url)
        
        if response.status_code != 200:
            error_msg = f"Error en el bloque HTTP ({i//batch_size + 1}): {response.status_code}\n"
            print(error_msg.strip())
            with open(log_path, "a") as log_file:
                log_file.write(error_msg)
            continue

        bloque_texto = response.text.strip()
        entradas = bloque_texto.split("///\n")
        nuevas_entradas = []

        for entrada in entradas:
            if entrada.strip():
                nuevas_entradas.append({"raw_text": entrada.strip() + "\n///"})

        acumulador.extend(nuevas_entradas)
        total += len(nuevas_entradas)
        print(f"Añadidas {len(nuevas_entradas)} entradas (Total acumuladas: {len(acumulador)})")

        if len(acumulador) >= bloque_size:
            bloques_guardados += 1
            filename = os.path.join(output_dir, f"bloque_{bloques_guardados:04d}.json")
            with open(filename, "w") as f:
                json.dump(acumulador[:bloque_size], f, indent=2)
            print(f"Guardado: {filename} con {bloque_size} entradas.")
            acumulador = acumulador[bloque_size:]

        time.sleep(delay)

    # Guardar lo que quede acumulado al final
    if acumulador:
        bloques_guardados += 1
        filename = os.path.join(output_dir, f"bloque_{bloques_guardados:04d}.json")
        with open(filename, "w") as f:
            json.dump(acumulador, f, indent=2)
        print(f"Guardado final: {filename} con {len(acumulador)} entradas.")

    print("Descarga completada.")
    print(f"Archivos guardados: {bloques_guardados}")
    print(f"Total de entradas KEGG descargadas: {total}")

if __name__ == "__main__":
    organism_code = "bce"  # Bacillus cereus
    carpeta_descargas = "descargas_kegg_json"
    
    print("Obteniendo lista de IDs de KEGG...")
    ids = obtener_ids_kegg(organism_code)
    print(f"Total de IDs obtenidos: {len(ids)}")

    print(f"Comenzando la descarga en bloques de 10 entradas...")
    descargar_entradas_kegg(ids, carpeta_descargas, batch_size=10)
