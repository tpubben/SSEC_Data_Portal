import xml.etree.ElementTree as ET
import urllib.request as urllib
import os

def open_wmts():
    urllib.urlretrieve('http://192.168.1.232:8080/geoserver/BurntLake/gwc/service/wmts?REQUEST=GetCapabilities',
                               'wmts.xml')
    with open('wmts.xml', 'r') as fh:
        tree = ET.parse(fh)
        root = ET.getroot ('Contents')
        for name in tree.iter('{http://www.opengis.net/ows/1.1}Title'):
            if name.text.startswith ('GeoServer'):
                pass
            else:
                for format in tree.iter('Format'):
                    class_variable.x.append((name.text, format))

    print (class_variable.x)

class class_variable():
    x = []

open_wmts()

os.remove('wmts.xml')