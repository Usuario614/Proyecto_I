import os
from fastapi import FastAPI
import pandas as pd

# Obtiene la ruta del directorio actual del script
dir_path = os.path.dirname(os.path.realpath(__file__))

# Define las rutas relativas a los archivos
reviews_file = os.path.join(dir_path, 'df_user_reviews_desanidada_final.csv')
items_file = os.path.join(dir_path, 'df_final_sample.parquet')
steam_file = os.path.join(dir_path, 'steam_games_final.csv')

# Carga los archivos usando las rutas relativas
df_reviews = pd.read_csv(reviews_file, encoding='latin-1')
df_items = pd.read_parquet(items_file)
df_steam = pd.read_csv(steam_file, encoding='latin-1')

app = FastAPI()


@app.get('/PlayTimeGenre/{genero}')
def PlayTimeGenre(genero: str):
    # Filtra los juegos del género específico
    juegos_genero = df_steam[df_steam['genres'].str.contains(genero, case=False, na=False)]

    if juegos_genero.empty:
        return {"Año de lanzamiento con más horas jugadas para el género": "No se encontraron juegos"}

    # Une con los DataFrames de reviews y user items
    df_merged = pd.merge(juegos_genero, df_items, on='item_id')
    df_merged = pd.merge(df_reviews, df_merged, on='item_id')

    # Calcula el año con más horas jugadas
    año_con_mas_horas = df_merged.groupby('year')['playtime_forever'].sum().idxmax()

    return {"Año de lanzamiento con más horas jugadas para el género": año_con_mas_horas}


@app.get('/UserForGenre/{genero}')
def UserForGenre(genero: str):
    # Filtra los juegos del género específico
    juegos_genero = df_steam[df_steam['genres'].str.contains(genero, case=False, na=False)]

    if juegos_genero.empty:
        return {"Usuario con más horas jugadas para Género": "No se encontraron juegos"}

    # Une con los DataFrames de reviews y user items
    df_merged = pd.merge(juegos_genero, df_items, on='item_id')
    df_merged = pd.merge(df_reviews, df_merged, on='item_id')

    # Filtra los usuarios que han jugado juegos de ese género
    usuarios_genero = df_merged['user_id'].unique()

    if not usuarios_genero:
        return {"Usuario con más horas jugadas para Género": "No se encontraron usuarios"}

    # Encuentra el usuario con más horas jugadas para ese género
    usuario_con_mas_horas = ""
    horas_acumuladas_por_año = []

    for usuario in usuarios_genero:
        df_usuario = df_merged[df_merged['user_id'] == usuario]
        horas_por_año = df_usuario.groupby('year')['playtime_forever'].sum()

        if not horas_por_año.empty:
            horas_totales = horas_por_año.sum()

            if horas_totales > 0 and (usuario_con_mas_horas == "" or horas_totales > horas_acumuladas_por_año[0]['Horas']):
                usuario_con_mas_horas = usuario
                horas_acumuladas_por_año = [{"Año": año, "Horas": horas} for año, horas in horas_por_año.items()]

    if usuario_con_mas_horas == "":
        return {"Usuario con más horas jugadas para Género": "No se encontraron horas jugadas"}

    return {"Usuario con más horas jugadas para Género": usuario_con_mas_horas, "Horas jugadas": horas_acumuladas_por_año}


