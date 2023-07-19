###########################################################################
# Script para facilitar el mapping de los datos de la base de datos       #
###########################################################################

import pandas as pd

metadatos = pd.read_excel(r'F:\Neogranadina\catalogo_colectivo\proyectos_origen\import\rsync_dir\rionegro_metadata_1.xlsx')

columnas = metadatos.columns

# save columns in a txt file
with open('map/columnas.txt', 'w') as f:
    cont = 1
    for item in columnas:
        f.write(f"{cont} : {item}\n")
        cont += 1
