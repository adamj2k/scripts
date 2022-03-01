import pandas as pd
import os
import ezdxf
import shapely.geometry as geometry
from shapely.geometry import Point
from shapely import wkt

#wczytaj plik txt z punktami
print('Proszę podać nazwę pliku')
punkty = input()
dane= pd.read_csv(punkty, sep='\t', header=None) #wczytanie współrzędnych
print (dane)


#konwersja punktów do geometrii
points = [Point(xyh) for xyh in zip(dane[1], dane[2], dane[3])]
point_collection = geometry.MultiPoint(list(points))
point_collection.envelope



#przetworzenie na convex hull
convex_hull_polygon = point_collection.convex_hull
poligon_buffor = convex_hull_polygon.buffer(5,1,3)

#eksport docelowo do dxf lub shp na razie wkt - instalacja fiona
eksport = wkt.dumps(poligon_buffor)
print (eksport)


"""
print('Proszę podać nazwę pliku DXF')   #plik do zaczytania
nazwapliku = input()
dokument=ezdxf.readfile(nazwapliku)
msp=dokument.modelspace()
for e in msp:
    if e.dxftype() == 'LINE':
        print_entity(e)
#pozyskanie danych z nagłówka pliku DXF i wsp do zakresu
gpnaroznik=dokument.header['$EXTMAX']
dlnaroznik=dokument.header['$EXTMIN']
x1=gpnaroznik[:1]
y1=gpnaroznik[1:2]
x2=dlnaroznik[:1]
y2=dlnaroznik[1:2]
glnaroznik=x2+y1
dpnaroznik=x1+y2
print (gpnaroznik)
print (dlnaroznik)
print (glnaroznik)
print (dpnaroznik)


#utwórz nowy plik dxf i utwórz w nim prostokąt wraz z opisem
przeglad=ezdxf.new(dxfversion='R2010')
przeglad.layers.new(punkty, dxfattribs={'color':5})
model=przeglad.modelspace()
#punkty=[gpnaroznik,dpnaroznik,dlnaroznik,glnaroznik,gpnaroznik]
model.add_polyline2d(points, dxfattribs={'layer':punkty})
#model.add_text(nazwapliku, dxfattribs={'layer':nazwapliku, 'color':5, 'height':20}).set_pos((dlnaroznik), align='LEFT')

przeglad.saveas('przeglad.dxf')
"""

