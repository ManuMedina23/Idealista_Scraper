import requests
from bs4 import BeautifulSoup as bs #Permite extraer el html y analizarlo
import random
import time
import pandas as pd
import numpy as np
from selenium import webdriver #Permite hacer web scrapping
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc #Permite no ser detectado
import time
from datetime import datetime

browser = uc.Chrome()

url_grande = 'https://www.idealista.com/areas/alquiler-viviendas/?shape=%28%28sy%7CaFjhxU%7DlIcyDgf%40%7DqNxvAc%60ErxQytHz%7DEpvGi%7E%40%7EzKyzMloN%29%29'

browser.get(url_grande)

browser.find_element("xpath", '//*[@id="didomi-notice-agree-button"]').click()

html = browser.page_source

soup = bs(html, 'html')

#Recoger todos los anuncios
article = soup.find('main',{'class':'listing-items'}).find_all('article')

#Obtener id de los anuncios (pisos)
id_muebles = [article.get('data-element-id') for article in article]


#Eliminar los None
id_muebles = [muebles for muebles in id_muebles if muebles is not None]


busqueda = 'shape=%28%28sy%7CaFjhxU%7DlIcyDgf%40%7DqNxvAc%60ErxQytHz%7DEpvGi%7E%40%7EzKyzMloN%29%29'
npagina = 1
ids = []

while True and npagina < 15:
    url = f'https://www.idealista.com/areas/alquiler-viviendas/pagina-{npagina}?{busqueda}'
    browser.get(url)

    time.sleep(random.randint(10,12))

    try:
        browser.find_element("xpath", '//*[@id="didomi-notice-agree-button"]').click()
    except:
        pass

    html = browser.page_source
    soup = bs(html, 'html')

    pagina_actual = int(soup.find('div',{'class':'pagination'}).find('li',{'class':'selected'}).text)
    if npagina == pagina_actual:
        articles = soup.find('main',{'class':'listing-items'}).find_all('article')
    else:
        break

    npagina += 1

    for article in articles:
        id_muebles = article.get('data-element-id')

        ids.append(id_muebles)

        time.sleep(random.randint(1,3))
        print(id_muebles)
        ids = [muebles for muebles in ids if muebles is not None]

ids_casas = pd.DataFrame(ids)
ids_casas.columns = ['id']
ids_casas

#Guardar en un csv los ids
ids_casas.to_csv('ids_casas.csv', index = False)

casas = pd.Series()

def parsear_inmueble(id_inmueble):
    print('\n Casa numero: ' + id_inmueble)
    
    url = "https://www.idealista.com/inmueble/" + id_inmueble + "/"

    browser.get(url)
    html = browser.page_source
    soup = bs(html, 'html')
    
    titulo = soup.find('span',{'class':'main-info__title-main'}).text
    print('\n Titulo: ' + titulo)

    localizacion = soup.find('span', {'class':'main-info__title-minor'}).text
    print('\n Localizacion: ' + localizacion)

    precio = int(soup.find('span',{'class':'txt-bold'}).text.replace('.',''))
    
    c1 = soup.find('div',{'class':'details-property-feature-one'})
    
    caract_basicas = [caract.text.strip() for caract in c1.find_all('li')]
    
    c2 = soup.find('div',{'class':'details-property-feature-two'})
    
    caract_extra = [caract.text.strip() for caract in c2.find_all('li')]

    casas['referencia'] = id_inmueble
    casas['titulo'] = titulo
    casas['localizacion'] = localizacion
    casas['precio'] = precio
    casas['caracteristicas_basicas'] = caract_basicas
    casas['caracteristicas_extras'] = caract_extra
    df_casas = pd.DataFrame(casas)

    return(df_casas.T)

df_casas = parsear_inmueble(ids_casas.iloc[0].id)
for i in range(1, len(ids)):
    try:
        df_casas = pd.concat([df_casas, parsear_inmueble(ids[i])])
        time.sleep(random.randint(4,8))
    except:
        print('error')
    finally:
        date = datetime.now().strftime("%d-%m-%Y")

        df_casas.reset_index(drop=True, inplace=True)
        df_casas.to_csv(f'casas_idealista_{date}.csv', index = False, sep = ';', encoding = 'utf-16')
