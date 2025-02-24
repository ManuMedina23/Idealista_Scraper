import undetected_chromedriver as uc 
from bs4 import BeautifulSoup as bs  
import pandas as pd
import time
import random

# SCRIPT PARA PARSEAR UNA SERIE DE INMUEBLES A TRAVES DE UNA LISTA DE IDs

# Configurar el navegador
browser = uc.Chrome()
url_grande = 'https://www.idealista.com/areas/alquiler-viviendas/?shape=%28%28sy%7CaFjhxU%7DlIcyDgf%40%7DqNxvAc%60ErxQytHz%7DEpvGi%7E%40%7EzKyzMloN%29%29'
browser.get(url_grande)
browser.find_element("xpath", '//*[@id="didomi-notice-agree-button"]').click()
time.sleep(random.randint(10,12))

# Función para parsear un inmueble
def parsear_inmueble(id_inmueble):

    print(f'\nCasa número: {id_inmueble}')
    
    url = f"https://www.idealista.com/inmueble/{id_inmueble}/"
    try:
        browser.get(url)
    except:
        return

    html = browser.page_source
    soup = bs(html, 'html.parser') 

    # Extraer datos
    titulo = soup.find('span', {'class': 'main-info__title-main'}).text.strip()
    print(titulo)


    localizacion = soup.find('span', {'class': 'main-info__title-minor'}).text.strip()
    print (localizacion)

    precio = int(soup.find('span', {'class': 'txt-bold'}).text.replace('.', '').strip())

    c1 = soup.find('div', {'class': 'details-property-feature-one'})
    caract_basicas = [caract.text.strip() for caract in c1.find_all('li')]


    c2 = soup.find('div', {'class': 'details-property-feature-two'})
    caract_extra = [caract.text.strip() for caract in c2.find_all('li')]


    # Crear un diccionario con los datos
    casa_data = {
        'titulo': titulo,
        'localizacion': localizacion,
        'precio': precio,
        'caracteristicas_basicas': caract_basicas,
        'caracteristicas_extras': caract_extra
    }

    return casa_data

# Leer el archivo CSV con los IDs de las casas
file_ids = 'ids_casas2.csv' # Sustituir por el nombre o ruta del archivo que contenga los ids
ids_casas = pd.read_csv(file_ids, sep=";", header=0)

# Lista para almacenar los datos de cada casa
lista_casas = []

# Iterar sobre cada ID y parsear la información
for i in range(len(ids_casas)):
    try:
        casa_data = parsear_inmueble(ids_casas.iloc[i].id)
        lista_casas.append(casa_data)
        time.sleep(random.randint(4, 8))  # Espera aleatoria para evitar bloqueos
    except Exception as e:
        print(f"Error al parsear el inmueble con ID {ids_casas.iloc[i].id}")
    finally:
        # Crear un DataFrame con todos los datos
        df_casas = pd.DataFrame(lista_casas)

        # Guardar el DataFrame resultante en un archivo CSV
        df_casas.to_csv('casas_idealista.csv', index=False, sep=';', encoding='utf-16')
