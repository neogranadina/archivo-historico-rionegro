# Archivo Histórico de Rionegro

Limpieza y modelado de la información para hacer la ingesta de datos en el repositorio abcng.org

## Origen de los datos

Fondos: [2022-03-31-AHR_Procesamiento_Fondos](https://docs.google.com/spreadsheets/d/1VH7CXdSf4yzWIg5nsj7qslq8R0xZdRjl/edit?usp=sharing&ouid=100264511648583728207&rtpof=true&sd=true) v. 23/12/2022

Documentos: [rionegro_importar](https://docs.google.com/spreadsheets/d/10Gq7669jHl-nBtHqlWqpqUMOth0Ew8pL/edit?usp=sharing&ouid=100264511648583728207&rtpof=true&sd=true) v. 4/7/2023

## Metodología

1. Descargados los archivos de origen en formato `.xlsx`, se guardan en el directorio `data` con los nombres `data/xlsx/rionegro_fondos.xlsx` y `data/xlsx/rionegro_metadata.xlsx`.
2. Se ejecuta el script `prepare.py` para generar los archivos `data/csv/rionegro_fondos.csv` y `data/csv/rionegro_metadata.csv`.
3. Mediante el módulo `colecciones.py` se procesa la información de los fondos, se limpia la información, se construye la estructura de colecciones, se generan los identificadores de cada colección, se ajusta el nombre de las columnas a la estructura de Collective Access y se procesa la información relacionada con la cantidad de folios y el rango de fechas. Se genera un archivo `data/csv/rionegro_collections.csv` por seguridad y el archivo `data/csv/rionegro_collections_columns.txt` para facilitar la referencia de las columnas.
4. El script `import_files.py` genera archivos Excel divididos en lotes para importación al sistema Collective Access.
5. El script `mapping.py` facilita la revisión de las columnas de los metadatos.

## Configuración

Los scripts utilizan rutas configurables que pueden personalizarse mediante variables de entorno:

- `SYNC_DIR`: Directorio de salida para archivos de importación (por defecto: `./output/rsync_dir/`)
- `METADATA_FILE`: Archivo de metadatos para mapping (por defecto: `./output/rsync_dir/rionegro_metadata_nivel_carpeta_1.xlsx`)

## Uso

1. Ejecutar `python prepare.py` para convertir archivos Excel a CSV
2. Ejecutar `python colecciones.py` para procesar colecciones
3. Ejecutar `python import_files.py` para generar archivos de importación
4. Ejecutar `python mapping.py` para revisar estructura de columnas

