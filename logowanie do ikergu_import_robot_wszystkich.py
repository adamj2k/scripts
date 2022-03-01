# -*- coding: utf-8 -
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome('C:\_PRACA\chromedriver')
# funckcja logowania do strony ikerg - policki -> dodać parametry url, login, haslo
def ikerg_login():
    driver.get("https://ikonto.e-osrodek.szczecin.pl/#/login?origin=IKERG")
    time.sleep(4)
    driver.find_element_by_id("ember12-field").send_keys(uzytkownik)
    driver.find_element_by_id("ember17-field").send_keys(haslo)
    driver.find_element_by_class_name('btn.btn-primary').click()
    time.sleep(7)

# funkcja pobierania listy wszystkich robot i zapisania jej do pliku txt, dodać prametry -> adres url czy funkcja ma zwracać dataframe?
def pobierzListeRobot ():
    driver.get("https://e-osrodek.szczecin.pl/#/ikerg/zgloszone-prace?onlyActiveWorks=false")
    time.sleep(5)
    #wybór większej iloci wierszy maks100- lista ze wszystkich pól wybieralnych i wybór z ostatniej listy rozwijalnej
    listyWybieralne = driver.find_elements_by_class_name('ember-basic-dropdown-trigger.ember-power-select-trigger')
    listyWybieralne[2].click()
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//ul[@class='ember-power-select-options']/li[4]"))).click()
    time.sleep(3)
    #pobranie strony do przetarzania
    soup=BeautifulSoup(driver.page_source, 'lxml')
    #okreslenie ilosci stron do przetworzenia
    tekstIloscStron = soup.find_all('div', class_='col-md-12 text-center')
    tekstDoPrzetworzenia = str(tekstIloscStron[0])
    pocz=tekstDoPrzetworzenia.find('Liczba stron: ')
    liczbaStron=int(tekstDoPrzetworzenia[(pocz+14):(pocz+14+1)])
    print(liczbaStron)
    #pusta lista do zapisania listy robót
    wszystkieRoboty=[]
    #petla iteracyjna po kolejnych stronach
    for n in range (0, liczbaStron):
        #pobranie strony do przetarzania
        soup2=BeautifulSoup(driver.page_source, 'lxml')
        #wszystkie  tabele na stronie
        table = soup2.find_all('table')[0]
        #import tabely do listy za pomocą pandas
        listaRoboty = pd.read_html(str(table),header=0)
        #print(listaRoboty)
        #poszerzenie listy o dane z kolejnej strony
        wszystkieRoboty.extend(listaRoboty)
        #print(wszystkieRoboty)
        #przejscie do następnej strony klikniecie w następne
        linkiStron = driver.find_elements_by_class_name('page-link')
        linkiStron[3].click()
        time.sleep(2)
    #zlaczenie wszystkich 
    robotyDF = pd.concat(wszystkieRoboty)
    # pokazanie tabeli
    print(robotyDF)
    # zapisanie tabeli do pliku txt
    robotyDF.to_csv ('roboty.txt', sep='\t')
    
#uruchomienie funkcji logowania i pobierania listy robót
ikerg_login()
pobierzListeRobot()
