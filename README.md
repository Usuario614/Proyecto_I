# Proyecto_I
Primer proyecto individual para #SoyHenry
Proyecto Individual Nº1
Rol: MLOps Engineer

MLOps: Machine Learning Operations

Descripción del Proyecto
Este proyecto se centra en la creación de un sistema de recomendación de videojuegos para usuarios de la plataforma Steam. El sistema se basa en datos recopilados a lo largo de los años y se desarrolla en el contexto de operaciones de Machine Learning (MLOps).

ETL (Extracción, Transformación y Carga)
La data se compone de tres tablas JSON comprimidas: steam_games.json.gz, user_reviews.json.gz, y user_items.json.gz. Estas tablas presentan datos anidados, valores nulos, duplicados y columnas repetidas. El proceso ETL incluye las siguientes etapas:

Conversión de los archivos JSON a DataFrames en Python.
Desanidación de columnas de interés, eliminación de columnas innecesarias y registros nulos y duplicados.
Corrección del formato de campos.
Creación de la variable sentiment_analysis en la tabla user_reviews, esencial para el modelo de recomendación.
Conversión de las tablas steam_games y user_reviews a formato CSV, y de la tabla user_items a formato Parquet debido a su gran tamaño.
EDA (Análisis Exploratorio de Datos)
Se realiza un análisis exploratorio de datos para identificar posibles relaciones entre variables y comportamientos que guiarán la construcción del modelo final. 

Desarrollo de la API
El proyecto propone la creación de seis funciones con sus respectivos endpoints para ser consumidos a través de una API. La API se desarrolla utilizando el framework FastAPI.

Modelo de Machine Learning
Una vez desarrollada la API, se procede a construir el modelo de recomendación más adecuado para los usuarios de Steam. Se presentan dos modelos:

1. Modelo Ítem-Ítem (Modelo seleccionado)
Este modelo se basa en la relación entre ítems, es decir, toma un juego de referencia y, en función de su similitud con otros juegos, recomienda títulos similares. El input es un juego y el output es una lista de cinco juegos recomendados.

2. Modelo Usuario-Ítem
El segundo enfoque se basa en el filtrado usuario-ítem. Aquí, se parte de un usuario, se identifican usuarios similares y se recomiendan juegos que han gustado a esos usuarios similares. El input es un usuario y el output es una lista de cinco juegos recomendados para ese usuario.

Conclusión
Este proyecto abarca todo el ciclo de procesamiento de datos, análisis, desarrollo de una API y creación de modelos de recomendación de videojuegos. Los modelos de recomendación ofrecen una experiencia personalizada a los usuarios y pueden aplicarse en un contexto real en una plataforma de juegos como Steam. La API proporciona una interfaz amigable para interactuar con el sistema de recomendación y obtener sugerencias de juegos.


Link API https://six61144.onrender.com/docs
#Video Youtube 
