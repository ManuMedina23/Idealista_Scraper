from idealista_scraper import IdealistaScraper

# Clase IdealistaCrawler que gestiona el proceso completo de scraping de las páginas de búsqueda
class IdealistaCrawler:
    def __init__(self, browser, base_url, busqueda_url):
        """
        Inicializa la clase con el navegador y la URL base de búsqueda.
        """
        self.scraper = IdealistaScraper(browser)  # Crea un objeto IdealistaScraper
        self.base_url = base_url  # URL base para las búsquedas
        self.busqueda_url = busqueda_url
        self.ids = []  # Lista donde se guardarán los identificadores de los anuncios
        

    def scrape_all(self):
        """
        Scrapea todas las páginas de anuncios y obtiene los IDs de todas las propiedades.
        """
        npagina = 1
        while True:
            # Construye la URL para la página npagina          
            url = f"{self.base_url}pagina-{npagina}{self.busqueda_url}"
            
            ids = self.scraper.get_listing_ids(url)  # Obtiene los IDs de los anuncios
            if not ids:  # Si no hay más IDs en la página, se detiene el scraping
                break
            self.ids.extend(ids)  # Agrega los IDs obtenidos a la lista
            npagina += 1  # Incrementa el número de página para continuar con la siguiente

        print("Se han obtenido todos los anuncios")
        return self.ids  # Devuelve la lista con todos los IDs de los anuncios
