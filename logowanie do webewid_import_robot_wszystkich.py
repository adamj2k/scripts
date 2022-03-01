# -*- coding: utf-8 -
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome('C:\_PRACA\chromedriver')
# funckcja logowania do strony webewid portal geodety -> dodać parametry url, login, haslo
def ikerg_login():
    driver.get("https://goleniowski.webewid.pl/e-uslugi/portal-geodety")
    time.sleep(5)
    driver.find_element_by_id("login").send_keys(uzytkownik)
    driver.find_element_by_id("password").send_keys(haslo)
    driver.find_element_by_id("st-accept-button-cookies").click()
    time.sleep(2)
    driver.find_element_by_id("login-button").click()
    time.sleep(7)

# funkcja pobierania listy wszystkich robot i zapisania jej do pliku txt, dodać prametry -> adres url czy funkcja ma zwracać dataframe?
def pobierzListeRobot ():
    time.sleep(3)
    #wybór wszystkich robot nawet zakonczonych
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="surveyor-tab-strip-1"]/div/div[1]/div/div[1]/ul/li[27]/span/i'))).click()
    time.sleep(3)
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="odgikPortGeodKergSearchForm"]/table/tbody/tr[6]/th/label/input'))).click()
    time.sleep(3)
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="iw-geodeta-kergSearch-window"]/div/button[2]'))).click()
    time.sleep(3)
    #pusta lista do zapisania listy robót
    wszystkieRoboty=[]
        #pobranie strony do przetarzania
    soup2=BeautifulSoup(driver.page_source, 'lxml')
        #wszystkie  tabele na stronie
    table = soup2.find_all('table')[2]
        #import tabely do listy za pomocą pandas
    listaRoboty = pd.read_html(str(table),header=None)
        #poszerzenie listy o dane z kolejnej strony
    wszystkieRoboty.extend(listaRoboty)
        #przejscie do następnej strony klikniecie w następne
    #zlaczenie wszystkich 
    robotyDF = pd.concat(wszystkieRoboty)
    # pokazanie tabeli
    print(robotyDF)
    # zapisanie tabeli do pliku txt
    robotyDF.to_csv ('roboty_webewid.txt', sep='\t')
    
#uruchomienie funkcji logowania i pobierania listy robót
ikerg_login()
pobierzListeRobot()
