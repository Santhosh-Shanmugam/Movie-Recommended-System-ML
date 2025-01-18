import streamlit as st
import pandas as pd
import requests
import pickle

# Load movie data
with open('data.pkl', 'rb') as file:
    movies, cosine_sim = pickle.load(file)

def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  
    movie_indices = [i[0] for i in sim_scores]
    return movies.iloc[movie_indices]

def fetch_poster(movie_id):
    api_key = 'bbec780a2b184df99f28bbc1aa520691'
    url = f'http://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
    return full_path

st.title("Movie Recommendation System")

selected_movie = st.selectbox("Select a movie", movies['title'].values)

if st.button('Recommend'):
    recommendations = get_recommendations(selected_movie)
    st.write("Top 10 Movies to Watch")

    for i in range(0, 10, 5):
        cols = st.columns(5)
        for col, j in zip(cols, range(i, i + 5)):
            if j < len(recommendations):
                movie_title = recommendations.iloc[j]['title']
                movie_id = recommendations.iloc[j]['movie_id']  
                poster_url = fetch_poster(movie_id)
                with col: 
                    st.image(poster_url, width=130)
                    st.write(movie_title)

#Function to display top 5 movies by genre
def display_genre_movies(genre, title):
    st.write(f"Top 5 {title} Movies")
    genre_movies = movies[movies['tags'].apply(lambda x: genre in x)].head(5)
    cols = st.columns(5)
    for col, movie in zip(cols, genre_movies.itertuples()):
        poster_url = fetch_poster(movie.movie_id)
        with col:
            st.image(poster_url, width=130)
            st.write(movie.title)

#Display top 5 Action movies
display_genre_movies('action', 'Action')

#Display top 5 Adventure movies
display_genre_movies('adventure', 'Adventure')

#Display top 5 Comedy movies
display_genre_movies('comedy', 'Comedy')

#Display top 5 Drama movies
display_genre_movies('drama', 'Drama')

#Display top 5 Other Genre movies (except those above section of Movies)
other_genres = movies[~movies['tags'].apply(lambda x: 'action' in x or 'adventure' in x)].head(5)
st.write("Top 5 Other Genre Movies")
cols = st.columns(5)
for col, movie in zip(cols, other_genres.itertuples()):
    poster_url = fetch_poster(movie.movie_id)
    with col:
        st.image(poster_url, width=130)
        st.write(movie.title)
