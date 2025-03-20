# Observatorio FCCA

## Observatorio de gestión pública e inteligencia de mercados


El objetivo de esta paquetería es proporcionar a la comunidad científica y académica, tanto Mexicana como extranjera, una función que pueda conectarse a las bases de datos del [Observatorio de Gestión Pública Inteligencia de Mercado (OGPIM)](https://sites.google.com/umich.mx/observatoriofcca/inicio?authuser=0), a efecto de descargar los precios históricos de granos, frutas y hortalizas recopilados por el Sistema Nacional de Información e integración de Mercados (SNIIM) de la Secretaría de Economía del Gobierno de la República Mexicana.

Esta función en Python es un resultado de los esfuerzos de investigación del [Dr. Oscar Valdemar De la Torre Torres](https://oscardelatorretorres.com) y de los trabajos de tesis doctoral dirigidos a Rodolfo Adrian López Torres y Felipa Andoni Luna Campos. Esto con apoyo de beca a estos últimos dos por parte de la Secretaría ce ciencia, humanidades, Tecnología e Innovación (SECIHT).

De manera complementaria, esta aplicación se realizó con proyectos concurrentes patrocinados por la Coordinación de la Investigación de la Universidad Michoacana de San Nicolás de Hidalgo y el Instituto de Ciencia, Tecnología e Innovación del gobierno del estado de Michoacán.

El objetivo de la función es tener acceso sencillo, a través de Python, a los precios de estos bienes para fines de investigación tanto académica como de mercado.

Para acceder a la creación de su usuario y password, es necesario visitar el acceso a la base de datos del [OGPIM](https://app1.observatorio-fcca-umich.com/web/login).

[Lista de productos y claves](https://app1.observatorio-fcca-umich.com/api/get_sniim_productos)

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
