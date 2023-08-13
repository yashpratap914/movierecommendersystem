import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_movie_trailer(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key=8265bd1679663a7ea12ac168da84d2e8')
    data = response.json()
    trailers = [item for item in data['results'] if item['site'] == 'YouTube']
    if trailers:
        return f"https://www.youtube.com/watch?v={trailers[0]['key']}"
    return None

def fetch_movie_details(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US')
    data = response.json()
    return data['overview']

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{'
                 '}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = response.json()

    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    recommended_movies_descriptions =[]
    recommended_movies_trailers = []
    for i in movies_list:
        movie_id =  movies.iloc[i[0]].movie_id
        #name of movie
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from api
        recommended_movies_posters.append(fetch_poster(movie_id))
        # fetch description from API
        recommended_movies_descriptions.append(fetch_movie_details(movie_id))
        # fetch trailer URL from API
        recommended_movies_trailers.append(fetch_movie_trailer(movie_id))
    return  recommended_movies, recommended_movies_posters, recommended_movies_descriptions, recommended_movies_trailers

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))
st.title('Movie Recommender System')
selected_movie_name = st.selectbox(
    'Give some movie here',
    movies['title'].values)
if st.button('Recommend'):
    names,posters,descriptions,trailers = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
        st.write(descriptions[0])
        st.write(trailers[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
        st.write(descriptions[1])
        st.write(trailers[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
        st.write(descriptions[2])
        st.write(trailers[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
        st.write(descriptions[3])
        st.write(trailers[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
        st.write(descriptions[4])
        st.write(trailers[4])
