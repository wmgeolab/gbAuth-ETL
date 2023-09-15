# gbAuth-ETL

This repository contains a Python ETL (Extract, Transform, Load) pipeline designed to collect data from UNSALB (United Nations Spatial Data Repository) through web scraping. The collected data is then transformed and organized into zip files, which are made available in the `gbAuthoritative` folder in source data of the [geoBoundaries repository](https://github.com/wmgeolab/geoBoundaries).

## Overview

The ETL pipeline consists of the following main steps:

1. **Extraction**:
   - Data is collected from UNSALB using web scraping techniques.
   - The collected data includes geojsons of ADM2,ADM1 and ADM0 Levels.

2. **Transformation**:
   - The raw data is processed and transformed into a format compatible with the `gbAuthoritative` folder structure.

3. **Loading**:
   - The transformed data is organized into zip files and made available in the appropriate folder in the geoBoundaries repository.
 


For more information on the geoBoundaries project, visit [wmgeolab/geoBoundaries](https://github.com/wmgeolab/geoBoundaries).
