# backend/consultas/consulta_uniprot_tabla.py

"""
Este módulo proporciona la lógica para consultar la colección 'UniProt' en MongoDB.
Su función principal, `obtener_resultados_tabla`, está diseñada para:

1.  Recibir un término de búsqueda (`query`).
2.  Validar que el término de búsqueda no esté vacío.
3.  Construir una consulta para MongoDB que busca coincidencias (insensibles a
    mayúsculas/minúsculas) en los campos:
    - `primaryAccession`
    - `_id` (si el `query` parece un ObjectId válido)
    - `genes.orderedLocusNames.value`
    - `sequence.value`
4.  Ejecutar la consulta contra la colección 'UniProt', limitando la recuperación
    inicial de documentos desde la base de datos a un máximo (actualmente 10 documentos
    debido a `to_list(length=10)`).
5.  Proyectar y seleccionar campos específicos de los documentos para optimizar
    la transferencia de datos.
6.  Mapear los documentos recuperados de MongoDB a una lista de objetos
    Pydantic `QueryResponse`. Este proceso incluye la extracción y estructuración
    de datos anidados como `proteinDescription`, `genes` y `sequence`.
7.  Manejar errores, incluyendo:
    - `ValueError` (convertido a `HTTPException` 400) si el `query` es inválido.
    - `HTTPException` 404 si no se encuentran documentos o si, tras el
      procesamiento, la lista de resultados está vacía.
    - `HTTPException` 500 para errores internos inesperados.
8.  Registrar información detallada y errores durante el proceso mediante `logging`.

La función devuelve una `List[QueryResponse]` o lanza una `HTTPException`.
"""

from bson import ObjectId
from app.config.db import db 
from app.models.models_data_mongo import QueryResponse, Gene, Sequence 
from typing import List, Optional
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

