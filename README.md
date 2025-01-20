# Proyecto de Descarga de Datos de UniProt

Este proyecto permite realizar consultas a la API de UniProt para descargar información sobre proteínas de organismos específicos. Los datos obtenidos se guardan en archivos JSON en una carpeta local llamada `descargas`. Además, se proporciona la funcionalidad para consultar el número total de entradas disponibles en UniProt para una consulta dada.

## Funcionalidades

1. **Consulta de proteínas validadas (reviewed)**: Puedes realizar búsquedas para obtener información sobre proteínas revisadas asociadas a un organismo específico (por ejemplo, *Homo sapiens*).
   
2. **Descarga de datos en bloques**: Los datos se descargan en bloques para optimizar el uso de la memoria y permitir la descarga de grandes cantidades de información.

3. **Almacenamiento local**: Los datos descargados se almacenan en archivos JSON dentro de la carpeta `descargas`.

4. **Consulta del número total de entradas**: Puedes consultar cuántas entradas en total existen en UniProt para una consulta específica.

## Requisitos

- Python 3.x
- Bibliotecas Python: `requests`, `json`, `time`, `os`

## Instalación

### Clonar el repositorio

```bash
git clone https://github.com/tu_usuario/tu_repositorio.git
