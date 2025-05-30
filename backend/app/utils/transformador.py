# backend/app/services/kegg_service.py

'''
# Este módulo proporciona servicios para manejar datos de KEGG. Centraliza la lógica para:
#
# 1.  `obtener_ruta_metabolica(entry, db_motor)`:
#     - Recupera documentos de rutas metabólicas desde una colección de MongoDB
#       (presumiblemente 'kegg_rutas').
#     - Realiza una búsqueda flexible, insensible a mayúsculas/minúsculas y
#       guiones bajos, para las entradas de rutas utilizando las capacidades
#       de $expr y regex de MongoDB.
#     - Serializa el `_id` de MongoDB (ObjectId) a una cadena para facilitar
#       su consumo.
#
# 2.  `parse_kgml_to_graph(kgml_string, pathway_map_id)`:
#     - Parsea cadenas XML crudas en formato KGML (KEGG Markup Language).
#     - Transforma los datos KGML en una representación de grafo estructurada,
#       consistente en nodos (derivados de los elementos `<entry>` de KGML) y
#       aristas (derivadas de los elementos `<relation>` de KGML).
#     - Extrae atributos como ID del nodo, etiqueta, tipo, coordenadas, y
#       origen, destino y etiqueta de las aristas.
#     - Devuelve un diccionario que contiene listas de nodos, aristas y cualquier
#       error de parseo.
#
# El módulo también define estructuras `TypedDict` personalizadas (`KgmlNode`,
# `KgmlEdge`, `ParsedKgmlGraph`) para representar los componentes del grafo
# KGML parseado.
#
# En general, este servicio tiene como objetivo abstraer y proporcionar información
# procesada de rutas KEGG para su uso en otras partes de la aplicación, como
# endpoints de API o componentes de visualización de datos.
'''

from bson import ObjectId

def transformar_documento(doc):
    if '_id' in doc and isinstance(doc['_id'], ObjectId):
        doc['_id'] = str(doc['_id'])
    return doc
