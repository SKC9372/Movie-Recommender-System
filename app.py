from flask import Flask,render_template,url_for
from forms import InputForm
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import pickle
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = 'my secret key'

with open('movie_name.pkl','rb') as f:
    dictionary = pickle.load(f)

movies = pd.DataFrame(dictionary)


def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=81ebc86b93b25ccf118174d9a1c39b28&language=en-US'
    response = requests.get(url)
    response = response.json()
    poster_path = response['poster_path']
    full_path = 'http://image.tmdb.org/t/p/w500' + poster_path
    return full_path



def recommend_movies(title):

    # Get the embedding of the target movie
    target_embedding = movies[movies['original_title'] == title]['embedding'].values[0].reshape(1, -1)
    
    # Calculate cosine similarities between the target and all other movies
    similarities = cosine_similarity(target_embedding, np.vstack(movies['embedding'].values)).flatten()
    
    # Add similarities to the DataFrame and sort by similarity scores
    movies_copy = movies.copy()
    movies_copy['similarity'] = similarities
    recommendations = movies_copy.sort_values(by='similarity', ascending=False)[['original_title','similarity','id']].head(11)
    
    # Exclude the target movie itself from the recommendations
    recommendations = recommendations[recommendations['original_title'] != title]

     # Generate a list of dictionaries with title and poster_url for each recommendation
    recommended_movies = [
        {"title": row['original_title'], "poster_url": fetch_poster(row['id'])}
        for _, row in recommendations.iterrows()
    ]
    
    return recommended_movies

@app.route('/',methods = ['GET','POST'])
def home():
    form = InputForm()
    recommendations = []
    if form.validate_on_submit():
        selected_movies = form.movies.data

        recommendations = recommend_movies(selected_movies)
    
    return render_template('recommend.html',form = form,recommendations = recommendations)



if __name__ == '__main__':
    app.run(debug=True)