# Dataset: Archivo Histórico de Rionegro - Metadatos Procesados

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17626109.svg)](https://doi.org/10.5281/zenodo.17626109)

## Descripción del Dataset

Este dataset contiene metadatos archivísticos procesados del Archivo Histórico de Rionegro, Colombia. Los datos han sido limpiados, estructurados y preparados para su ingesta en el sistema de repositorio digital Collective Access (abcng.org).

## Identificación del Dataset

- **Título**: Archivo Histórico de Rionegro - Metadatos Archivísticos Procesados
- **Proyecto**: Iniciativa colaborativa de patrimonio digital de Neogranadina
- **Procesamiento Técnico**: Jairo A. Melo Flórez
- **Materia**: Humanidades Digitales, Ciencias Archivísticas, Historia Colombiana, Patrimonio Cultural
- **Fecha de Creación**: 2023 (recolección de datos original: 2022-2023)
- **Fecha de Modificación**: 2023-07-20
- **Idioma**: Español (spa)
- **Cobertura**: Rionegro, Antioquia, Colombia (temporal: siglos XVIII-XX)

## Estructura de Archivos y Contenidos

```text
data/
├── xlsx/                               # Archivos de datos fuente
│   ├── rionegro_fondos.xlsx           # Estructura de colecciones/fondos (1.4 MB)
│   └── rionegro_metadata.xlsx         # Metadatos archivísticos originales (variable)
├── csv/                               # Archivos de datos procesados
│   ├── rionegro_fondos.csv           # Datos de colecciones en formato CSV (1.3 MB)
│   ├── rionegro_collections.csv      # Estructura de colecciones procesada (1.3 MB)
│   ├── rionegro_metadata.csv         # Metadatos limpiados (32.5 MB)
│   └── rionegro_metadata_prepared.csv # Metadatos procesados finales (59.2 MB)
└── README.md                          # Este archivo de documentación
```

## Descripción de los Datos

### Datos de Colecciones (`rionegro_fondos.xlsx`, `rionegro_collections.csv`)
- **Contenido**: Estructura jerárquica de colecciones archivísticas, incluyendo instituciones, fondos, series y subseries
- **Registros**: ~1,200 registros de colecciones
- **Campos**: Identificadores de colecciones, títulos, fechas, extensión, organización, condiciones de acceso
- **Estructura**: Sigue estándares de descripción archivística (basado en ISAD(G))

### Archivos de Metadatos (`rionegro_metadata.csv`, `rionegro_metadata_prepared.csv`)
- **Contenido**: Descripciones a nivel de ítem de documentos archivísticos
- **Registros**: ~8,000+ registros de documentos
- **Campos**: Identificadores de documentos, títulos, fechas, creadores, materias, descripción física, condiciones de acceso
- **Formato**: Estructurado para importación en Collective Access
- **Rango Temporal**: Documentos de los siglos XVIII-XX

## Metodología de Procesamiento de Datos

1. **Fuente**: Datos originales exportados de bases de datos institucionales y hojas de cálculo
2. **Limpieza**: Estandarización de nombres de columnas, eliminación de campos vacíos, normalización de texto
3. **Estructuración**: Aplicación de organización archivística jerárquica (institución > fondo > serie > ítem)
4. **Generación de Identificadores**: Creación de identificadores únicos siguiendo estándares ISO
5. **Normalización de Fechas**: Estandarización de formatos y rangos de fechas
6. **Mapeo**: Alineación de campos con el esquema de metadatos de Collective Access

### Scripts de Procesamiento
El pipeline completo de procesamiento de datos está disponible en el repositorio de GitHub complementario:
- **Repositorio**: https://github.com/neogranadina/archivo-historico-rionegro
- **Scripts**: `prepare.py`, `colecciones.py`, `metadatos.py`, `import_files.py`

## Estándares de Metadatos y Esquemas

- **Descripción Archivística**: Basado en ISAD(G) (Norma Internacional General de Descripción Archivística)
- **Codificación**: Codificación de caracteres UTF-8
- **Formato de Fecha**: ISO 8601 (YYYY-MM-DD) donde hay fechas precisas disponibles
- **Esquema de Identificadores**: Identificadores institucionales compatibles con ISO 15511 (CO.AHR.*)
- **Códigos de Idioma**: ISO 639-2 (spa para español)
- **Encabezados de Materia**: Vocabulario controlado local con términos geográficos y temáticos

## Calidad y Completitud de los Datos

- **Completitud**: ~95% de campos requeridos poblados para colecciones, ~80% para descripciones de ítems
- **Exactitud**: Datos validados contra instrumentos de descripción archivística originales
- **Consistencia**: Vocabulario y formato estandarizado aplicado en todo el conjunto
- **Problemas Conocidos**: 
  - Algunos rangos de fechas son aproximados debido a registros históricos incompletos
  - Los nombres geográficos pueden variar en ortografía (histórica vs. moderna)
  - Las descripciones de condición física usan terminología local

## Derechos de Uso y Licenciamiento

- **Licencia**: Creative Commons Zero v1.0 Universal (CC0 1.0) - Dedicación al Dominio Público
- **Derechos**: Este trabajo ha sido dedicado al dominio público
- **Uso**: Libre uso para cualquier propósito sin restricciones
- **Atribución**: Aunque no es requerida, la atribución es apreciada para propósitos académicos
- **Restricciones**: Ninguna para metadatos; el acceso a documentos originales puede estar restringido por el archivo
- **Aviso Legal**: En la medida de lo posible bajo la ley, el creador del dataset ha renunciado a todos los derechos de autor y derechos relacionados sobre este trabajo

## Atribución y Citación

### Citación Preferida
Fundación Histórica Neogranadina. (2023). *Archivo Histórico de Rionegro - Metadatos Archivísticos Procesados* [Dataset]. Zenodo. https://doi.org/10.5281/zenodo.17626109

### Roles de Contribuyentes
- **Recolección y Digitalización**: Equipo colaborativo de Neogranadina
- **Procesamiento Técnico y Publicación**: Jairo A. Melo Flórez

### Publicaciones Relacionadas
- Software del repositorio: https://github.com/neogranadina/archivo-historico-rionegro
- Colección digital: https://abcng.org [si está disponible]

## Requisitos Técnicos

### Dependencias de Software
- **Lectura de archivos CSV**: Cualquier software de hojas de cálculo (Excel, LibreOffice, Google Sheets)
- **Análisis de datos**: Python (pandas, numpy), R, o similar
- **Codificación de caracteres**: Se requiere soporte UTF-8

### Herramientas Recomendadas
- **Python**: biblioteca pandas para manipulación de datos
- **OpenRefine**: Para exploración de datos y limpieza adicional
- **Collective Access**: Sistema de repositorio objetivo para esta estructura de datos

## Historial de Versiones

- **Versión 1.0** (2023-07-20): Dataset procesado inicial
  - Procesamiento completo de colecciones y metadatos
  - Identificadores estandarizados y mapeos de campos
  - Preparado para importación en Collective Access

## Recursos Relacionados

- **Código de Procesamiento**: https://github.com/neogranadina/archivo-historico-rionegro
- **Repositorio Institucional**: abcng.org
- **Collective Access**: https://collectiveaccess.org/
- **Estándar ISAD(G)**: https://www.ica.org/en/isadg-general-international-standard-archival-description-second-edition

## Palabras Clave

Humanidades Digitales, Metadatos Archivísticos, Archivos Colombianos, Patrimonio Cultural, Rionegro, Antioquia, Documentos Históricos, Collective Access, ISAD(G), Procesamiento de Metadatos

---

*Este README sigue los principios de datos FAIR para asegurar que el dataset sea Localizable, Accesible, Interoperable y Reutilizable.*