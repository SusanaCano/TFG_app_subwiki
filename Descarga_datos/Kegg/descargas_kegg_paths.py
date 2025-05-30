'''
Resumen:
Este script procesa archivos JSON descargados con datos de KEGG, extrae información sobre
rutas metabólicas de las entradas de *Bacillus cereus*, y guarda los resultados 
en archivos JSON estructurados por bloques.

Pasos del script:
1. **Configuración de carpetas**:
   - Se define una carpeta de entrada (`descargas_kegg_json`) donde están los archivos 
   descargados y una carpeta de salida (`descargas_rutas_kegg_json`) donde se guardarán 
   los resultados.

2. **Función `extraer_info_pathways`**:
   - Extrae información relevante sobre rutas metabólicas a partir del campo `raw_text` 
   de cada entrada.
   - Para cada ruta encontrada, se guarda el ID de la ruta y su nombre.

3. **Función `procesar_archivos_kegg`**:
   - Recorre los archivos JSON en la carpeta de entrada, cargando y procesando cada uno.
   - Si el archivo contiene datos válidos en formato lista, extrae las rutas metabólicas
   y las almacena en un acumulador.
   - Una vez que el acumulador alcanza el tamaño de `bloque_size` (500 entradas), 
   se guarda en un archivo JSON en la carpeta de salida.
   - Finalmente, guarda cualquier entrada restante que no haya alcanzado el tamaño
   de bloque.

4. **Ejecución del script**:
   - Al ejecutarse el script, comienza el procesamiento de los archivos en la carpeta 
   de entrada y genera archivos de salida con las rutas metabólicas extraídas.
'''


import os
import json
import re
from pathlib import Path

# Configuración
carpeta_entrada = "descargas_kegg_json"  # Carpeta donde estarán los archivos descargados
carpeta_salida = "descargas_rutas_kegg_json"  # Carpeta donde se guardarán los archivos de rutas
batch_size = 10  # Número de entradas por descarga
bloque_size = 500  # Número de entradas por archivo JSON

# Crear carpeta de salida si no existe
Path(carpeta_salida).mkdir(parents=True, exist_ok=True)

def extraer_info_pathways(raw_text):
    entry = None
    name = None
    pathways = []

    lines = raw_text.split("\n")
    current_key = None

    for line in lines:
        if not line.strip():
            continue

        if re.match(r"^[A-Z]", line[:12]):
            current_key = line[:12].strip()
            content = line[12:].strip()
        else:
            content = line.strip()

        # Depuración: mostrar líneas que estamos procesando
        print(f"Procesando línea: {line}")

        if current_key == "ENTRY":
            entry = content.split()[0]
        elif current_key == "NAME":
            name = content
        elif current_key == "PATHWAY":
            # Ajuste para capturar las rutas en el formato correcto
            match = re.match(r"^(bce\d{5})\s+(.*)$", content)
            if match:
                pathways.append({
                    "pathway_id": match.group(1),  # ID de la ruta (por ejemplo, bce03010)
                    "pathway_name": match.group(2)  # Nombre de la ruta (por ejemplo, Ribosome)
                })

    # Depuración: Mostrar las rutas extraídas
    print(f"Rutas encontradas: {pathways}")

    return {
        "entry": entry,
        "name": name,
        "pathways": pathways
    }

def procesar_archivos_kegg(carpeta):
    total_guardados = 0
    acumulador = []
    bloques_guardados = 0

    # Verificamos que la carpeta de entrada tenga archivos
    archivos = sorted(os.listdir(carpeta))
    if not archivos:
        print("No se encontraron archivos en la carpeta de entrada.")
        return

    for archivo in archivos:
        if archivo.endswith(".json"):
            print(f"Procesando archivo: {archivo}")
            ruta_entrada = os.path.join(carpeta, archivo)
            with open(ruta_entrada, "r") as f:
                try:
                    datos = json.load(f)
                    if not isinstance(datos, list):  # Verificar si el contenido es una lista
                        print(f"El archivo {archivo} no tiene el formato esperado (debe ser una lista de entradas).")
                        continue

                    for item in datos:
                        raw_text = item.get("raw_text", "")
                        if raw_text:  # Si hay raw_text, procesar
                            doc = extraer_info_pathways(raw_text)
                            if doc["pathways"]:  # Solo guardar si tiene rutas
                                acumulador.append(doc)

                    # Si se ha alcanzado el número de entradas en bloque, guardar archivo
                    if len(acumulador) >= bloque_size:
                        bloques_guardados += 1
                        nombre_salida = f"rutas_bloque_{bloques_guardados:04d}.json"
                        ruta_salida = os.path.join(carpeta_salida, nombre_salida)
                        with open(ruta_salida, "w") as out_file:
                            json.dump(acumulador[:bloque_size], out_file, indent=2)
                        print(f" Guardado archivo {nombre_salida} con {bloque_size} entradas.")
                        acumulador = acumulador[bloque_size:]  # Reiniciar acumulador

                except json.JSONDecodeError:
                    print(f"Error al procesar el archivo {archivo}. No es un archivo JSON válido.")

    # Guardar lo que quede en el acumulador
    if acumulador:
        bloques_guardados += 1
        nombre_salida = f"rutas_bloque_{bloques_guardados:04d}.json"
        ruta_salida = os.path.join(carpeta_salida, nombre_salida)
        with open(ruta_salida, "w") as out_file:
            json.dump(acumulador, out_file, indent=2)
        print(f"Guardado final archivo {nombre_salida} con {len(acumulador)} entradas.")

    if bloques_guardados == 0:
        print("No se encontraron rutas metabólicas válidas en los archivos.")
    else:
        print(f"Total de archivos guardados: {bloques_guardados}")

if __name__ == "__main__":
    procesar_archivos_kegg(carpeta_entrada)
