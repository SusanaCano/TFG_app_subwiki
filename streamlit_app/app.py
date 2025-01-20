import streamlit as st
from pymongo import MongoClient
import pandas as pd

# Configuración de conexión a MongoDB Atlas
MONGO_URI = "mongodb+srv://susanacm7:PM1OGO1MzCYyoEFM@buscarGenes.jjl4x.mongodb.net/BacillusCereus?retryWrites=true&w=majority"
DATABASE_NAME = "BacillusCereus"
COLLECTION_NAME = "buscarGenes"

def get_genes():
    """Consulta MongoDB Atlas para obtener los nombres de genes que comienzan con 'BC_'."""
    # Conexión a MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    # Consulta para buscar genes con el patrón BC_xxxx
    regex_filter = {"gene_name": {"$regex": r"^BC_\d{4}$"}}
    result = collection.find(regex_filter, {"_id": 0, "gene_name": 1})

    # Convertir a lista
    genes = list(result)
    client.close()
    return genes

# Streamlit App
st.title("Consulta de Genes BC_xxxx")
st.write("Esta aplicación muestra los nombres de los genes que comienzan con 'BC_'.")

# Obtener datos de la base de datos
genes = get_genes()

if genes:
    # Convertir a DataFrame para mostrar con Streamlit
    df = pd.DataFrame(genes)
    st.write("Genes encontrados:")
    st.dataframe(df)
else:
    st.warning("No se encontraron genes que coincidan con el patrón.")
