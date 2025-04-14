import sqlalchemy as sa
from sqlalchemy import URL, MetaData,Table, Column, Integer, String


#Conexion BD
__url_object = URL.create(
    drivername='postgresql',
    username='idealista_admin',
    password='idealistaJamon2025!',
    host='localhost',
    port=5432,
    database='idealista_analyzer'
)
try:
    engine = sa.create_engine(__url_object)
    if (engine != None):
        print('Se ha conectado con exito a la bd')
except:
    print('Error conectando a la bd')    


def get_engine():
    return engine
