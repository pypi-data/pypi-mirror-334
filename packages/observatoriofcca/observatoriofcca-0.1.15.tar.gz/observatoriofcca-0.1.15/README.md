# Observatorio FCCA

## Observatorio de gestión pública e inteligencia de mercados


El objetivo de esta paquetería es proporcionar a la comunidad científica y académica, tanto Mexicana como extranjera, una función que pueda conectarse a las bases de datos del [Observatorio de Gestión Pública Inteligencia de Mercado (OGPIM)](https://sites.google.com/umich.mx/observatoriofcca/inicio?authuser=0), a efecto de descargar los precios históricos de granos, frutas y hortalizas recopilados por el Sistema Nacional de Información e integración de Mercados (SNIIM) de la Secretaría de Economía del Gobierno de la República Mexicana.

Esta función en Python es un resultado de los esfuerzos de investigación del [Dr. Oscar Valdemar De la Torre Torres](https://oscardelatorretorres.com) y de los trabajos de tesis doctoral dirigidos a Felipe Andoni Luna Campos y Rodolfo López. Esto con apoyo de beca a estos últimos dos por parte de la Secretaría ce ciencia, humanidades, Tecnología e Innovación (SECIHT).

De manera complementaria, esta aplicación se realizó con proyectos concurrentes patrocinados por la Coordinación de la Investigación de la Universidad Michoacana de San Nicolás de Hidalgo y el Instituto de Ciencia, Tecnología e Innovación del gobierno del estado de Michoacán.

El objetivo de la función es tener acceso sencillo, a través de Python, a los precios de estos bienes para fines de investigación tanto académica como de mercado.

Para acceder a la creación de su usuario y password, es necesario visitar el acceso a la base de datos del [OGPIM](https://app1.observatorio-fcca-umich.com/web/login) y enviar un correo a 1803672F@umich.mx.

Consulte aquí la [lista de productos y claves](https://app1.observatorio-fcca-umich.com/api/get_sniim_productos)


Ejemplo 1. Debe indicar el preduct_key y fecha (YYYY-MM-DD)

```
from observatoriofcca import sniimapp

username = 'USUARIO'   
password = 'PASSWORD'  

client = sniimapp.sniimapp_precios(username=username,password=password)

prices = client.get_sniim_precios(
    product_key="FH-CD42", date_start="2024-02-01", date_end="2024-04-10"
)

print(prices)

```

Ejemplo 2. Para convertir los datos a un Dataframe solo debe utilizar la libreria pandas como se muestra a continuación.

```
from observatoriofcca import sniimapp
import pandas as pd

username = 'USUARIO'
password = 'PASSWORD'

client = sniimapp.sniimapp_precios(username=username,password=password)

prices = client.get_sniim_precios(
    product_key="G-FCO", date_start="2024-02-01", date_end="2024-04-10"
)

for key, val in prices.items():
    if isinstance(val, list) and all(isinstance(item,dict) for item in val):
        df = pd.DataFrame(val)
print(df)
```
