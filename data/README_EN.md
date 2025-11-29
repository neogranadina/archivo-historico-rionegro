# Dataset: Archivo Histórico de Rionegro - Processed Metadata

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17626109.svg)](https://doi.org/10.5281/zenodo.17626109)

## Dataset Description

This dataset contains processed archival metadata from the Archivo Histórico de Rionegro (Historical Archive of Rionegro), Colombia. The data has been cleaned, structured, and prepared for ingestion into the Collective Access digital repository system (abcng.org).

## Dataset Identification

- **Title**: Archivo Histórico de Rionegro - Processed Archival Metadata
- **Project**: Neogranadina collaborative digital heritage initiative
- **Technical Processing**: Jairo A. Melo Flórez
- **Subject**: Digital Humanities, Archival Science, Colombian History, Cultural Heritage
- **Date Created**: 2023 (original data collection: 2022-2023)
- **Date Modified**: 2023-07-20
- **Language**: Spanish (spa)
- **Coverage**: Rionegro, Antioquia, Colombia (temporal: 18th-20th century)

## File Structure and Contents

```
data/
├── xlsx/                               # Source data files
│   ├── rionegro_fondos.xlsx           # Collections/fonds structure (1.4 MB)
│   └── rionegro_metadata.xlsx         # Original archival metadata (varies)
├── csv/                               # Processed data files
│   ├── rionegro_fondos.csv           # Collections data in CSV format (1.3 MB)
│   ├── rionegro_collections.csv      # Processed collections structure (1.3 MB)
│   ├── rionegro_metadata.csv         # Cleaned metadata (32.5 MB)
│   └── rionegro_metadata_prepared.csv # Final processed metadata (59.2 MB)
└── README.md                          # This documentation file
```

## Data Description

### Collections Data (`rionegro_fondos.xlsx`, `rionegro_collections.csv`)
- **Content**: Hierarchical structure of archival collections, including institutions, fonds, series, and subseries
- **Records**: ~1,200 collection records
- **Fields**: Collection identifiers, titles, dates, extent, arrangement, access conditions
- **Structure**: Follows archival description standards (ISAD(G) based)

### Metadata Files (`rionegro_metadata.csv`, `rionegro_metadata_prepared.csv`)
- **Content**: Item-level descriptions of archival documents
- **Records**: ~8,000+ document records  
- **Fields**: Document identifiers, titles, dates, creators, subjects, physical description, access conditions
- **Format**: Structured for Collective Access import
- **Date Range**: Documents from 18th-20th centuries

## Data Processing Methodology

1. **Source**: Original data exported from institutional databases and spreadsheets
2. **Cleaning**: Standardized column names, removed empty fields, normalized text
3. **Structuring**: Applied hierarchical archival organization (institution > fonds > series > items)
4. **Identifier Generation**: Created unique identifiers following ISO standards
5. **Date Normalization**: Standardized date formats and ranges
6. **Mapping**: Aligned fields with Collective Access metadata schema

### Processing Scripts
The complete data processing pipeline is available in the companion GitHub repository:
- **Repository**: https://github.com/neogranadina/archivo-historico-rionegro
- **Scripts**: `prepare.py`, `colecciones.py`, `metadatos.py`, `import_files.py`

## Metadata Standards and Schemas

- **Archival Description**: Based on ISAD(G) (International Standard Archival Description)
- **Encoding**: UTF-8 character encoding
- **Date Format**: ISO 8601 (YYYY-MM-DD) where precise dates available
- **Identifier Scheme**: ISO 15511 compliant institutional identifiers (CO.AHR.*)
- **Language Codes**: ISO 639-2 (spa for Spanish)
- **Subject Headings**: Local controlled vocabulary with geographic and topical terms

## Data Quality and Completeness

- **Completeness**: ~95% of required fields populated for collections, ~80% for item descriptions
- **Accuracy**: Data validated against original archival finding aids
- **Consistency**: Standardized vocabulary and formatting applied throughout
- **Known Issues**: 
  - Some date ranges approximate due to incomplete historical records
  - Geographic names may vary in spelling (historical vs. modern)
  - Physical condition descriptions use local terminology

## Usage Rights and Licensing

- **License**: Creative Commons Zero v1.0 Universal (CC0 1.0) - Public Domain Dedication
- **Rights**: This work has been dedicated to the public domain
- **Usage**: Free to use for any purpose without restriction
- **Attribution**: While not required, attribution is appreciated for scholarly purposes
- **Restrictions**: None for metadata; access to original documents may be restricted by archive
- **Legal Notice**: To the extent possible under law, the dataset creator has waived all copyright and related rights to this work

## Attribution and Citation

### Preferred Citation
Fundación Histórica Neogranadina. (2023). *Archivo Histórico de Rionegro - Processed Archival Metadata* [Dataset]. Zenodo. https://doi.org/10.5281/zenodo.17626109

### Contributor Roles
- **Data Collection & Digitization**: Neogranadina collaborative team
- **Data Processing & Repository Publication**: Jairo A. Melo Flórez

### Related Publications
- Repository software: https://github.com/neogranadina/archivo-historico-rionegro
- Digital collection: https://abcng.org [if available]

## Technical Requirements

### Software Dependencies
- **Reading CSV files**: Any spreadsheet software (Excel, LibreOffice, Google Sheets)
- **Data analysis**: Python (pandas, numpy), R, or similar
- **Character encoding**: UTF-8 support required

### Recommended Tools
- **Python**: pandas library for data manipulation
- **OpenRefine**: For data exploration and further cleaning
- **Collective Access**: Target repository system for this data structure

## Version History

- **Version 1.0** (2023-07-20): Initial processed dataset
  - Complete processing of collections and metadata
  - Standardized identifiers and field mappings
  - Prepared for Collective Access import

## Related Resources

- **Processing Code**: https://github.com/neogranadina/archivo-historico-rionegro
- **Institutional Repository**: abcng.org
- **Collective Access**: https://collectiveaccess.org/
- **ISAD(G) Standard**: https://www.ica.org/en/isadg-general-international-standard-archival-description-second-edition

## Keywords

Digital Humanities, Archival Metadata, Colombian Archives, Cultural Heritage, Rionegro, Antioquia, Historical Documents, Collective Access, ISAD(G), Metadata Processing
