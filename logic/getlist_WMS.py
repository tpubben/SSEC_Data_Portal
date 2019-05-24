from owslib.wms import WebMapService


def get_wmslist():
    wms = WebMapService('http://192.168.1.232:8080/geoserver/BurntLake/gwc/service/wms?', version='1.1.1')

    servlist = list(wms.contents)
    class_variable.layers.append(servlist)

    frmt = list(wms.getOperationByName('GetMap').formatOptions)
    class_variable.formats.append(frmt)

    print('Layers:', class_variable.layers)
    print('Formats:', class_variable.formats)

class class_variable():
    layers = []
    formats = []

get_wmslist()

