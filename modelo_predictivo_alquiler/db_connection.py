import sqlalchemy as sa
from sqlalchemy import URL, MetaData,Table, Column, Integer, String


#Conexion BD
__url_object = URL.create(
    drivername='postgresql',
    username='',
    password='',
    host='localhost',
    port=5432,
    database=''
)
try:
    engine = sa.create_engine(__url_object)
    if (engine != None):
        print('Se ha conectado con exito a la bd')
except:
    print('Error conectando a la bd')    


def get_engine():
    return engine
