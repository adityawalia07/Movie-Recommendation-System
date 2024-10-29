import pickle
import streamlit as st
import requests
from datetime import datetime

# Configure Streamlit page
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS with enhanced styling
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 1rem;
        margin: 0 auto;
    }

    /* Header styling with animated gradient */
    .stHeader {
        background: linear-gradient(-45deg, #1a1a1a, #2d2d2d, #3d1a1a, #2d1a2d);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    @keyframes gradient {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }

    /* Title styling */
    h1 {
        color: #ffffff;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        text-align: center;
        margin-bottom: 0.5rem !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }

    /* Selectbox styling */
    .stSelectbox {
        background-color: #ffffff;
        border-radius: 8px;
        margin-bottom: 1rem;
    }

    /* Button styling with pulse animation */
    .stButton > button {
        background: linear-gradient(90deg, #ff4b6e, #ff6b6b);
        color: white;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
        margin-bottom: 1.5rem;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(255, 75, 110, 0.4);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(255, 75, 110, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(255, 75, 110, 0);
        }
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(255, 75, 110, 0.2);
        animation: none;
    }

    /* Movie title styling with animated reveal */
    .movie-title {
        font-size: 1rem;
        font-weight: 600;
        color: #ffffff !important;
        text-align: center;
        margin-top: 0.5rem;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
        opacity: 0;
        animation: fadeIn 0.5s ease forwards;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Column styling */
    div[data-testid="column"] {
        text-align: center;
        padding: 0.5rem;
    }

    /* Image styling with hover effect */
    img {
        border-radius: 8px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    img:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }

    /* Loading animation styling */
    .stSpinner > div {
        border-color: #ff4b6e !important;
    }

    /* Custom badge styling */
    .badge {
        background: rgba(255, 75, 110, 0.1);
        color: #ffffff;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin-top: 0.5rem;
        display: inline-block;
        backdrop-filter: blur(5px);
    }
    </style>
""", unsafe_allow_html=True)


# Caching for better performance
@st.cache_data(ttl=3600)
def fetch_movie_details(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=9062682b2658292d1e661e8a80ace4fe&language=en-US"
        data = requests.get(url, timeout=5).json()

        # Get movie details
        poster_path = data.get('poster_path')
        poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else None
        release_date = data.get('release_date', '')
        rating = data.get('vote_average', 0)
        overview = data.get('overview', 'No overview available.')
        runtime = data.get('runtime', 0)
        genres = ", ".join([genre['name'] for genre in data.get('genres', [])])

        # Fetch cast and director information
        credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=9062682b2658292d1e661e8a80ace4fe&language=en-US"
        credits_data = requests.get(credits_url, timeout=5).json()

        cast = [f"{member['name']} as {member['character']}" for member in credits_data.get('cast', [])[:5]]
        director = next((crew['name'] for crew in credits_data.get('crew', []) if crew['job'] == 'Director'), 'N/A')

        return {
            "poster_url": poster_url,
            "release_date": release_date,
            "rating": rating,
            "overview": overview,
            "runtime": runtime,
            "genres": genres,
            "cast": cast,
            "director": director
        }
    except:
        return None


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommendations = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title
        details = fetch_movie_details(movie_id)

        if details and details["poster_url"]:
            recommendations.append({
                'title': title,
                'poster': details["poster_url"],
                'year': details["release_date"][:4] if details["release_date"] else 'N/A',
                'rating': details["rating"],
                'similarity': round(i[1] * 100, 1)
            })

    return recommendations


# Load data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# App header with current date
current_year = datetime.now().year
st.markdown('<div class="stHeader">', unsafe_allow_html=True)
st.title('🎬 Movie Recommender')
st.markdown('<p style="color: white; text-align: center;">Discover your next favorite movie</p>',
            unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Movie selection with counter
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "🔍 Search from our collection of " + str(len(movie_list)) + " movies",
    movie_list,
    help="Type or select a movie from the dropdown"
)

# Fetch and display details for the selected movie
selected_movie_info = movies[movies['title'] == selected_movie].iloc[0]
selected_movie_details = fetch_movie_details(selected_movie_info.movie_id)

# Display selected movie details
st.markdown("### Selected Movie")
if selected_movie_details:
    col1, col2 = st.columns([1, 2])

    with col1:
        if selected_movie_details["poster_url"]:
            st.image(selected_movie_details["poster_url"], width=150)
        else:
            st.write("Poster not available")

    with col2:
        st.markdown(f"**Enter the world of {selected_movie}**")
        st.markdown(f"📅 {selected_movie_details['release_date'][:4]}")
        st.markdown(f"⏱️ {selected_movie_details['runtime']} min")
        st.markdown(f"⭐ {selected_movie_details['rating']}/10")
        st.markdown(selected_movie_details["genres"])
        st.markdown(f"**Overview**: {selected_movie_details['overview']}")
        st.markdown(f"**Director**: {selected_movie_details['director']}")
        st.markdown("**Cast**: " + " • ".join(selected_movie_details["cast"]))

# Recommendation button
if st.button('🎯 Get Recommendations'):
    with st.spinner('🎬 Finding perfect movies for you...'):
        recommendations = recommend(selected_movie)
        cols = st.columns(5)

        # Display recommendations in columns
        for col, movie in zip(cols, recommendations):
            with col:
                st.image(movie['poster'], width=150)
                st.markdown(f'<p class="movie-title">{movie["title"]}</p>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="badge">{movie["year"]} | ⭐ {movie["rating"]}/10</div>',
                    unsafe_allow_html=True
                )
                st.markdown(
                    f'<div class="badge tooltip" data-tooltip="Similarity Score">🎯 {movie["similarity"]}%</div>',
                    unsafe_allow_html=True
                )

# Footer with dynamic year
st.markdown(f"""
    <div style="text-align: center; margin-top: 2rem; padding: 1rem; color: #ffffff;">
        <p>Made with ❤️ for movie lovers | © {current_year}</p>
    </div>
""", unsafe_allow_html=True)
