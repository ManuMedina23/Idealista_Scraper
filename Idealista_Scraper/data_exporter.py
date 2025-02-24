import pandas as pd

# Clase DataExporter que gestiona la exportación de datos a CSV
class DataExporter:
    @staticmethod
    def save_to_csv(data, filename):
        """
        Guarda los datos en un archivo CSV.
        """
        # Convierte los datos en un DataFrame de pandas
        df = pd.DataFrame(data)
        # Guarda el DataFrame en un archivo CSV
        df.to_csv(filename, index=False, sep=';', encoding='utf-16')
