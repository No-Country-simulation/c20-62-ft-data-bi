# Importaciones
import pandas as pd
import operator
import warnings
import pandas as pd
import operator
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import streamlit as st
warnings.filterwarnings("ignore")


#Load data

genres_playtime = pd.read_parquet('Data/funciones1.parquet')
games_playtime = pd.read_parquet('Data/funciones2.parquet')
df_mod_game = pd.read_parquet('Data/df_mod_game.parquet')
game_sim_df = pd.read_parquet('Data/game_sim.parquet')
df_mf = pd.read_parquet('Data/models.parquet')
umatrix_norm = pd.read_parquet('Data/umatrix_norm.parquet')
user_sim_df = pd.read_parquet('Data/user_sim.parquet')





def top_genres_by_playtime(release_year):
    """
    This function returns the top 5 genres with the highest playtime hours for a given release year.

    Parameters:
    release_year (int or float): The release year to filter the data. The function ensures that the input is a number.

    Returns:
    - A DataFrame containing the top 5 genres and their corresponding playtime hours if data for the year exists.
    - If no valid data is found for the provided year, a dictionary with an appropriate message is returned.

    Notes:
    - The function checks if the input is numeric. If not, it returns an error message.
    - It also checks if the provided year is present in the DataFrame. If not, it returns a message indicating the absence of data for that year.
    """
    # Ensure the parameter is a number
    if not isinstance(release_year, (int, float)):
        return {"Invalid input. Please provide a numeric year.": None}
    
    # Ensure that the 'Release' column is treated as a numeric type for comparison
    genres_playtime['Release'] = pd.to_numeric(genres_playtime['Release'], errors='coerce')
    
    # Check if the year is in the DataFrame
    if release_year not in genres_playtime['Release'].unique():
        return {f"There is no data available for the year {release_year}": None}
    
    # Filter the DataFrame by the release year
    genres_playtime_filtered = genres_playtime[genres_playtime['Release'] == release_year]

    # Check if the filtered DataFrame is empty
    if genres_playtime_filtered.empty:
        return {f"No data available for year {release_year}": None}
    
    # Group by genre and sum the playtime hours
    genres_playtime_grouped = genres_playtime_filtered.groupby('Genres')['Playtime_Millon_Hours'].sum().reset_index()

    # Sort by playtime hours in descending order
    genres_playtime_sorted = genres_playtime_grouped.sort_values(by='Playtime_Millon_Hours', ascending=False)

    # Get the top 5 genres
    top_5_genres = genres_playtime_sorted.head(5)

    return top_5_genres





def top_5_games_by_playtime(release_year):
    """
    This function returns the top 5 games with the highest playtime hours for a given release year.

    Parameters:
    release_year (int): The release year to filter the data.

    Returns:
    - A DataFrame containing the top 5 game names and their corresponding playtime hours for the specified year.
    - If the input is not a number or the year is not in the DataFrame, it returns an appropriate message.
    """
    # Ensure the parameter is a number
    if not isinstance(release_year, (int, float)):
        return {"Invalid input. Please provide a numeric year.": None}
    
    # Ensure 'Release' column is numeric
    games_playtime['Release'] = pd.to_numeric(games_playtime['Release'], errors='coerce')

    # Check if the year is in the DataFrame
    if release_year not in games_playtime['Release'].unique():
        return {f"There is no data available for the year {release_year}": None}
    
    # Filter the DataFrame by the release year
    games_filtered = games_playtime[games_playtime['Release'] == release_year]

    # Check if the filtered DataFrame is empty
    if games_filtered.empty:
        return {f"No data available for year {release_year}": None}
    
    # Sort by playtime in descending order and get the top 5
    top_5_games = games_filtered.sort_values(by='Playtime', ascending=False).head(5)

    # Return only the game name and playtime
    return top_5_games[['Item_name', 'Playtime']]




