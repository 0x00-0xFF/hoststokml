__author__ = 'Bram Stienstra'

import pygeoip
from pykml.factory import KML_ElementMaker as KML
from lxml import etree
import os


hosts = []
hostslatlong = []

with open(os.path.expanduser('./hosts.txt')) as inputfile:
    for x in inputfile:
        host = x.strip()
        host = str(host)
        hosts.append(str(host))

try:
    for x in hosts:
        host = str(x.strip())

        _rawgeodata = pygeoip.GeoIP('GeoLiteCity.dat')
        _geodata = _rawgeodata.record_by_addr(x)
        _hopip = str(x)
        _hoplat = _geodata['latitude']
        _hoplong = _geodata['longitude']
        hostslatlong.append([_hopip, _hoplat, _hoplong])
except:
    pass

_kmlname = 1
kmlfolder = KML.Folder()
for i in hostslatlong:
    if not "private" in str(i[2]):
        _xlat = i[1]
        _xlong = i[2]
        _kmlcoord = "{},{}".format(_xlong,_xlat)
        _kmlnr = i[0]
        _kmlname = i[0]
        _kmldescr = "<h1>{}</h1>".format(i[1])
        _kmldescr = "<a href=\"https://www.robtex.com/ip/{}.html\">{}</a>".format(i[0],i[0])
        _kml = KML.Placemark(KML.name(_kmlname),
                             KML.description(_kmldescr),
                             KML.Point(KML.coordinates(_kmlcoord)))
        kmlfolder.append(_kml)


def getXmlWithCDATA(obj, cdata_elements):
  # Convert Objectify document to lxml.etree (is there a better way?)
    root = etree.fromstring(etree.tostring(etree.ElementTree(obj)))

  #Create an xpath expression to search for all desired cdata elements
    xpath = '|'.join(map(lambda tag: '//kml:' + tag, cdata_elements))

    results = root.xpath(xpath, namespaces={'kml': 'http://www.opengis.net/kml/2.2'})
    for element in results:
        element.text = etree.CDATA(element.text)
    return root

TEXT_ELEMENTS = ['description']

kmlobj_with_cdata = getXmlWithCDATA(kmlfolder, TEXT_ELEMENTS)

# print etree.tostring(kmlobj_with_cdata, pretty_print=True)

kmlfile = open("test.kml", "wb")
kmlfile.write(etree.tostring(kmlfolder, pretty_print=True))
kmlfile.close()