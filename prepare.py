###############################################################################
# Este script tiene como única intención convertir los archivos de Excel      #
# que contienen los datos de las colecciones y documentos de archivo en       #
# un archivo CSV que pueda ser leído por el script de conversión de datos     #
###############################################################################

import pandas as pd

colecciones = pd.read_excel("data/rionegro_fondos.xlsx")
metadatos = pd.read_excel("data/rionegro_metadata.xlsx", skiprows=1)

# remove empty columns
colecciones = colecciones.dropna(axis=1, how="all")
metadatos = metadatos.dropna(axis=1, how="all")

# rename columns that end with empty spaces
colecciones.columns = colecciones.columns.str.replace(r'\s*\(.*\)|\|.*', '', regex=True).str.strip()
metadatos.columns = metadatos.columns.str.replace(r'\s*\(.*\)|\|.*', '', regex=True).str.strip()

# remove columns
metadatos = metadatos.drop(columns=["(convertir","como","se", "abajo)"])

# rename columns to make them more readable
colecciones.columns = colecciones.columns.str.replace(" ", "_").str.lower()
metadatos.columns = metadatos.columns.str.replace(" ", "_").str.lower()

# pre-clean data
colecciones['nivel_de_descripción'] = colecciones['nivel_de_descripción'].str.strip().str.split(" ").str[0]

# Convertir los archivos de Excel en CSV
colecciones.to_csv("data/rionegro_fondos.csv", index=False)
metadatos.to_csv("data/rionegro_metadata.csv", index=False)
