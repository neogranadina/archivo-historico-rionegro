######################################################################
# Crea la estructura de metadatos para crear las colecciones que     #
# contienen los documentos de archivo                                #
######################################################################

import pandas as pd
import numpy as np


class Coleccion:
    def __init__(self, dfcolecciones):
        self.cols = dfcolecciones

    def collection_tree(self) -> pd.DataFrame:
        """
        Crear un árbol de colecciones y subcolecciones a partir de los datos de entrada
        del dataframe self.cols

        Estructura:

        institucion
            - fondo
                - tomo
                - caja
                    - carpeta

        :return: pd.DataFrame con la estructura de colecciones
        """
        data_colecciones = self.cols[['unidad_documental_compuesta', 'identificador', 'título', 'nivel_de_descripción']].copy()

        # replace value in column 'nivel_de_descripción' from Carpeta to Caja where título contains 'Caja'
        data_colecciones.loc[data_colecciones['título'].str.contains('Caja'), 'nivel_de_descripción'] = 'Caja'

        # segmentamos el dataframe en instituciones, fondos, subfondos y series
        instituciones = data_colecciones.loc[data_colecciones['nivel_de_descripción'].isna()]
        fondos = data_colecciones.loc[data_colecciones['nivel_de_descripción'] == 'Fondo'].copy()
        subfondos = data_colecciones.loc[data_colecciones['nivel_de_descripción'].isin(['Tomo', 'Caja'])].copy()
        series = data_colecciones.loc[data_colecciones['nivel_de_descripción'] == 'Carpeta'].copy()

        # encontrar el padre de cada fondo y hacer un merge
        fondos['institucion_nombre'] = fondos['unidad_documental_compuesta'].str.split(',').str[0].str.strip()
        fondos['institucion_id'] = fondos['institucion_nombre'].map(instituciones.set_index('unidad_documental_compuesta')['identificador'])
        fondos = fondos.rename(columns={'título': 'fondo_nombre', 'identificador': 'fondo_id'})[['institucion_id', 'institucion_nombre', 'fondo_id', 'fondo_nombre']].reset_index(drop=True)
        fondos['fondo_nombre'] = fondos['fondo_nombre'].str.split().str[-1]

        # encontrar el padre de cada subfondo y hacer un merge
        subfondos['fondo_nombre'] = subfondos['unidad_documental_compuesta'].str.split(',').str[1].str.strip()
        subfondos = subfondos.merge(fondos, on='fondo_nombre', how='left')
        subfondos = subfondos.rename(columns={'título': 'subfondo_nombre', 'identificador': 'subfondo_id', 'nivel_de_descripción': 'subfondo_tipo', 'unidad_documental_compuesta': 'ruta_subfondo'})[['institucion_id', 'institucion_nombre', 'fondo_id', 'fondo_nombre', 'subfondo_id', 'subfondo_nombre', 'subfondo_tipo', 'ruta_subfondo']].reset_index(drop=True)

        # remove punctuation from column 'subfondo_nombre
        subfondos['subfondo_nombre'] = subfondos['subfondo_nombre'].str.replace(r'[^\w\s]', '', regex=True).str.strip()

        # encontrar el padre de cada serie y hacer un merge
        series['unidad_documental_compuesta'] = series['unidad_documental_compuesta'].str.replace('Caja 0269', 'Caja 269').str.replace('Caja 0081', 'Caja 081').str.replace('Caja 0054', 'Caja 054') # <- corregir errores puntuales de digitación
        series['subfondo_nombre'] = series['unidad_documental_compuesta'].str.split(',').str[2].str.strip()
        series = series.merge(subfondos, on='subfondo_nombre', how='left')
        series = series.rename(columns={'título': 'serie_nombre', 'identificador': 'serie_id', 'unidad_documental_compuesta':'ruta_serie'})[['institucion_id', 'institucion_nombre', 'fondo_id', 'fondo_nombre', 'subfondo_id', 'subfondo_nombre', 'subfondo_tipo', 'ruta_subfondo', 'serie_id', 'serie_nombre', 'ruta_serie']].reset_index(drop=True)

        # crear el identificador de la unidad documental compuesta
        series['unidad_documental_compuesta'] = (
            'CO.' + series['institucion_id'].astype(str) + '.' + series['fondo_id'].astype(str) +
            '.T' + series['subfondo_id'].astype(str).replace(r'\D', '', regex=True) +
            '.T' + series['serie_id'].astype(str).replace(r'\D', '', regex=True)
        )

        subfondos['unidad_documental_compuesta'] = (
            'CO.' + subfondos['institucion_id'].astype(str) + '.' + subfondos['fondo_id'].astype(str) +
            '.T' + subfondos['subfondo_id'].astype(str).replace(r'\D', '', regex=True)
        )

        colecciones = pd.concat([series, subfondos], ignore_index=True)

        return colecciones


    def build_collection_df(self) -> pd.DataFrame:
        """
        merge tree and collection dataframes
        """
        collection_df = self.cols
        collection_df = collection_df.rename(columns={'unidad_documental_compuesta': 'ruta'})
        collection_df = collection_df.drop(columns=['identificador', 'nivel_de_descripción', 'título'])

        collection_df['alcance_y_contenido'] = collection_df['alcance_y_contenido'].str.replace(r'\n', ' ', regex=True)

        tree = self.collection_tree()

        # merge tree['ruta_subfondo'] and collection['ruta'] dataframes
        colleccion_subfondo = pd.merge(tree, collection_df, left_on='ruta_subfondo', right_on='ruta', how='left')

        # merge tree['ruta_serie'] and collection['ruta'] dataframes
        colleccion_serie = pd.merge(tree, collection_df, left_on='ruta_serie', right_on='ruta', how='left')

        # concatenate the two merges while avoiding duplicities
        merged_df = pd.concat([colleccion_subfondo, colleccion_serie.drop(columns=colleccion_subfondo.columns)], axis=1)

        return merged_df

    def prepare_collections(self) -> pd.DataFrame:
        """
        Change column names, drop some columns, create date ranges, and number of folios
        """

        collect_df = self.build_collection_df()
        
        # drop columns that are not needed because they are redundant or not useful
        todrop = ['institucion_id', 'secuencia', 'ruta', 'folio_inicial_del_documento', 'punto_de_acceso', 'lugar', 'descriptionidentifier', 'physicalobjectname', 'physicalobjectlocation', 'serie_id']

        # columns to rename
        columns = {
            "institucion_nombre": "ca_collections.preferred_labels_institucion", 
            "fondo_id": "ca_collections.idno_fondo", 
            "fondo_nombre": "ca_collections.preferred_labels_fondo", 
            "subfondo_id": "ca_collections.idno_subfondo", 
            "subfondo_nombre": "ca_collections.preferred_labels_subfondo", 
            "subfondo_tipo": "collection_type_subfondo", 
            "ruta_subfondo": "ca_collections.arrangement_subfondo", 
            "serie_nombre": "ca_collections.preferred_labels", 
            "ruta_serie": "ca_collections.arrangement", 
            "unidad_documental_compuesta": "ca_collections.idno", 
            "medio_y_extensión": "ca_collections.extent_text", 
            "folio_final_del_documento": "folio_final_del_documento", 
            "repositorio": "ca_collections.repository.repositoryName", 
            "alcance_y_contenido": "ca_collections.scopecontent", 
            "condiciones_de_acceso": "ca_collections.accessrestrict", 
            "condiciones_de_reproducción": "ca_collections.reproduction", 
            "caracterísitcas_físicas": "ca_collections.note", 
            "ubicación_de_los_originales": "ca_collections.repository.repositoryLocation", 
            "nameaccesspoints": 'ca_places', 
            "tipo_de_documento": "ca_collections.description", 
            "institutionidentifier": "ca_collections.idno_institucion", 
            "fuentes": "ca_collections.relatedmaterial", 
            "fecha_inicial": "fecha_inicial", 
            "fecha_final": "fecha_final",
        }

        # drop columns
        collect_df = collect_df.drop(columns=todrop)
       
        # rename columns
        collect_df = collect_df.rename(columns=columns)

        # create idnos
        collect_df['ca_collections.idno_fondo'] = collect_df['ca_collections.idno'].str.split('.').str[:3].str.join('.')
        collect_df['ca_collections.idno_subfondo'] = collect_df['ca_collections.idno'].str.split('.').str[:4].str.join('.')

        # change collection_type_subfondo to match with vocabulary ('tomos' and 'caja')
        collect_df['collection_type_subfondo'] = collect_df['collection_type_subfondo'].str.replace('Tomo', 'tomos', regex=True).str.replace('Caja', 'caja', regex=True)

        # populate "ca_collections.extent_text" with the number of folios (extract value from "folio_final_del_documento")
        collect_df['ca_collections.extent_text'] = collect_df['folio_final_del_documento'].str.extract(r'(\d+)', expand=False) + " folios"

        # create date ranges from "fecha_inicial" and "fecha_final" columns

        collect_df['ca_collections.unitdate.date_value'] = collect_df.apply(lambda x: self.get_date_range(x['fecha_inicial'], x['fecha_final']), axis=1)

        collect_df['ca_collections.unitdate.dates_types'] = 'recordKeeping'

        collect_df = collect_df.drop(columns=['fecha_inicial', 'fecha_final', 'folio_final_del_documento'])

        # rearange columns
        collect_df = collect_df[['ca_collections.idno_institucion', 'ca_collections.preferred_labels_institucion', 'ca_collections.idno_fondo', 'ca_collections.preferred_labels_fondo', 'ca_collections.idno_subfondo', 'ca_collections.preferred_labels_subfondo', 'collection_type_subfondo', 'ca_collections.arrangement_subfondo', 'ca_collections.preferred_labels', 'ca_collections.arrangement', 'ca_collections.idno', 'ca_collections.extent_text', 'ca_collections.repository.repositoryName', 'ca_collections.scopecontent', 'ca_collections.accessrestrict', 'ca_collections.reproduction', 'ca_collections.note', 'ca_collections.repository.repositoryLocation', 'ca_places', 'ca_collections.description', 'ca_collections.relatedmaterial', 'ca_collections.unitdate.date_value', 'ca_collections.unitdate.dates_types']]

        # final clean: drop duplicates
        collect_df = collect_df.drop_duplicates()

        return collect_df

    def get_date_range(self, f_ini, f_fin):
        """
        Crea un rango de años de tipo (AAAA - AAAA)
        validando que el año final sea mayor que el inicial
        """

        if f_ini is np.nan or f_fin is np.nan:
            return np.nan

        f_ini = f_ini.split('-')[0]
        f_fin = f_fin.split('-')[0]

        if f_ini > f_fin:
            return f_fin + ' - ' + f_ini
        elif f_ini == '0000':
            return f_fin
        else:
            return f_ini + ' - ' + f_fin


if __name__ == '__main__':
    colecciones = pd.read_csv("data/csv/rionegro_fondos.csv")
    
    c = Coleccion(colecciones)
    t = c.prepare_collections()
    t.to_csv('data/csv/rionegro_collections.csv', index=False)
    # save t.columns to a file
    with open('logs/rionegro_collections_columns.txt', 'w') as f:
        for item in t.columns:
            f.write("%s\n" % item)
