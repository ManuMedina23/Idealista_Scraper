import undetected_chromedriver as uc
from idealista_crawler import IdealistaCrawler
from data_exporter import DataExporter
import random
import time

if __name__ == "__main__":
    # Paso 1: Crear el navegador
    browser = uc.Chrome()

    # Paso 2: Definir la URL base para la búsqueda
    base_url = 'https://www.idealista.com/areas/alquiler-viviendas/'
    busqueda_url = '?shape=%28%28sy%7CaFjhxU%7DlIcyDgf%40%7DqNxvAc%60ErxQytHz%7DEpvGi%7E%40%7EzKyzMloN%29%29'

    # Paso 3: Crear un objeto crawler para manejar todo el proceso de scraping
    crawler = IdealistaCrawler(browser, base_url,busqueda_url)

    # Paso 4: Recoger todos los identificadores de los anuncios
    listing_ids = crawler.scrape_all()

    # Paso 5: Crear una lista para almacenar los detalles de cada propiedad
    properties = []
    for listing_id in listing_ids:
        # Obtiene los datos de cada propiedad y los agrega a la lista 'properties'
        try:
            property_data = crawler.scraper.parse_property(listing_id)
            properties.append(property_data)
        except:
            DataExporter.save_to_csv(properties, 'casas_idealista.csv')

        print ("se ha añadido un piso, total: " + len(properties))
        time.sleep(random.randint(4, 8))  # Esperar un poco entre peticiones para evitar bloqueos

    # Paso 6: Exportar los datos a un archivo CSV
    DataExporter.save_to_csv(properties, 'casas_idealista.csv')

    
    print("Scraping completado y datos guardados en casas_idealista.csv")
