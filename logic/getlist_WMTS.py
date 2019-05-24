from __future__ import (absolute_import, division, print_function)
from owslib.wmts import WebMapTileService

def get_wmts():
    wmts = WebMapTileService('http://192.168.1.232:8080/geoserver/BurntLake/gwc/service/wmts?')
    contents = sorted(list(wmts.contents))
    service_list.services.append(contents)
    print (service_list.services)

class service_list():
    services = []

get_wmts()
