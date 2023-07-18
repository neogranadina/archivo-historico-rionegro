import pandas as pd
from metadatos import Metadatos
import os

colecciones = pd.read_csv("data/rionegro_fondos.csv")

dtypes = {
    'título': str,
    'language': str,
    'catálogos': str,
    'descriptionstatus': str,
    'historia_de_revisión': str,
    'scriptofdescription': str
}

documentos = pd.read_csv("data/rionegro_metadata.csv", dtype=dtypes)

m = Metadatos(colecciones, documentos)
t = m.prepare_data()

sync_dir = os.path.join("/media/jairomelo/141R0M310/Neogranadina/catalogo_colectivo/proyectos_origen/import/rsync_dir")

os.makedirs(sync_dir, exist_ok=True)

# break t dataframe in dataframes of 5000 rows each and save them as Excel files
secuencia = 1
for i in range(0, len(t), 5000):
    t[i:i+5000].to_excel(f"{sync_dir}/rionegro_metadata_{secuencia}.xlsx", index=False)
    secuencia += 1
