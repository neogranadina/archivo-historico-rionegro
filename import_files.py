import pandas as pd
from metadatos import Metadatos
import os
import sys

colecciones = pd.read_csv("data/csv/rionegro_fondos.csv")

dtypes = {
    'título': str,
    'language': str,
    'catálogos': str,
    'descriptionstatus': str,
    'historia_de_revisión': str,
    'scriptofdescription': str
}

documentos = pd.read_csv("data/csv/rionegro_metadata.csv", dtype=dtypes)

m = Metadatos(colecciones, documentos)
t = m.prepare_data()

# create a dataframe from t with only those records where the column ca_collections.preferred_labels is not empty
nivel_carpeta = t[t['ca_collections.preferred_labels'].notna()].copy()
nivel_tomo = t[t['ca_collections.preferred_labels'].isna()].copy()

print(f"Total de registros: {len(t)}")
print(f"Registros con nivel de carpeta: {len(nivel_carpeta)}")
print(f"Registros con nivel de tomo: {len(nivel_tomo)}")

nivel_carpeta.name = "nivel_carpeta"
nivel_tomo.name = "nivel_tomo"

# path if running on Linux

if sys.platform == "linux":
    sync_dir = os.path.join("/media/jairomelo/141R0M310/Neogranadina/catalogo_colectivo/proyectos_origen/import/rsync_dir")
elif sys.platform == "win32":
    sync_dir = os.path.join("F:/Neogranadina/catalogo_colectivo/proyectos_origen/import/rsync_dir")

os.makedirs(sync_dir, exist_ok=True)

# delete all xlsx files in sync_dir
for file in os.listdir(sync_dir):
    if file.endswith(".xlsx"):
        os.remove(os.path.join(sync_dir, file))

# break nivel_carpeta and nivel_tomo dataframes in dataframes of 5000 rows each and save them as Excel files
for df in [nivel_carpeta, nivel_tomo]:
    secuencia = 1
    for i in range(0, len(df), 5000):
        df[i:i+5000].to_excel(f"{sync_dir}/rionegro_metadata_{df.name}_{secuencia}.xlsx", index=False)
        secuencia += 1