async def obtener_resultados_tabla(query: str) -> List[QueryResponse]:
    """
    Realiza una búsqueda en la colección UniProt para la tabla de resultados.
    Busca en primaryAccession, _id, genes (orderedLocusNames.value y geneName), y sequence.value.
    Devuelve una lista de objetos QueryResponse o lanza HTTPException.
    """
    logger.info(f"ConsultaTabla: Iniciando obtener_resultados_tabla con query='{query}'")

    try:
                
        # Validación de la query de entrada
        if not isinstance(query, str) or not query.strip():
            logger.warning(f"ConsultaTabla: Query inválida (vacía o no es string): '{query}'")
            raise ValueError("El término de búsqueda no puede ser vacío.")

        collection = db['UniProt']
        # Intento de conversión a ObjectId 
        query_object_id = None
        if len(query) == 24 and all(c in '0123456789abcdefABCDEF' for c in query):
            try:
                query_object_id = ObjectId(query)
                logger.info(f"ConsultaTabla: Query convertida a ObjectId: {query_object_id}")
            except Exception:
                logger.debug(f"ConsultaTabla: '{query}' parecía ObjectId pero falló la conversión.")
                query_object_id = None
        
        # Construcción de la Query MongoDB
        mongo_query_conditions = [
            {"primaryAccession": {"$regex": query, "$options": "i"}},
            {"genes.orderedLocusNames.value": {"$regex": query, "$options": "i"}}, 
            {"sequence.value": {"$regex": query, "$options": "i"}}
        ]
        
        
        if query_object_id:
            mongo_query_conditions.append({"_id": query_object_id})

        query_dict = {"$or": mongo_query_conditions}
        logger.info(f"ConsultaTabla: Query MongoDB a ejecutar: {query_dict}")

        # Proyección (campos a devolver)
        projection = {
            "_id": 0, 
            "primaryAccession": 1,
            "proteinDescription.submissionNames.fullName.value": 1,
            "proteinDescription.recommendedName.fullName.value": 1,
            "genes.orderedLocusNames": 1, 
            # "genes.geneName": 1, 
            "sequence.value": 1,
            "sequence.length": 1,
            "sequence.molWeight": 1,
            "sequence.crc64": 1,
            "sequence.md5": 1
        }

        logger.debug(f"ConsultaTabla: Proyección MongoDB: {projection}")

    
        resultados_cursor = collection.find(query_dict, projection)
        
        # Ejecutar la consulta
        
        documentos = await resultados_cursor.to_list(length=10)  
        logger.info(f"ConsultaTabla: MongoDB devolvió {len(documentos)} documentos crudos para query='{query}'.")

        # Manejar caso de no documentos encontrados por MongoDB
        
        if not documentos:
            logger.warning(f"ConsultaTabla: No se encontraron documentos en MongoDB para query='{query}'. Lanzando 404.")
            raise HTTPException(status_code=404, detail="No se encontraron datos que coincidan con la consulta.")
        
       
        # Procesar documentos y convertir a objetos QueryResponse
        resultados: List[QueryResponse] = []
        for doc_idx, doc in enumerate(documentos):
            logger.debug(f"ConsultaTabla: Procesando documento {doc_idx + 1}/{len(documentos)}: {doc.get('primaryAccession', 'N/A')}")
            
            # Procesamiento de Genes
            genes_list: List[Gene] = []
            raw_genes_data = doc.get("genes", [])
            if isinstance(raw_genes_data, list):
                for gene_data in raw_genes_data:
                    if isinstance(gene_data, dict):
                        gene_name_val = gene_data.get("geneName", "") 
                        
                        ordered_locus_name_str = ""
                        raw_locus_names_list = gene_data.get("orderedLocusNames")
                        if isinstance(raw_locus_names_list, list) and raw_locus_names_list:
                            first_locus_item = raw_locus_names_list[0] 
                            if isinstance(first_locus_item, dict):
                                ordered_locus_name_str = first_locus_item.get("value", "")
                        elif isinstance(raw_locus_names_list, str): 
                            ordered_locus_name_str = raw_locus_names_list
                        
                        genes_list.append(Gene(
                            geneName=gene_name_val,
                            orderedLocusNames=ordered_locus_name_str
                        ))
                        
            # Procesamiento de ProteinDescription
            proteinDescription_str: Optional[str] = None 
            raw_protein_desc_data = doc.get("proteinDescription", {})
            if isinstance(raw_protein_desc_data, dict):
                submission_names_list = raw_protein_desc_data.get("submissionNames", [])
                if submission_names_list and isinstance(submission_names_list[0], dict):
                    full_name_data = submission_names_list[0].get("fullName", {})
                    protein_desc_val_from_db = full_name_data.get("value")
                    proteinDescription_str = protein_desc_val_from_db

                if proteinDescription_str is None: 
                    recommended_name_obj = raw_protein_desc_data.get("recommendedName", {})
                    if isinstance(recommended_name_obj, dict):
                        full_name_data_rec = recommended_name_obj.get("fullName", {})
                        if isinstance(full_name_data_rec, dict):
                            proteinDescription_str = full_name_data_rec.get("value")
            
            # Procesamiento de Sequence
            raw_sequence_data = doc.get("sequence", {})
            sequence_obj = Sequence(
                value=raw_sequence_data.get("value", ""),
                length=raw_sequence_data.get("length", 0),
                molWeight=raw_sequence_data.get("molWeight"),
                crc64=raw_sequence_data.get("crc64"),       
                md5=raw_sequence_data.get("md5")          
            )            
    

            # Crear el objeto QueryResponse
            try:
                resultado_obj = QueryResponse(
                    primaryAccession=doc.get("primaryAccession"), 
                    proteinDescription=proteinDescription_str,
                    genes=genes_list,
                    sequence=sequence_obj
                )
                resultados.append(resultado_obj)
            except Exception as pydantic_exc: 
                logger.error(f"ConsultaTabla: Error al crear QueryResponse para doc {doc.get('primaryAccession', 'N/A')}: {pydantic_exc}. Documento parcial: {str(doc)[:200]}", exc_info=True)
                
        # Manejar caso de no resultados después del procesamiento
        if not resultados:
            logger.warning(f"ConsultaTabla: 'resultados_convertidos' está vacío para query='{query}' (después de procesar {len(documentos)} docs). Lanzando 404.")
            raise HTTPException(status_code=404, detail="Los datos encontrados no pudieron ser procesados o no cumplen los criterios.")
            
        logger.info(f"ConsultaTabla: Devolviendo {len(resultados)} resultados procesados para query='{query}'.")
        return resultados
    
    # Manejo de Excepciones 
    except ValueError as ve: # Para la validación inicial de 'query'
        logger.error(f"ConsultaTabla: ValueError para query='{query}': {str(ve)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(ve))
    except HTTPException: 
        raise
    except Exception as e: # Para cualquier error inesperado
        logger.error(f"ConsultaTabla: Error general inesperado para query='{query}': {type(e).__name__} - {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Ocurrió un error interno al procesar su solicitud.")