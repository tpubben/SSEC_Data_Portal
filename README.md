**This application requires the following dependencies:**

  - Django
  - Django-guardian
  - GDAL
  - PROJ4

**Not intended for production work. Intended as proof of concept only. Record level security not implemented at this time.**

# Description

This is a Django application that uses and extended user model to allow clients to access reports and web maps stored on a server for
their assets. Users log in and see a list of their pipelines and the associated reports/web maps.

## Web Maps: 

Geospatial data hosted on a Geoserver implementation using a Postgres 10.8 (with PostGIS extensions) back-end. 

Web maps generated using Leaflet and the Geoserver WMS to serve raster tiles for survey data, pipeline location and raster base imagery
(if supplied by client survey).

## Reports:

Stored as static flat files on the webserver.

## File and layer naming conventions

Files and geoserver data layers must be named according to a strict naming convention to ensure functionality:

- ClientName_Pipeline Name_YYYY-MM-DD

Where "ClientName" is the CamelCased concatenation of the first two words of a client's name. Eg:

- Sample Gas Company Ltd. -> SampleGas
- Gas Ltd. -> GasLtd

## Passing variables into leaflet

Variables are passed into Leaflet by pushing the filename to a URL variable and using HTTP Get to pull that variable out and pass the
parsed values into the Javascript web map.
