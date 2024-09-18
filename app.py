import pandas as pd
import operator
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import streamlit as st

import streamlit as st
from functions import (
    top_genres_by_playtime,
    top_5_games_by_playtime,
    bottom_3_games_by_playtime,
    similar_user_recs,
    get_recommendations_by_name
)

# Definición de la función para mostrar el dashboard
def dashboard():
    enlace_embebido = '''
    <iframe width="1366" height="768" src="https://app.powerbi.com/view?r=eyJrIjoiZmVjY2JiNGItYjM4OC00MTM4LWI2YjYtYjA5YzdiY2RhYjgwIiwidCI6Ijk2M2JjMjIzLTBjMDktNDk3MC05NTlmLTIyZjdjODFkZWYzNyIsImMiOjR9" frameborder="0" allowfullscreen></iframe>
    '''
    st.markdown(enlace_embebido, unsafe_allow_html=True)

# Título de la aplicación
st.title('Games Market Analysis')

# Selección de la función que el usuario desea usar
st.sidebar.title('Funciones')
option = st.sidebar.selectbox(
    'Selecciona una función:',
    [
        'Top Genres by Playtime',
        'Top 5 Games by Playtime',
        'Bottom 3 Games by Playtime',
        'Similar User Recommendations',
        'Game Recommendations by Name',
        'Ver Dashboard'
    ]
)

# Lógica para la función seleccionada
if option == 'Top Genres by Playtime':
    year = st.sidebar.number_input('Introduce el año de lanzamiento:', min_value=1900, max_value=2100, step=1)
    if st.sidebar.button('Obtener resultados'):
        result = top_genres_by_playtime(year)
        st.write(result)

elif option == 'Top 5 Games by Playtime':
    year = st.sidebar.number_input('Introduce el año de lanzamiento:', min_value=1900, max_value=2100, step=1)
    if st.sidebar.button('Obtener resultados'):
        result = top_5_games_by_playtime(year)
        st.write(result)

elif option == 'Bottom 3 Games by Playtime':
    year = st.sidebar.number_input('Introduce el año de lanzamiento:', min_value=1900, max_value=2100, step=1)
    if st.sidebar.button('Obtener resultados'):
        result = bottom_3_games_by_playtime(year)
        st.write(result)

elif option == 'Similar User Recommendations':
    user = st.sidebar.text_input('Introduce el nombre del usuario:')
    if st.sidebar.button('Obtener recomendaciones'):
        result = similar_user_recs(user)
        if isinstance(result, pd.DataFrame) and not result.empty:
            st.write('Recomendaciones basadas en usuarios similares:')
            st.write(result)

            # Seleccionar un ítem de las recomendaciones
            selected_item = st.selectbox('Selecciona un ítem para obtener recomendaciones adicionales:', result['Item_name'].tolist(), key='item_select')
            
            if selected_item:
                if st.button('Obtener recomendaciones por nombre del juego'):
                    game_recommendations = get_recommendations_by_name(selected_item)
                    st.write(f'Recomendaciones para el juego: {selected_item}')
                    st.write(game_recommendations)
        else:
            st.write(result)  # Mostrar mensaje de error si corresponde

elif option == 'Game Recommendations by Name':
    game_name = st.sidebar.text_input('Introduce el nombre del juego:')
    if st.sidebar.button('Obtener recomendaciones'):
        result = get_recommendations_by_name(game_name)
        st.write(result)

elif option == 'Ver Dashboard':
    dashboard()

# Para ejecutar el despliegue en Streamlit
# Utiliza el siguiente comando en la terminal:
# streamlit run app.py
