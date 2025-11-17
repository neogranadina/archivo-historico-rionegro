#########################################################################
# Procesamiento de los metadatos del AHR para preparar su ingesta       #
# en el sistema de archivos de la plataforma abcng.org.                 #
#########################################################################

import re
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import calendar
import logging

# custom modules
from colecciones import Coleccion

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('logs/errores.log')
file_handler.setFormatter(formatter)
log.addHandler(file_handler)


class Metadatos:
    def __init__(self, colecciones, metadata):
        self.metadata = metadata
        self.colecciones = colecciones

    def collections_and_metadata(self) -> pd.DataFrame:
        """
        merge the collections and metadata dataframes
        """

        collections = Coleccion(self.colecciones)
        collections = collections.prepare_collections()

        metadata = self.metadata.rename(
            columns={'unidad_documental_compuesta': 'ca_collections.idno'})

        # Existe una inconsistencia entre las colecciones y los metadatos. Es necesario añadir
        # manualmente las colecciones que están en los metadatos pero no en las colecciones.

        colecciones_faltantes = pd.read_json(
            'manual/colecciones_faltantes.json')
        collections = pd.concat(
            [collections, colecciones_faltantes], ignore_index=True)
        # <- evita crear un número mayor de filas en el merge
        collections = collections.drop_duplicates(
            subset=['ca_collections.idno'], keep='last')

        # asegurar el formato de ca_collections.idno
        metadata['ca_collections.idno'] = metadata['ca_collections.idno'].str.replace(
            r"\.(\d+)", r".T\1", regex=True)

        df = pd.merge(metadata, collections,
                      on='ca_collections.idno', how='left')

        # collecctions that are not in the metadata
        sobrantes = collections.loc[~collections['ca_collections.idno'].isin(
            metadata['ca_collections.idno'])]
        sobrantes.to_csv('logs/colecciones_sobrantes.csv', index=False)

        return df

    def prepare_data(self) -> pd.DataFrame:
        """
        Ensure data consistency and prepare the data for ingestion

        """

        data = self.collections_and_metadata()

        todrop = ['secuencia', 'nivel_de_descripción', 'imagen_inicial', 'imagen_final', 'language', 'catálogos', 'lugar', 'tipo_de_documento', 'identificador_de_la_institución',
                  'descriptionstatus', 'historia_de_revisión', 'languageofdescription', 'scriptofdescription', 'notas_del_archivero', 'identificadores_alternativos']

        renombrar = {
            "identificador": "ca_objects.idno",
            "título": "ca_objects.preferred_labels",
            "medio_y_extensión": "soporte",
            "folio_inicial_del_documento": "folio_inicial",
            "folio_final_del_documento": "folio_final",
            "alcance_y_contenido": "ca_objects.description",
            "condiciones_de_acceso": "ca_objects.accessrestrict",
            "condiciones_de_reproducción": "ca_objects.reproduction",
            "caracterísitcas_físicas": "ca_objects.note",
            "ubicación_de_los_originales": "ca_objects.originalsloc",
            "punto_de_acceso": "ca_objects.arrangement",
            "fuentes": "ca_objects.otherfindingaid",
            "fecha_inicial": "fecha_inicial",
            "fecha_final": "fecha_final",
            "actores": "ca_entities_inst",
            "actores.1": "ca_entities"
        }

        data = data.drop(columns=todrop)
        data = data.rename(columns=renombrar)

        # if value in ca_objects.preferred_labels is null, replace it with the value in ca_objects.description (max 100 words)
        data['ca_objects.preferred_labels'] = data.apply(
            lambda x: x['ca_objects.description'] if pd.isnull(x['ca_objects.preferred_labels']) else x['ca_objects.preferred_labels'], axis=1)

        # replace null values in ca_objects.preferred_labels with 'sin título'
        data['ca_objects.preferred_labels'] = data['ca_objects.preferred_labels'].fillna(
            'sin título')

        # create column ca_objects.extent_text with the combined values of "soporte", "folio_inicial" and "folio_final"
        data['ca_objects.extent_text'] = 'soporte: ' + data['soporte'] + ' |' + \
            ' folios: ' + data['folio_inicial'] + ' - ' + data['folio_final']

        data = data.drop(columns=['soporte', 'folio_inicial', 'folio_final'])

        data['fecha_inicial'] = data['fecha_inicial'].str.replace(
            '\.', '-', regex=True).str.replace(r"-(\d)$", r"-0\1", regex=True)
        data['fecha_final'] = data['fecha_final'].str.replace(
            '\.', '-', regex=True).str.replace(r"-(\d)$", r"-0\1", regex=True)

        # corrección manual de fechas
        data['fecha_final'] = data['fecha_final'].str.replace('178-01-21', '1798-01-21').str.replace(
            r'179\'-07-09', '1790-07-09', regex=True).str.replace(r'1º', '01', regex=True).str.replace('1773- -06', '1773')
        data['fecha_inicial'] = data['fecha_inicial'].str.replace(
            r'1º', '01', regex=True)

        data['ca_objects.unitdate.date_value'] = data.apply(
            lambda x: self.get_date_range(x['fecha_inicial'], x['fecha_final']), axis=1)
        
        data = data.drop(columns=['fecha_inicial', 'fecha_final'])

        data['ca_objects.idno'] = data['ca_collections.idno'] + '.' + \
            data['ca_objects.idno'].str.replace(r'\.', '', regex=True)

        # rearange columns
        data = data[['ca_collections.idno', 'ca_collections.idno_institucion',
                     'ca_collections.preferred_labels_institucion',
                     'ca_collections.idno_fondo', 'ca_collections.preferred_labels_fondo',
                     'ca_collections.idno_subfondo',
                     'ca_collections.preferred_labels_subfondo', 'collection_type_subfondo',
                     'ca_collections.arrangement_subfondo',
                     'ca_collections.preferred_labels', 'ca_collections.arrangement',
                     'ca_collections.extent_text',
                     'ca_collections.repository.repositoryName',
                     'ca_collections.scopecontent', 'ca_collections.accessrestrict',
                     'ca_collections.reproduction', 'ca_collections.note',
                     'ca_collections.repository.repositoryLocation', 'ca_places',
                     'ca_collections.description', 'ca_collections.relatedmaterial',
                     'ca_collections.unitdate.date_value',
                     'ca_collections.unitdate.dates_types',
                     'ca_objects.idno', 'ca_objects.preferred_labels',
                     'ca_objects.description', 'ca_objects.accessrestrict',
                     'ca_objects.reproduction', 'ca_objects.note', 'ca_objects.originalsloc',
                     'ca_objects.arrangement', 'ca_objects.otherfindingaid',
                     'ca_entities_inst', 'ca_entities',
                     'ca_objects.extent_text',
                     'ca_objects.unitdate.date_value']]

        return data

    def get_date_range(self, fecha_inicial: str, fecha_final: str) -> str:
        """
        Get the date range from fecha_inicial and fecha_final
        and ensure that the date range is consistent and the dates
        are correct.

        Args:
            fecha_inicial (str): fecha_inicial
            fecha_final (str): fecha_final

        Returns:
            str: date range

        """

        def remove_date_placeholders(
            x): return re.sub(r'-00|0000-00-00|0000', '', x)

        fecha_inicial = remove_date_placeholders(fecha_inicial)
        fecha_final = remove_date_placeholders(fecha_final)

        # check if dates are valid and if not, find the nearest valid date
        if not self.is_valid_date(fecha_inicial) and fecha_inicial != '':
            try:
                fecha_inicial = self.find_nearest_valid_date(fecha_inicial)
            except ValueError as e:
                log.error(
                    f"{fecha_inicial} en columna \'fecha_inicial\' - Error: {e}")
                fecha_inicial = ''

        if not self.is_valid_date(fecha_final) and fecha_final != '':
            try:
                fecha_final = self.find_nearest_valid_date(fecha_final)
            except ValueError as e:
                log.error(
                    f"{fecha_final} en columna \'fecha_final\' - Error: {e}")
                fecha_final = ''

        # if fecha_inicial and fecha_final are the same, return only one date
        if fecha_inicial == fecha_final:
            return fecha_inicial
        elif fecha_inicial > fecha_final:
            return f"{fecha_final} - {fecha_inicial}"
        else:
            return f"{fecha_inicial} - {fecha_final}"

    def is_valid_date(self, date: str) -> bool:
        """
        Check if a date is valid

        Parameters
        ----------
        date : str
            Date to check
            Format: YYYY-MM-DD

        Returns
        -------
        bool
        """

        try:
            if len(date.split('-')) == 1:
                datetime.strptime(date, '%Y')
            elif len(date.split('-')) == 2:
                year, month = date.split('-')
                if 1 <= int(month) <= 12:
                    datetime.strptime(date, '%Y-%m')
                else:
                    return False
            elif len(date.split('-')) == 3:
                datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def find_nearest_valid_date(self, date_str: str) -> str:
        """
        Fix invalid dates by finding the nearest valid date

        Parameters
        ----------
        date_str : str
            Date to fix
            Format: YYYY-MM-DD

        Returns
        -------
        str
            Fixed date
        """

        if len(date_str.split('-')) == 1:
            year = int(date_str)
            month = 1
            day = 1
        elif len(date_str.split('-')) == 2:
            year, month = map(int, date_str.split('-'))
            day = 1
        elif len(date_str.split('-')) == 3:
            year, month, day = map(int, date_str.split('-'))

        if month > 12:
            month = 12
        elif month < 1:
            month = 1

        last_day_of_month = calendar.monthrange(year, month)[1]
        while not self.is_valid_date(f'{year}-{month}-{last_day_of_month}'):
            last_day_of_month -= 1

        if day > last_day_of_month:
            day = last_day_of_month
        elif day < 1:
            day = 1

        date = datetime(year, month, day)
        return date.strftime('%Y-%m-%d')


if __name__ == '__main__':
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
    t.to_csv("data/rionegro_metadata_prepared.csv", index=False)
