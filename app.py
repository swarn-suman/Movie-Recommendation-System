import pickle
import streamlit as st
import requests
import pandas as pd

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=69bc002110586f7b4c0c0e7683a97418&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

st.header('Movie Recommender System')
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, posters = recommend(selected_movie)
    num_columns = 5
    num_recommendations = len(recommended_movie_names)
    num_rows = (num_recommendations + num_columns - 1) // num_columns
    columns = st.columns(num_columns)

    recommendation_index = 0
    for row in range(num_rows):
        for col in range(num_columns):
            if recommendation_index < num_recommendations:
                with columns[col]:
                    st.header(recommended_movie_names[recommendation_index])
                    st.image(posters[recommendation_index])
                recommendation_index += 1
