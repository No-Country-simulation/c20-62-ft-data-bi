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
    <iframe title="Games_Analytics" width="600" height="373.5" src="https://app.fabric.microsoft.com/view?r=eyJrIjoiZjg4ZjA5YjEtY2Q4Ny00ZDY0LTlkM2QtYjFjM2I1YzU5M2ZkIiwidCI6IjM0NGY1NzYyLWEzMGItNGNiMC05MWYyLTFhYTJjMzEwOTk0ZCIsImMiOjR9" frameborder="0" allowFullScreen="true"></iframe>
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
        
        if isinstance(result, pd.DataFrame) and not result.empty:
            st.write('Recomendaciones basadas en usuarios similares:')
            st.write(result)

            # Seleccionar un ítem de las recomendaciones
            selected_item = st.selectbox(
                'Selecciona un ítem para obtener recomendaciones adicionales:',
                result['Item_name'].unique().tolist(),  # Usamos unique() para evitar duplicados
                key='item_select'
            )

            # Verifica si hay un ítem seleccionado
            if selected_item:
                # Usamos session_state para almacenar el ítem seleccionado
                st.session_state.selected_item = selected_item

                # Verifica si ya hay un ítem seleccionado en la sesión y el botón es presionado
                if st.button('Obtener recomendaciones por nombre del juego', key='recommend_button'):
                    game_recommendations = get_recommendations_by_name(st.session_state.selected_item)
                    
                    # Verifica que la función de recomendaciones devuelva un DataFrame válido
                    if isinstance(game_recommendations, pd.DataFrame) and not game_recommendations.empty:
                        st.write(f'Recomendaciones para el juego: {st.session_state.selected_item}')
                        st.write(game_recommendations)
                    else:
                        st.write(f'No se encontraron recomendaciones para {st.session_state.selected_item}.')
        else:
            st.write('No se encontraron recomendaciones para este usuario.')


elif option == 'Ver Dashboard':
    dashboard()

# Para ejecutar el despliegue en Streamlit
# Utiliza el siguiente comando en la terminal:
# 
