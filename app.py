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
    <iframe title="Games_Analytics" width="600" height="373.5" src="https://app.fabric.microsoft.com/view?r=eyJrIjoiZjg4ZjA5YjEtY2Q4Ny00ZDY0LTlkM2QtYjFjM2I1YzU5M2ZkIiwidCI6IjM0NGY1NzYyLWEzMGItNGNiMC05MWYyLTFhYTJjMzEwOTk0ZCIsImMiOjR9&pageName=3470fe379c94d0319def" frameborder="0" allowFullScreen="true"></iframe>
    '''
    st.markdown(enlace_embebido, unsafe_allow_html=True)

# Título de la aplicación
st.title('Games Market Analysis')

# Selección de la función que el usuario desea usar
st.sidebar.title('Sinergy Data Solutions')
option = st.sidebar.selectbox(
    'Selecciona una función:',
    [
        'Top Genres by Playtime',
        'Top 5 Games by Playtime',
        'Bottom 3 Games by Playtime',
        'Game Recommendations by Name',
        'Similar User Recommendations',
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


elif option == 'Game Recommendations by Name':
    game_name = st.sidebar.text_input('Introduce el nombre del juego:')
    if st.sidebar.button('Obtener recomendaciones'):
        result = get_recommendations_by_name(game_name)
        st.write(result)


elif option == 'Similar User Recommendations':
    user = st.sidebar.text_input('Introduce el nombre del usuario:')
    if st.sidebar.button('Obtener recomendaciones'):
        result = similar_user_recs(user)
        st.write('Recomendaciones basadas en usuarios similares:')
        st.write(result)

        # Guardar el resultado en session_state
        st.session_state.similar_recs = result

    # Mostrar el selectbox solo si hay recomendaciones
    if 'similar_recs' in st.session_state:
        selected_item = st.selectbox('Selecciona un ítem para obtener recomendaciones adicionales:', st.session_state.similar_recs['Item_name'].tolist(), key='item_select') 
        if st.button('Obtener recomendaciones por nombre del juego'):
            # Obtener recomendaciones basadas en el ítem seleccionado
            game_recommendations = get_recommendations_by_name(selected_item)
            st.write(game_recommendations)

            # Guardar las nuevas recomendaciones en session_state
            st.session_state.current_recommendations = game_recommendations

    # Mostrar un selectbox para las recomendaciones actuales si existen
    if 'current_recommendations' in st.session_state:
        selected_game = st.selectbox('Selecciona un ítem de las recomendaciones:', st.session_state.current_recommendations['Item_name'].tolist(), key='game_select')
        if st.button('Obtener más recomendaciones'):
            # Obtener más recomendaciones basadas en el ítem seleccionado
            more_recommendations = get_recommendations_by_name(selected_game)
            st.write(more_recommendations)

            # Actualizar las recomendaciones actuales
            st.session_state.current_recommendations = more_recommendations




elif option == 'Ver Dashboard':
    dashboard()

# Para ejecutar el despliegue en Streamlit
# Utiliza el siguiente comando en la terminal:
# streamlit run app.py

