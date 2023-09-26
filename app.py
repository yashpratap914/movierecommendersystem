import streamlit as st
import pickle
import pandas as pd
import requests

# Apply custom styling with HTML/CSS

st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQUSkHGzZdjC5ZmP9k694FXwRDPctXvoKu_OWC0gag1&s');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        margin: 0;
        padding: 0;
        
    }
    
    .ezrtsby2{
     background-color : gray;
     color:white; 
    }
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 20px;
        background-color: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(5px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    }
    .navbar-brand {
        font-size: 50px;
        font-weight: bold;
        color: red;
        position: absolute;
        top: -144px;
    }
    }
    .navbar-links {
        display: flex;
        left: 625px;
        top: -157px;
        
    }
    .navbar-link {
        color: white;
        text-decoration: none;
        font-weight: bold;
        margin-right: 20px; /* Add some spacing between links */
        
    }
    .movie-title-frame {
        border-top: 1px solid rgba(255, 255, 255, 0.2);
        margin: 20px 0;
        padding-top: 20px;
    }
    .recommend-button {
        background-color: #3366cc;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .header{
        color: blue;
        font-weight:bold;
        font-size: 40px;
        top:15px;
    }
    .movie-container {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.1);
    }
    .movie-title {
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .movie-description {
        margin-bottom: 10px;
    }
    .movie-trailer {
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ...

# Streamlit app layout
st.markdown('<div class="navbar">', unsafe_allow_html=True)
st.markdown('<div class="movie-title-frame">', unsafe_allow_html=True)
st.markdown('<div class="navbar-brand">MOVIREC</div>', unsafe_allow_html=True)
st.markdown('<div class="navbar-links">', unsafe_allow_html=True)
# Add navigation links or buttons here
# st.markdown('<a class="navbar-link" href="#about">About</a>', unsafe_allow_html=True)
# st.markdown('<a class="navbar-link" href="#contact">Contact</a>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


st.markdown('<p class="header">Discover Your Next Movie!</p>', unsafe_allow_html=True)


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
    'CHOOSE YOUR MOVIE:',
    movies['title'].values)
if st.button('Recommend'):
    names,posters,descriptions,trailers = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
        st.write(descriptions[0])
        st.video(trailers[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])
        st.write(descriptions[1])
        st.video(trailers[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
        st.write(descriptions[2])
        st.video(trailers[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
        st.write(descriptions[3])
        st.video(trailers[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
        st.write(descriptions[4])
        st.video(trailers[4])
