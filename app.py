import streamlit as st
import pickle
import pandas as pd
import requests
st.markdown("""
<style>

/* Recommend Button */
div.stButton > button:first-child {
    background-color: transparent;
    color: red;
    border: 2px solid red;
    border-radius: 10px;
    padding: 10px 24px;
    font-size: 18px;
    font-weight: bold;
    transition: 0.3s;
}

/* Hover Effect */
div.stButton > button:first-child:hover {
    color: white;
    border: 2px solid red;
}

/* Click Effect */
div.stButton > button:first-child:active {
    background-color: darkred;
    color: white;
    border: 2px solid white;
}

</style>
""", unsafe_allow_html=True)

# Fetch poster from TMDB
def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=1ec2ca5fbebb13f654157aaa9f5edc5f&language=en-US"

    response = requests.get(url)

    data = response.json()

    poster_path = data.get('poster_path')

    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster"


# Load movie dictionary
movies_dict = pickle.load(open('movies.dict.pkl', 'rb'))

# Convert to dataframe
movies_df = pd.DataFrame(movies_dict)

# Load similarity matrix
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Movie titles list
movies_list = movies_df['title'].tolist()


# Streamlit UI
st.title("Movie Recommender System")

selected_movie = st.selectbox(
    'Select a movie you like:',
    movies_list
)


# Recommendation function
def recommend(movie):

    # Get selected movie index
    movie_index = movies_df[movies_df['title'] == movie].index[0]

    # Get similarity scores
    distances = similarity[movie_index]

    # Sort movies based on similarity
    movies_sorted = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_sorted:

        # Correct TMDB movie id
        movie_id = movies_df.iloc[i[0]].movie_id

        # Append movie title
        recommended_movies.append(
            movies_df.iloc[i[0]].title
        )

        # Append poster
        recommended_movies_posters.append(
            fetch_poster(movie_id)
        )

    return recommended_movies, recommended_movies_posters
# Button
if st.button('Recommend'):

    recommended_movies, recommended_movies_posters = recommend(selected_movie)

    cols = st.columns(5)

    for idx, col in enumerate(cols):

        with col:

            # Movie Name on Top
            st.markdown(
                f"""
                <div style="
                    text-align:center;
                    color:white;
                    font-size:16px;
                    font-weight:300;
                    white-space:nowrap;
                    overflow:hidden;
                    text-overflow:ellipsis;
                    margin-bottom:8px;
                ">
                    {recommended_movies[idx]}
                </div>
                """,
                unsafe_allow_html=True
            )

            # Poster
            st.image(
                recommended_movies_posters[idx],
                use_container_width=True
            )