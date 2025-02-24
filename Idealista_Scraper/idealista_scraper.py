from web_scraper import WebScraper
from bs4 import BeautifulSoup as bs

# Clase IdealistaScraper que utiliza WebScraper para obtener los detalles de los anuncios
class IdealistaScraper:
    def __init__(self, browser):
        # Inicializa la clase con el navegador y crea un objeto WebScraper
        self.browser = browser
        self.scraper = WebScraper(browser)

    def get_listing_ids(self, url):
        """
        Obtiene los identificadores de los anuncios en una página de resultados de búsqueda.
        """
        # Usa el WebScraper para cargar la página
        self.scraper.load_page(url)
        html = self.browser.page_source  # Obtiene el código HTML de la página
        soup = bs(html, 'html')  # Convierte el HTML en un objeto BeautifulSoup para analizarlo

        # Encuentra todos los artículos en la página que representan anuncios
        articles = soup.find('main', {'class': 'listing-items'}).find_all('article')

        # Extrae el identificador de cada artículo
        ids = [article.get('data-element-id') for article in articles]
        # Filtra los valores None (si los hubiera)
        return [mueble for mueble in ids if mueble is not None]

    def parse_property(self, id_inmueble):
        """
        Obtiene los detalles de una propiedad individual.
        """
        # Construye la URL de la propiedad
        url = f"https://www.idealista.com/inmueble/{id_inmueble}/"
        self.scraper.load_page(url)  # Usa WebScraper para cargar la página de la propiedad
        html = self.browser.page_source  # Obtiene el HTML
        soup = bs(html, 'html')  # Analiza el HTML con BeautifulSoup

        # Extrae los detalles de la propiedad (título, ubicación, precio, etc.)
        titulo = soup.find('span', {'class': 'main-info__title-main'}).text
        localizacion = soup.find('span', {'class': 'main-info__title-minor'}).text
        precio = int(soup.find('span', {'class': 'txt-bold'}).text.replace('.', ''))  # Precio sin puntos

        # Extrae las características básicas y extras de la propiedad
        caract_basicas = [caract.text.strip() for caract in soup.find('div', {'class': 'details-property-feature-one'}).find_all('li')]
        caract_extra = [caract.text.strip() for caract in soup.find('div', {'class': 'details-property-feature-two'}).find_all('li')]

        # Devuelve los datos obtenidos en un diccionario
        return {
            'titulo': titulo,
            'localizacion': localizacion,
            'precio': precio,
            'caracteristicas_basicas': caract_basicas,
            'caracteristicas_extras': caract_extra
        }