@app.get('/UsersRecommend/{año}')
def UsersRecommend(año: int):
    # Filtra las reviews para el año específico y con recomendaciones positivas o neutrales
    reviews_filtradas = df_reviews[(df_reviews['posted'].dt.year == año) & (df_reviews['sentiment_analysis'] >= 0)]

    if reviews_filtradas.empty:
        return {"Top 3 juegos más recomendados para el año": "No se encontraron reviews"}

    # Agrupa por item_id y cuenta las recomendaciones
    juegos_recomendados = reviews_filtradas[reviews_filtradas['recommend'] == 1].groupby('item_id')['recommend'].count().reset_index()

    if juegos_recomendados.empty:
        return {"Top 3 juegos más recomendados para el año": "No se encontraron juegos recomendados"}

    # Ordena los juegos por cantidad de recomendaciones en orden descendente
    juegos_recomendados = juegos_recomendados.sort_values(by='recommend', ascending=False)

    # Toma los 3 juegos más recomendados
    top_3_juegos = juegos_recomendados.head(3)

    # Obtiene los nombres de los juegos
    nombres_juegos = df_steam[df_steam['id'].isin(top_3_juegos['item_id'])]['app_name']

    resultado = [{"Puesto 1": nombres_juegos.iloc[0]}, {"Puesto 2": nombres_juegos.iloc[1]}, {"Puesto 3": nombres_juegos.iloc[2]}]

    return {"Top 3 juegos más recomendados para el año": resultado}


@app.get('/UsersNotRecommend/{año}')
def UsersNotRecommend(año: int):
    # Filtra las reviews para el año específico y con recomendaciones negativas
    reviews_filtradas = df_reviews[(df_reviews['posted'].dt.year == año) & (df_reviews['recommend'] == 0) & (df_reviews['sentiment_analysis'] < 0)]

    if reviews_filtradas.empty:
        return {"Top 3 juegos menos recomendados para el año": "No se encontraron reviews"}

    # Agrupa por item_id y cuenta las recomendaciones negativas
    juegos_no_recomendados = reviews_filtradas.groupby('item_id')['recommend'].count().reset_index()

    if juegos_no_recomendados.empty:
        return {"Top 3 juegos menos recomendados para el año": "No se encontraron juegos no recomendados"}

    # Ordena los juegos por cantidad de recomendaciones negativas en orden descendente
    juegos_no_recomendados = juegos_no_recomendados.sort_values(by='recommend', ascending=False)

    # Toma los 3 juegos menos recomendados
    top_3_juegos = juegos_no_recomendados.head(3)

    # Obtiene los nombres de los juegos
    nombres_juegos = df_steam[df_steam['id'].isin(top_3_juegos['item_id'])]['app_name']

    resultado = [{"Puesto 1": nombres_juegos.iloc[0]}, {"Puesto 2": nombres_juegos.iloc[1]}, {"Puesto 3": nombres_juegos.iloc[2]}]

    return {"Top 3 juegos menos recomendados para el año": resultado}


@app.get('/sentiment_analysis/{año}')
def sentiment_analysis(año: int):
    # Filtra las reseñas para el año específico
    reviews_año = df_reviews[df_reviews['posted'].dt.year == año]

    if reviews_año.empty:
        return {"Análisis de sentimiento para el año": "No se encontraron reseñas para el año"}

    # Cuenta la cantidad de registros de reseñas con análisis de sentimiento
    cantidad_negative = (reviews_año['sentiment_analysis'] < 0).sum()
    cantidad_neutral = (reviews_año['sentiment_analysis'] == 0).sum()
    cantidad_positive = (reviews_año['sentiment_analysis'] > 0).sum()

    resultado = {"Negative": cantidad_negative, "Neutral": cantidad_neutral, "Positive": cantidad_positive}

    return {"Análisis de sentimiento para el año": resultado}


# Definimos la ruta y método para la recomendación de juegos por ítem
@app.get('/recomendacion_juego/{id_juego}')
def recomendacion_juego(id_juego: int):
    # Obtenemos el índice del juego de entrada
    idx = df_steam[df_steam['id'] == id_juego].index[0]

    # Obtenemos la similitud del juego de entrada con todos los demás juegos
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Ordenamos los juegos por similitud en orden descendente
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Obtenemos los índices de los juegos recomendados (excluyendo el juego de entrada)
    top_indices = [i for i, _ in sim_scores[1:6]]

    # Obtenemos los nombres de los juegos recomendados
    recommended_games = df_steam['game_name'].iloc[top_indices]

    return {"juegos_recomendados": recommended_games.tolist()}
