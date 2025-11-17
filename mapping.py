###########################################################################
# Script para facilitar el mapping de los datos de la base de datos       #
###########################################################################

import pandas as pd
import os

default_path = os.path.join(os.getcwd(), 'output', 'rsync_dir', 'rionegro_metadata_nivel_carpeta_1.xlsx')
metadata_path = os.environ.get('METADATA_FILE', default_path)

metadatos = pd.read_excel(metadata_path)

columnas = metadatos.columns

# save columns in a txt file
with open('mappings/columnas.txt', 'w') as f:
    cont = 1
    for item in columnas:
        f.write(f"{cont} : {item}\n")
        cont += 1
