import ezdxf
import pandas as pd
import geopandas as gpd
import random
import shapely.geometry as geometry
from shapely.geometry import Point, Polygon
import csv
import re

#utwórz nowy plik dxf
przeglad=ezdxf.new(dxfversion='R2010')
model=przeglad.modelspace()

#wczytaj plik txt z punktami
print('Proszę podać nazwę pliku do wczytania')   #zaczytanie pliku z xyhatryb
plik_xyh = input()


#ustalenie separatora
testowy = open(plik_xyh).read()
separatory = [' ', '\t']
podzial = csv.Sniffer().sniff(testowy, separatory).delimiter
print ('sperator to ' + podzial)

#przetworzenie pliku w zaleznosci od tego jaki separator jest w danym pliku
if podzial ==' ' :
    plikOdcz = open(plik_xyh).readlines()
#    plikPop = open(plik_xyh+'_pop.txt',"w")
#    for line in plikOdcz:
#        line = re.sub(r'^\s+' , '', line)
#        line = re.sub(r'\s+' , ' ', line)
#        print (line)
#        plikPop.write (line+'\n')
#    plikPop.close()
    data = pd.read_csv(plik_xyh, sep=podzial, header=None, names=range(7))  #utworzenie dataframe z pliku z pikietami
else:        
    data = pd.read_csv(plik_xyh, sep=podzial, header=None)  #utworzenie dataframe z pliku z pikietami

print(data)

try:
    color = random.randint(2,220) #losowy kolor dla operatu
#konwersja punktów do geometrii
    points = [Point(xyh) for xyh in zip(data[2], data[1], data[3])]
    point_collection = geometry.MultiPoint(list(points))
except Exception as komunikat:
    print(type(komunikat))
    print(komunikat)

            
    #wczytaj punkty do dxf
for index in data.index:
    wspolrzedne= (data[2][index],data[1][index])
    tekst1 = data[0][index]
    tekst2 = data[4][index]
    tekst3 = data[5][index]
    #print (tekst+wspolrzedne)
    model.add_text(tekst1, dxfattribs={'layer':'nr_pkt', 'color':color, 'height':1}).set_pos((wspolrzedne), align='TOP_LEFT')
    model.add_text(tekst2, dxfattribs={'layer':'mat', 'color':color, 'height':1}).set_pos((wspolrzedne), align='MIDDLE_LEFT')
    model.add_text(tekst3, dxfattribs={'layer':'srednica', 'color':color, 'height':1}).set_pos((wspolrzedne), align='BOTTOM_LEFT')

#zapis pliku dxf
przeglad.saveas('wczytane_wsp.dxf')
