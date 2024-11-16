from flask import Flask, render_template, url_for
from forms import InputForm
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import pickle
import requests
import os
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my secret key'

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load the movies data
if not os.path.exists('movie_name.pkl'):
    raise FileNotFoundError("movie_name.pkl file is missing. Make sure it is included in the deployment.")

with open('movie_name.pkl', 'rb') as f:
    dictionary = pickle.load(f)

movies = pd.DataFrame(dictionary)

# Caching for poster URLs
poster_cache = {}

def log_memory():
    import psutil
    process = psutil.Process(os.getpid())
    memory_usage = process.memory_info().rss / 1024 / 1024  # Convert to MB
    logging.info(f"Memory usage: {memory_usage:.2f} MB")

def fetch_poster(movie_id):
    if movie_id in poster_cache:
        return poster_cache[movie_id]

    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=81ebc86b93b25ccf118174d9a1c39b28&language=en-US'
    try:
        response = requests.get(url)
        response.raise_for_status()
        poster_path = response.json().get('poster_path', '')
        full_path = 'http://image.tmdb.org/t/p/w500' + poster_path if poster_path else None
        poster_cache[movie_id] = full_path
        return full_path
    except Exception as e:
        logging.error(f"Error fetching poster for movie_id {movie_id}: {e}")
        return None

def recommend_movies(title):
    log_memory()

    # Get the embedding of the target movie
    target_embedding = movies[movies['original_title'] == title]['embedding'].values[0].reshape(1, -1)

    # Calculate cosine similarities between the target and all other movies
    similarities = cosine_similarity(target_embedding, np.vstack(movies['embedding'].values)).flatten()

    # Add similarities to the DataFrame and sort by similarity scores
    movies['similarity'] = similarities
    recommendations = movies.sort_values(by='similarity', ascending=False)[['original_title', 'similarity', 'id']].head(11)

    # Exclude the target movie itself from the recommendations
    recommendations = recommendations[recommendations['original_title'] != title]

    # Generate a list of dictionaries with title and poster_url for each recommendation
    recommended_movies = [
        {"title": row['original_title'], "poster_url": fetch_poster(row['id'])}
        for _, row in recommendations.iterrows()
    ]

    log_memory()
    return recommended_movies

@app.route('/', methods=['GET', 'POST'])
def home():
    form = InputForm()
    recommendations = []
    if form.validate_on_submit():
        selected_movies = form.movies.data
        recommendations = recommend_movies(selected_movies)
    return render_template('recommend.html', form=form, recommendations=recommendations)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if $PORT is not set
    app.run(host="0.0.0.0", port=port, debug=False)
