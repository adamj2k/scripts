import ezdxf
import pandas as pd
import geopandas as gpd
import random
import shapely.geometry as geometry
from shapely.geometry import Point, Polygon

#utwórz nowy plik dxf
przeglad=ezdxf.new(dxfversion='R2010')
model=przeglad.modelspace()

#import przeglądówek 2000 i 65 z obszarami
print('Proszę podać nazwę pliku wraz ze sciezka z plikami SHP do konwersji - ukl2000')   #zaczytanie pliku z shp z obszarami
plik_2000= input()
print('Proszę podać nazwę pliku wraz ze sciezka z plikami SHP do konwersji - ukl1965')   #zaczytanie pliku z shp z obszarami
plik_65 = input()
przeg2000=gpd.read_file(plik_2000)
przeg65=gpd.read_file(plik_65)

#wczytaj plik txt z punktami
print('Proszę podać nazwę pliku ze spisem plików do konwersji')   #zaczytanie pliku z nazwami txt .... .txt
plik_nazwy = input()
with open (plik_nazwy) as na:
     nazwy = [line.rstrip() for line in na]
     
calosc=pd.DataFrame()   #utworzenie pustej tabeli do której będą zapisywane kolejne pliki

for n in nazwy:
    print('przetarzany plik: '+n)  #plik z pikietami nr x y 
    dane = pd.read_csv(n, sep=' ', header=None)  #utworzenie dataframe z pliku z pikietami
    color = random.randint(2,220) #losowy kolor dla operatu
    #konwersja punktów do geometrii
    points = [Point(xyh) for xyh in zip(dane[2], dane[1], dane[3])]
    point_collection = geometry.MultiPoint(list(points))
    #sprawdzenie w jakim obszarze są punkty z pliku ukl2000
    for index, row in przeg2000.iterrows():
        obszar=(row[6])
        zawiera=point_collection.within(obszar)
        przecina=point_collection.crosses(obszar)
        #sprawdzenie zawierania i przecinania punktów przez obszar
        if zawiera is True or przecina is True:
            wynik=(row[5])
            wynik_txt=(n+' czesc='+wynik)
            print(wynik_txt)
            break
    #sprawdzenie w jakim obszarze są punkty z pliku ukl65    
    for index, row in przeg65.iterrows():
        obszar65=(row[6])
        zawiera65=point_collection.within(obszar65)
        przecina65=point_collection.crosses(obszar65)
        #sprawdzenie zawierania i przecinania punktów przez obszar
        if zawiera65 is True or przecina65 is True:
            wynik=(row[5])
            print(n+' czesc='+wynik)
            break
        
    #wczytaj punkty do dxf
    for index in dane.index:
        wspolrzedne= (dane[2][index],dane[1][index])
        tekst = dane[0][index]
        #print (tekst+wspolrzedne)
        model.add_text(tekst, dxfattribs={'layer':n, 'color':color, 'height':5}).set_pos((wspolrzedne), align='LEFT')

#zapis pliku dxf
przeglad.saveas('przeglad.dxf')
