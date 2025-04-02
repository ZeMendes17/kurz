from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import uvicorn
import random
from keybert import KeyBERT
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Predefined movie list
movies_list = [
    "tt0114709", "tt0113189", "tt0114148", "tt0112442", "tt0076759",
    "tt0109830", "tt0117008", "tt0120783", "tt0067992", "tt0065421"
]

seen_movies = []
liked_movies = []

# Load dataset and filter to only include movies from the list
movies_df = pd.read_csv("src/dataset/movies_meta.csv")
filtered_df = movies_df[movies_df['imdb_id'].isin(movies_list)].copy().reset_index(drop=True)
filtered_df['overview'] = filtered_df['overview'].fillna('')  # Handle missing overviews

# Initialize TF-IDF Vectorizer with filtered movies
tfidf = TfidfVectorizer(stop_words='english')
overview_matrix = tfidf.fit_transform(filtered_df['overview'])

# KeyBERT model for keyword extraction
kw_model = KeyBERT()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_movie_info(movie_id):
    movie_info = filtered_df[filtered_df['imdb_id'] == movie_id]
    if not movie_info.empty:
        movie_info = movie_info.iloc[0]
        return {
            "imdb_id": movie_info["imdb_id"],
            "title": movie_info["original_title"],
            "genres": movie_info["genres"].split(","),
            "overview": movie_info["overview"]
        }
    return None

def get_keywords(movie_id):
    movie_info = get_movie_info(movie_id)
    if not movie_info:
        return []
    doc = movie_info["overview"]
    return kw_model.extract_keywords(doc, keyphrase_ngram_range=(1, 2), stop_words=None)

def get_recommendation():
    if not liked_movies:
        return None
    
    # Get indices of liked movies in filtered_df
    liked_indices = []
    for movie_id in liked_movies:
        movie_idx = filtered_df.index[filtered_df['imdb_id'] == movie_id].tolist()
        if movie_idx:
            liked_indices.append(movie_idx[0])
    
    if not liked_indices:
        return None
    
    # Calculate average vector of liked movies
    liked_vectors = overview_matrix[liked_indices]
    avg_vector = np.mean(liked_vectors.toarray(), axis=0).reshape(1, -1)
    
    # Compute cosine similarities
    similarities = cosine_similarity(avg_vector, overview_matrix).flatten()
    
    # Sort movies by similarity
    sorted_indices = np.argsort(similarities)[::-1]
    
    # Find the first movie not seen or already liked
    for idx in sorted_indices:
        candidate_id = filtered_df.iloc[idx]['imdb_id']
        if candidate_id not in seen_movies and candidate_id not in liked_movies:
            return candidate_id
    
    return None

@app.post("/api/like/{movie_id}")
def like_movie(movie_id: str):
    if movie_id not in movies_list:
        return {"error": "Movie not in available list"}, 404
    if movie_id not in liked_movies:
        liked_movies.append(movie_id)
    return {"message": "Movie liked successfully"}

@app.get("/api/recommendation")
def recommendation():
    available_movies = [m for m in movies_list if m not in seen_movies]
    
    if not available_movies:
        return {"error": "No movies available"}
    
    if not liked_movies:
        movie_id = random.choice(available_movies)
        seen_movies.append(movie_id)
        return {
            "movie": get_movie_info(movie_id),
            "keywords": get_keywords(movie_id)
        }
    
    # Get content-based recommendation
    movie_id = get_recommendation()
    
    # Fallback to random if no recommendations found
    if not movie_id:
        movie_id = random.choice(available_movies)
    
    seen_movies.append(movie_id)
    return {
        "movie": get_movie_info(movie_id),
        "keywords": get_keywords(movie_id)
    }

@app.get("/api/reset")
def reset():
    """Reset the state of the recommendation system"""
    global seen_movies, liked_movies
    seen_movies = []
    liked_movies = []
    return {"message": "State reset successfully"}

def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("src.kurz_recommendation_api.main:app", host="0.0.0.0", port=8000, reload=True)