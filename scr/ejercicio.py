import pandas as pd
import numpy as np
import seaborn as sns

import plotly
from plotnine import *
from plotnine.data import *

ejercicio = pd.read_csv("ejercicio.csv",
                        encoding="latin1",
                        delimiter=';')

#Eliminamos las filas problemáticas
ejercicio.drop(ejercicio.index[13943:], inplace=True)

#Recodificamos las columnas de interés
ejercicio.replace("Desapruebo mucho", -2, inplace=True)
ejercicio.replace("Desapruebo", -1, inplace=True)
ejercicio.replace("No sé", 0, inplace=True)
ejercicio.replace("Apruebo", 1, inplace=True)
ejercicio.replace("Apruebo mucho", 2, inplace=True)
ejercicio.replace("Muy Mala", -2, inplace=True)
ejercicio.replace("Mala", -1, inplace=True)
ejercicio.replace("NO LO CONOZCO", 0, inplace=True)
ejercicio.replace("NO LA CONOZCO", 0, inplace=True)
ejercicio.replace("Buena", 1, inplace=True)
ejercicio.replace("Muy Buena", 2, inplace=True)
ejercicio.replace("Algo probable", 0, inplace=True)
ejercicio.replace("Nada probable", -1, inplace=True)
ejercicio.replace("Muy probable", 2, inplace=True)

#Armamos una pivot con la columna que divide a la encuesta por semanas con la intención de voto 2021 y lo promediamos
pivot = ejercicio.pivot_table(index='analisis_temporal', 
                        columns='intencion_voto_2021', 
                        values='peso',
                        fill_value=0,
                        aggfunc='sum')

pivot = pivot.apply(lambda x: x/sum(x),axis=1)
pivot

#Luego desarmamos la pivot para poder graficarla
graph1 = pivot.melt(
    var_name=['Partido'],
    value_name='intencion_voto',  
    ignore_index=False
    ).reset_index()

graph1.head(2)

#Realizamos el primer gráfico
gf1 = (
    ggplot(
        graph1, 
        aes(x='analisis_temporal', y='intencion_voto',group='Partido')
    )
    + geom_point(aes(fill='Partido'))
    + geom_line(aes(color='Partido'))
    + theme_minimal()
    + theme(axis_text_x = element_text(angle = 90))
    + xlab("Tiempo")
    + ylab("Itención de Voto")
    + labs(title='Evolución de la intención de voto entre semanas')
    
)
gf1

#Realizamos una matriz con las columnas de interés con el objetivo de calcular la correlación entre las variables seleccionadas
matriz = ejercicio[['opinion_gestion_alberto', 
                   'opinion_tolosapaz',
                   'opinion_manes',
                   'opinion_santilli',
                   'posibilidad_voto_santilli',
                   'posibilidad_voto_manes',
                    'posibilidad_voto_tolosapaz',
                   ]]

matriz.rename({'opinion_gestion_alberto': '1_opinion_gestion_alberto',
               'opinion_tolosapaz': '2_opinion_tolosapaz',
                'opinion_manes': '3_opinion_manes',
                'opinion_santilli': '4_opinion_santilli',
                'posibilidad_voto_santilli': '5_posibilidad_voto_santilli',
                'posibilidad_voto_manes': '6_posibilidad_voto_manes',
                'posibilidad_voto_tolosapaz': '7_posibilidad_voto_tolosapaz'},
                 axis=1, 
                 inplace=True)
correlation = matriz.corr()

#Luego desarmamos la matriz para realizar el segundo gráfico
graph2 = correlation.melt(
    var_name=['opinion'],
    value_name='correlacion',  
    ignore_index=False
    ).reset_index()

graph2 = graph2.astype({"correlacion": "float"}).round(2)
graph2.head(2)

#Realizamos el segundo gráfico
rename = ['opinion_gestion_alberto', 
                   'opinion_tolosapaz',
                   'opinion_manes',
                   'opinion_santilli',
                   'posibilidad_voto_santilli',
                   'posibilidad_voto_manes',
                    'posibilidad_voto_tolosapaz']

gf2 = (
    ggplot(
        graph2, 
        aes(x='index', y='opinion', fill='correlacion')
    )
    + geom_tile(aes(width=.95, height=.95))
    + geom_text(aes(label='correlacion'), size=10)
    + theme_minimal()
    + theme(axis_text_x = element_text(angle = 90))
    + scale_x_discrete(labels= rename)
    + scale_y_discrete(labels= rename)
    + xlab(" ")
    + ylab(" ")
    + labs(title='Correlación entre la opinión de la gestión presidencial y la intención de voto')
)   
gf2

#Armamos una segunda pivot con las variables de interés para el tercer gráfico y calculamos el porcentaje
pivot2 = ejercicio.pivot_table(index='voto_emitido_2019', 
                        columns='intencion_voto_2021', 
                        values='peso',
                        fill_value=0,
                        aggfunc='sum')

pivot2 = pivot2.apply(lambda x: x/sum(x)*100,axis=1)
pivot2

#Luego desarmamos la pivot para poder hacer el tercer gráfico
graph3 = pivot2.melt(
    var_name=['intencion_voto_2021'],
    value_name='%votos',  
    ignore_index=False
    ).reset_index()

graph3 = graph3.astype({"%votos": "float"}).round(1)
graph3 = graph3.iloc[8:]

#Hacemos el tercer gráfico
gf3 = (
       ggplot(
        graph3, 
        aes(y='voto_emitido_2019', x='intencion_voto_2021',fill='%votos')
        )
    + geom_tile(aes(width=.95, height=.95))
    + geom_text(aes(label='%votos'), size=10)
    + theme_minimal()
    + theme(axis_text_x = element_text(angle = 90))
    #+ scale_x_discrete(labels= rename)
    #+ scale_y_discrete(labels= rename)
    #+ xlab(" ")
    #+ ylab(" ")
    + labs(title='Transferencia de voto entre eleccion 2019-2021')
)  
gf3
