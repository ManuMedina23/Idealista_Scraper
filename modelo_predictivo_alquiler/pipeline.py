import pandas as pd
import numpy as np
from ast import literal_eval
import re
import sqlalchemy as sa
import db_connection as dbcon

def match_property(property, patterns):
    for pat in patterns:
        match_prop = re.search(pat, property)
        if match_prop:
            return True
    return False        

def check_property(property, patterns):
    for pat in patterns:
        check = re.search(pat, property)
        if check:
            return 1
    return 0        

def get_number(property):
    nums = re.findall(r'\d', property)
    if len(nums) == 2:
        return int(nums[0] + nums[1])
    else:
        return int(nums[0])
    
def get_ascensor(features):
    for prop in features:
        if match_property(prop.lower().strip(), ['ascensor']):
            return(check_property(prop.lower().strip(), ['con']))    
        
def get_baños(features):
    for prop in features:
        if match_property(prop.lower().strip(), ['baño']):
            return(get_number(prop.lower().strip()))

def get_año(features):
    for prop in features:
        if match_property(prop.lower().strip(), ['construido en']):
            return(get_number(prop.lower().strip()))

def get_trastero(features):
    value = 0
    for prop in features:
        if match_property(prop.lower().strip(), ['trastero']):
            value +=1
    return(value)

def get_orientacion(features):
    for prop in features:
        if match_property(prop.lower().strip(), ['orientacion']):
            return(prop.split(' ', maxsplit=1)[1].strip().split(', ')[0])                        

def get_piso(features):
    for prop in features:
        if match_property(prop.lower().strip(), ['bajo','planta','interior','exterior']):
            return(prop)

def get_habitaciones(features):
    for prop in features:
        if match_property(prop.lower().strip(), ['habitaci']):
            try:
                habitaciones = get_number(prop.lower().strip())
            except:
                habitaciones = prop
            return(habitaciones)

def get_metros_reales(features):
    for prop in features:
        if match_property(prop.lower().strip(), ['m²']):
            try:
                metros = get_number(prop.lower().strip().split(',')[0])
            except:
                metros = prop
            return(metros)    
                            
def get_condicion(features):
    for prop in features:
        if match_property(prop.lower().strip(), ['segunda mano', 'promocion de obra nueva']):
            return(prop)

def get_armario_empotrado(features):
    value = 0
    for prop in features:
        if match_property(prop.lower().strip(), ['armarios empotrados']):
            value +=1
    return(value)                

def get_terraza(features):
    value = 0
    for prop in features:
        if match_property(prop.lower().strip(), ['terraza']):
            value +=1
    return(value)   

def get_balcon(features):
    value = 0
    for prop in features:
        if match_property(prop.lower().strip(), ['balcon']):
            value +=1
    return(value)          

def get_jardin(features):
    value = 0
    for prop in features:
        if match_property(prop.lower().strip(), ['jardin']):
            value +=1
    return(value)

def get_garaje(features):
    value = 0
    for prop in features:
        if match_property(prop.lower().strip(), ['garaje']):
            value +=1
    return(value)

def get_calefaccion(features):
    value = 0
    for prop in features:
        if match_property(prop.lower().strip(), ['calefacción']):
            value +=1
    return(value)

def get_aire_acon(features):
    value = 0
    for prop in features:
        if match_property(prop.lower().strip(), ['aire acondicionado']):
            value +=1
    return(value)

def get_piscina(features):
    value = 0
    for prop in features:
        if match_property(prop.lower().strip(), ['piscina']):
            value +=1
    return(value)

def get_zonas_verdes(features):
    value = 0
    for prop in features:
        if match_property(prop.lower().strip(), ['zonas verdes']):
            value +=1
    return(value)

def process_piso(serie):
    lista = serie.split()
    mapeo = ''
    if ((lista[0] == 'Bajo') | (lista[0] == 'Entreplanta') | (lista[0] == 'Exterior')):
        mapeo = 'Bajo'
    elif lista[0] == 'Planta':
        try:           
            if int(lista[1][0]) < 4:
                mapeo = 'Primeros_pisos'
            else:
                mapeo = 'Ultimos_pisos'
        #Excepcion que ocurre con aquellos que incluyen un signo antes del número,         
        except ValueError:
            if int(lista[1][1]) < 4:
                mapeo = 'Primeros_pisos'
            else:
                mapeo = 'Ultimos_pisos'              
    else:
        mapeo = 'Muchas_plantas'
    return(mapeo)    

#Leer CSV con los datos
df = pd.read_csv('casas_idealista2.csv', 
                 sep=';', 
                 encoding='utf-16', 
                 converters={'caracteristicas_basicas': literal_eval, 
                             'caracteristicas_extras': literal_eval})

#Añadir columnas con los datos procesados
df['ascensor'] = df.caracteristicas_basicas.apply(get_ascensor)
df['baños'] = df.caracteristicas_basicas.apply(get_baños)
df['año'] = df.caracteristicas_basicas.apply(get_año)
df['trastero'] = df.caracteristicas_basicas.apply(get_trastero)
df['orientacion'] = df.caracteristicas_basicas.apply(get_orientacion)
df['piso'] = df.caracteristicas_basicas.apply(get_piso)
df['habitaciones'] = df.caracteristicas_basicas.apply(get_habitaciones)
df['metros_reales'] = df.caracteristicas_basicas.apply(get_metros_reales)
df['condicion'] = df.caracteristicas_basicas.apply(get_condicion)
df['armarios_empotrados'] = df.caracteristicas_basicas.apply(get_armario_empotrado)
df['terraza'] = df.caracteristicas_basicas.apply(get_terraza)
df['balcon'] = df.caracteristicas_basicas.apply(get_balcon)
df['jardin'] = df.caracteristicas_basicas.apply(get_jardin)
df['garaje'] = df.caracteristicas_basicas.apply(get_garaje)
df['calefaccion'] = df.caracteristicas_basicas.apply(get_calefaccion)
df['aire_acondicionado'] = df.caracteristicas_extras.apply(get_aire_acon)
df['piscina'] = df.caracteristicas_extras.apply(get_piscina)
df['zonas_verdes'] = df.caracteristicas_extras.apply(get_zonas_verdes)

#Borras columnas de caracteristicas basicas y extras, ya no son necesarias
df.drop(columns = ['caracteristicas_basicas', 'caracteristicas_extras'], inplace = True)
print(df.head(5))


#Procesado de datos basados en el EDA
df = df[df.precio < 2700] #Quitar outlier
df.loc[df['ascensor'].isna(), 'ascensor'] = 0 #Reemplazar NA del ascensor por 0
df = df[~df.piso.isna()] #Como el dataframe no es reciente y quizas no existan los anuncios se eliminan aquellos sin el dato piso
df.piso = df.piso.apply(process_piso) #Se procesa el numero del piso para categorizarlo
df.loc[df.habitaciones == 'Sin habitación', 'habitaciones'] = 1 #Aquellos sin habitación se cambian por 1, se supone que al menos 1  hay
df.drop(columns = ['balcon','jardin','año','orientacion','condicion'], inplace=True) #Se eliminan la columnas balcon, jardin, año y orientacion porque no aportan apenas informacion

df.to_csv('idealista_machine_learning.csv', index = False)
try:
    columnas_creadas = df.to_sql('casas_granada', con=dbcon.engine) 
    print(columnas_creadas)
except AttributeError:
    print(AttributeError)
except ValueError:
    pass    

