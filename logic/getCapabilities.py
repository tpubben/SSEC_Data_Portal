import xml.etree.ElementTree as ET
import urllib.request as urllib
import os

def open_wmts():
    urllib.urlretrieve('http://192.168.1.232:8080/geoserver/BurntLake/gwc/service/wmts?REQUEST=GetCapabilities',
                               'wmts.xml')
    with open('wmts.xml', 'r') as fh:
        tree = ET.parse(fh)
        for name in tree.iter('{http://www.opengis.net/ows/1.1}Title'):
            namevar = ''
            formatvar = ''
            if name.text.startswith ('GeoServer'):
                pass
            else:
                namevar = (name.text)
            for format in tree.iter('{http://www.opengis.net/wmts/1.0}Format'):
                if format.text.startswith('image/jpeg'):
                    formatvar = (format.text)
                if name.text.startswith('Geoserver'):
                    pass
                else:
                    pass
            class_variable.x.append([namevar, formatvar])


    print (class_variable.x)

class class_variable():
    x = []

open_wmts()

os.remove('wmts.xml')