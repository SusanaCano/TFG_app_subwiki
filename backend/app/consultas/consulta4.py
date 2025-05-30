# backend/app/consultas/consulta4.py

'''
    Realiza una búsqueda asíncrona en la colección 'UniProt' de MongoDB
    basándose en un término de consulta proporcionado.

    La función construye una consulta compleja que busca el término `query`
    de forma insensible a mayúsculas y minúsculas en los siguientes campos:
    - `_id` (si `query` es un ObjectId válido)
    - `primaryAccession`
    - `genes.orderedLocusNames.value` (dentro de un array de nombres de locus ordenados)
    - `genes.geneName`
    - `sequence.value`

    Proyecta campos específicos para optimizar la transferencia de datos y luego
    mapea los documentos encontrados a una lista de objetos `QueryResponse`.
    La función actualmente limita los resultados a los primeros 10 documentos.

    Utiliza logging para registrar la consulta generada, el número de documentos
    encontrados, los documentos individuales y cualquier error que ocurra.

    Args:
        query (str): El término de búsqueda a utilizar. Debe ser una cadena no vacía.

    Returns:
        List[QueryResponse]: Una lista de objetos QueryResponse que coinciden con
                             la consulta. Cada objeto contiene la descripción de la
                             proteína, información de genes y la secuencia.

    Raises:
        ValueError: Si el `query` proporcionado no es una cadena o es una cadena vacía.
        HTTPException (404): Si no se encuentran resultados que coincidan con la consulta.
        HTTPException (500): Si ocurre un error inesperado durante la consulta a la
                             base de datos o el procesamiento de los datos.
'''

from bson import ObjectId
from app.config.db import db
from app.models.models_data_mongo import QueryResponse, Gene, Sequence
from typing import List
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

async def obtener_resultados(query: str) -> List[QueryResponse]:

    try:
        # Asegurarnos de que query sea una cadena
        if not isinstance(query, str) or not query.strip():
            raise ValueError("El valor de la consulta debe ser una cadena no vacía.")

        collection = db['UniProt']
     
        # Convertir el _id a ObjectId si es un valor válido
        query_object_id = None
        try:
            query_object_id = ObjectId(query)
        except Exception:
            
            pass

        # Construir el query_dict con condiciones OR
        query_dict = {
            "$or": [
                # Buscar por _id si es un ObjectId válido
                {"_id": query_object_id} if query_object_id else None,
                {"primaryAccession": {"$regex": query, "$options": "i"}},
                {"genes": {
                    "$elemMatch": {
                        "orderedLocusNames": {
                            "$elemMatch": {
                                "value": {"$regex": query, "$options": "i"}
                            }
                        }
                    }
                }},
                {"genes.geneName": {"$regex": query, "$options": "i"}},
                {"sequence.value": {"$regex": query, "$options": "i"}}
            ]
        }

        # Eliminar valores None de query_dict (por si no se genera alguna de las condiciones)
        query_dict["$or"] = [cond for cond in query_dict["$or"] if cond is not None]

        # LOG: Mostrar la consulta generada
        logger.info("Consulta generada: %s", query_dict)

        # Ejecutar la consulta y traer los primeros 10 resultados
        resultados_cursor = db['UniProt'].find(query_dict, {
                        "proteinDescription.submissionNames.fullName.value": 1,
            "genes.geneName": 1,
            "genes.orderedLocusNames.value": 1,
            "sequence.value": 1,
            "sequence.length": 1
        })
        
        documentos = await resultados_cursor.to_list(length=10)  # Limitar los resultados a 10 para depuración

        # LOG: Mostrar el número de documentos encontrados
        logger.info("Número de documentos encontrados: %d", len(documentos))

        if len(documentos) == 0:
            logger.warning("No se encontraron documentos que coincidan con la consulta.")
        else:
            for doc in documentos:
                logger.info("Documento encontrado: %s", doc)

        # Procesa los resultados 
        resultados = []
        for doc in documentos:
            genes = []
            for gene in doc.get("genes", []):
                if isinstance(gene, dict):
                    for orderedLocus in gene.get("orderedLocusNames", []):
                        if isinstance(orderedLocus, dict):
                            value = orderedLocus.get("value", "")
                            if isinstance(value, str):
                                genes.append(Gene(
                                geneName=gene.get("geneName", ""),
                                orderedLocusNames=orderedLocus.get("value", "")  # Obtenemos el valor de orderedLocusName
                        ))
            # Procesar el campo 'sequence' 
            sequence_data = doc.get("sequence", {})
            # Imprimir tipo de sequence_data para depuración
            print(f"Tipo de sequence_data: {type(sequence_data)}")
            # Asegurarse de que sequence_data sea un diccionario antes de acceder a sus claves
            if isinstance(sequence_data, dict):
                sequence = Sequence(
                    value=sequence_data.get("value", ""),
                    length=sequence_data.get("length", 0),
                    molWeight=sequence_data.get("molWeight", 0),
                    crc64=sequence_data.get("crc64"),
                    md5=sequence_data.get("md5")
                )            
            else:
            # Manejo del caso en que sequence no es un diccionario 
                sequence = Sequence(
                value="",
                length=0,
                molWeight=0,
                crc64=None,
                md5=None
            )
    
             # Asegurar de que proteinDescription es un diccionario adecuado
            protein_description_data = doc.get("proteinDescription", {})
            submission_names = protein_description_data.get("submissionNames", [])

            # Asegurar que haya al menos un elemento en 'submissionNames' y que 'fullName' y 'value' estén presentes
            if submission_names and isinstance(submission_names[0], dict):
                full_name_data = submission_names[0].get("fullName", {})
                proteinDescription = full_name_data.get("value", "")
            else:
                proteinDescription = ""
                   
            resultado = QueryResponse(
                proteinDescription=proteinDescription,
                genes=genes,
                
                sequence=sequence
                #sequence=doc.get("sequence", {}).get("value", ""),
                #sequenceLength=doc.get("sequence", {}).get("length", 0)  # Añadimos la longitud de la secuencia
            )
            resultados.append(resultado)

            # Si no hay resultados, lanzar la excepción
        if not resultados:
            raise HTTPException(status_code=404, detail="No se encontraron resultados")
    
        return resultados

    except Exception as e:
        # LOG: Captura y muestra cualquier error
        logger.error("Error en la consulta: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Error en la consulta: {str(e)}")

