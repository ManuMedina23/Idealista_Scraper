import time
import random

# Clase WebScraper que maneja las interacciones básicas con la web
class WebScraper:
    def __init__(self, browser):
        # Inicializa la clase recibiendo el navegador (browser) como parámetro
        self.browser = browser

    def load_page(self, url):
        """
        Carga una página web usando el navegador (browser).
        También maneja el aviso de cookies en la página.
        """
        self.browser.get(url)  # Accede a la URL proporcionada
        try:
            # Si aparece el botón de aceptar cookies, lo hace clic
            self.browser.find_element("xpath", '//*[@id="didomi-notice-agree-button"]').click()
        except:
            # Si no aparece el botón (o ya se aceptaron las cookies), no hace nada
            pass
        # Pausa aleatoria para evitar ser detectado como un bot
        time.sleep(random.randint(10, 12))
