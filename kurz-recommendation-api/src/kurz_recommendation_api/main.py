from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import uvicorn
import random
from keybert import KeyBERT

movies_list = [
    "tt0114709",
    "tt0113189",
    "tt0114148",
    "tt0112442",
    "tt0076759",
    "tt0109830",
    "tt0117008",
    "tt0055277",
    "tt0067992",
    "tt0065421"
]

seen_movies = []

movies_df = pd.read_csv("src/dataset/movies_meta.csv")
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
    # Get the movies info from the CSV file
    movie_info = movies_df[movies_df['imdb_id'] == movie_id]

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
    doc = get_movie_info(movie_id)["overview"]

    return kw_model.extract_keywords(doc, keyphrase_ngram_range=(1, 2), stop_words=None)

def get_recommendation():
    pass

@app.get("/api/recommendation")
def recommendation():
    if len(seen_movies) == 0:
        # pick a random movie from the list
        movie_id = random.choice(movies_list)
        seen_movies.append(movie_id)
        return get_keywords(movie_id)

    return get_recommendation()

def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("src.kurz_recommendation_api.main:app", host="0.0.0.0", port=8000, reload=True)