def bottom_3_games_by_playtime(release_year):
    """
    This function returns the 3 games with the lowest playtime hours (greater than 0) for a given release year.

    Parameters:
    release_year (int): The release year to filter the data.

    Returns:
    - A DataFrame containing the 3 game names with the lowest playtime hours greater than 0 for the specified year.
    - If the input is not a number or the year is not in the DataFrame, it returns an appropriate message.
    """
    # Ensure the parameter is a number
    if not isinstance(release_year, (int, float)):
        return {"Invalid input. Please provide a numeric year.": None}
    
    # Ensure 'Release' column is numeric
    games_playtime['Release'] = pd.to_numeric(games_playtime['Release'], errors='coerce')

    # Check if the year is in the DataFrame
    if release_year not in games_playtime['Release'].unique():
        return {f"There is no data available for the year {release_year}": None}
    
    # Filter the DataFrame by the release year and playtime > 0
    games_filtered = games_playtime[(games_playtime['Release'] == release_year) & (games_playtime['Playtime'] > 0)]

    # Check if the filtered DataFrame is empty
    if games_filtered.empty:
        return {f"No data available for year {release_year} with playtime greater than 0": None}
    
    # Sort by playtime in ascending order and get the bottom 3
    bottom_3_games = games_filtered.sort_values(by='Playtime', ascending=True).head(3)

    # Return only the game name and playtime
    return bottom_3_games[['Item_name', 'Playtime']]



def similar_user_recs(user: str):
    '''
    Generates a list of the most recommended items for a user, based on ratings from similar users.
    
    Arguments:
        user (str): The name or identifier of the user for whom you want to generate recommendations.
        
    Returns:
        DataFrame: A DataFrame with columns Item_name, Genres, Rating, and Ranking, representing
                   the top 5 recommended items based on the ratings of similar users.
    '''
    if user not in umatrix_norm.columns:
        return f'No data available on user {user}'
    
    sim_users = user_sim_df.sort_values(by=user, ascending=False).index[1:11]
    
    best = []
    most_common = {}
    
    for i in sim_users:
        max_score = umatrix_norm.loc[:, i].max()
        best.extend(umatrix_norm[umatrix_norm.loc[:, i] == max_score].index.tolist())
    
    for j in best:
        most_common[j] = most_common.get(j, 0) + 1
    
    sorted_list = sorted(most_common.items(), key=operator.itemgetter(1), reverse=True)
    
    top_items = [item[0] for item in sorted_list[:5]]
    
    filtered_df = df_mf[df_mf['Item_name'].isin(top_items)]
    
    recommendations_df = filtered_df[['Item_name', 'Genres', 'Rating', 'Ranking']].drop_duplicates().reset_index(drop=True)

    # Return the DataFrame for Streamlit to display
    return recommendations_df



def get_recommendations_by_name(item_name):
    """
    Returns the top 5 recommended games similar to the given game name, along with their information.
    Generates a wordcloud based on the reviews of the selected game.
    
    Parameters:
    - item_name (str): The name of the game for which recommendations are to be generated.
    
    Returns:
    - A DataFrame containing the recommended games with columns: Item_name, Genres, Rating, and average Ranking.
    - A wordcloud based on the reviews of the selected game.
    """
    item_name = item_name.lower()

    if item_name not in df_mf['Item_name'].str.lower().values:
        return f"No recommendations available for the game '{item_name}'."

    selected_game_name = df_mf[df_mf['Item_name'].str.lower() == item_name]['Item_name'].iloc[0]

    if selected_game_name not in game_sim_df.index:
        return f"No recommendations available for the game '{item_name}'."

    game_row = game_sim_df.loc[selected_game_name]

    similar_games = game_sim_df.dot(game_row).sort_values(ascending=False)
    similar_games = similar_games.drop(selected_game_name)

    recommended_games = similar_games.nlargest(5).index.tolist()

    recommendations_df = df_mf[df_mf['Item_name'].isin(recommended_games)]
    recommendations_df = recommendations_df[['Item_name', 'Genres', 'Rating', 'Ranking']].drop_duplicates().reset_index(drop=True)

    reviews = df_mf[df_mf['Item_name'] == selected_game_name]['Review'].dropna().tolist()

    if reviews:
        review_text = ' '.join(reviews)
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(review_text)

        # Convert the wordcloud to an image and display it in Streamlit
        buffer = io.BytesIO()
        wordcloud.to_image().save(buffer, format="PNG")
        st.image(buffer.getvalue(), caption=f'Wordcloud for {selected_game_name}')

    # Return the DataFrame for Streamlit to display
    return recommendations_df
