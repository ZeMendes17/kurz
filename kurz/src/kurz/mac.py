import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from transformers import pipeline
import time


classifier = pipeline("sentiment-analysis", model="michellejieli/emotion_text_classifier")

def store_movie_subtitle_files(id):
    df = pd.read_csv("dataset/movies_subtitles.csv").dropna().drop_duplicates()

    df_movie = df[df["imdb_id"] == id].drop(columns=["imdb_id"])
    df_movie.to_csv(f"movies/{id}.csv", index=False)


def analyze_movie_sentiments(id):
    window_size="60s"

    df = pd.read_csv(f"movies/{id}.csv")

    df['start_time'] = pd.to_timedelta(df['start_time'], unit='s')
    df['end_time'] = pd.to_timedelta(df['end_time'], unit='s')

    df = df.sort_values("start_time")
    df['window_start'] = (df['start_time'] // pd.Timedelta(window_size)) * pd.Timedelta(window_size)

    df_clips = df.groupby('window_start').agg({
        'text': ' '.join,
        'start_time': 'first',
        'end_time': 'last'
    }).reset_index()

    start_time = time.time()

    df_clips['sentiment'] = df_clips['text'].apply(lambda text: classifier(text[:500]))

    end_time = time.time()

    df_clips['max_emotion_score'] = df_clips['sentiment'].apply(
    lambda x: max(
        [e for e in x if e['label'] != 'neutral'], 
        key=lambda e: e['score'], 
        default={'score': 0}
    )['score']
)
    
    best_clip = df_clips.loc[df_clips['max_emotion_score'].idxmax()]
    print("------------------------------------------------------")
    print("------------------------START------------------------")
    print(f"Best Clip: {best_clip['text']}")
    
    print(f"Start Time: {best_clip['start_time']}, End Time: {best_clip['end_time']}")
    
    print(f"Emotion: {best_clip['sentiment']}")

    elapsed_time = end_time - start_time
    print(f"Sentiment analysis took {elapsed_time:.2f} seconds.")

    print("-------------------------END----------------------------")
    print("--------------------------------------------------------")



analyze_movie_sentiments("arristocats_subtitles")

analyze_movie_sentiments("forrest_gump_subtitles")

analyze_movie_sentiments("golden_eye_subtitles")

analyze_movie_sentiments("toy_story_subtitles")

#store_movie_subtitle_files()


