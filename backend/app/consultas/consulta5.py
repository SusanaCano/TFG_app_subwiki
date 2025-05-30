from bson import ObjectId
from app.config.db import db
from app.models.models_data_mongo import QueryResponse, Gene, Sequence
from typing import List
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

async def obtener_resultados(query: str) -> List[QueryResponse]:
    try:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("El valor de la consulta debe ser una cadena no vacía.")

        collection = db['UniProt']

        # Intentar convertir el query en ObjectId
        query_object_id = None
        try:
            query_object_id = ObjectId(query)
        except Exception:
            pass

        # Construir consulta $or
        query_dict = {
            "$or": [
                {"_id": query_object_id} if query_object_id else None,
                {"primaryAccession": {"$regex": query, "$options": "i"}},
                {"genes.orderedLocusNames.value": {"$regex": query, "$options": "i"}}
            ]
        }
        query_dict["$or"] = [q for q in query_dict["$or"] if q is not None]

        logger.info("Consulta generada: %s", query_dict)

        projection = {
            "proteinDescription.submissionNames.fullName.value": 1,
            "genes.orderedLocusNames.value": 1,
            "sequence.value": 1,
            "sequence.length": 1,
            "sequence.molWeight": 1,
            "sequence.crc64": 1,
            "sequence.md5": 1
        }

        documentos = await collection.find(query_dict, projection).to_list(length=10)
        logger.info("Documentos encontrados: %d", len(documentos))

        resultados = []

        for doc in documentos:
            # Extraer proteinDescription
            proteinDescription = ""
            try:
                submission_names = doc.get("proteinDescription", {}).get("submissionNames", [])
                if submission_names and isinstance(submission_names[0], dict):
                    proteinDescription = submission_names[0].get("fullName", {}).get("value", "")
            except Exception as e:
                logger.warning("Error extrayendo proteinDescription: %s", e)

            # Extraer genes
            genes = []
            for gene in doc.get("genes", []):
                gene_name = gene.get("geneName", "")
                for locus in gene.get("orderedLocusNames", []):
                    value = locus.get("value", "")
                    if isinstance(value, str):
                        genes.append(Gene(
                            geneName=gene_name,
                            orderedLocusNames=value
                        ))

            # Extraer sequence
            seq = doc.get("sequence", {})
            sequence = Sequence(
                value=seq.get("value", ""),
                length=seq.get("length", 0),
                molWeight=seq.get("molWeight"),
                crc64=seq.get("crc64"),
                md5=seq.get("md5")
            )

            resultados.append(QueryResponse(
                proteinDescription=proteinDescription,
                genes=genes,
                sequence=sequence
            ))

        return resultados

    except Exception as e:
        logger.error("Error en la consulta: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Error en la consulta: {str(e)}")
