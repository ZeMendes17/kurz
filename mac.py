import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from transformers import pipeline


# Load sentiment analysis model
classifier = pipeline("sentiment-analysis", model="michellejieli/emotion_text_classifier") #top_k=None



# Filter Toy Story subtitles




# # Extract instances
# instances = df_toy_story["text"].tolist()

# # Perform sentiment analysis
# sentiment_analysis = []
# for i, instance in enumerate(instances):
#     sentiment = classifier(instance)[0]['label']
#     sentiment_analysis.append((i, sentiment))

# # Convert to DataFrame
# sentiment_df = pd.DataFrame(sentiment_analysis, columns=["Index", "Sentiment"])

# # Assign numerical values to sentiments
# sentiment_map = {
#     "anger": -1.5,
#     "disgust": -1,
#     "fear": -0.5,
#     "sadness": 0,
#     "neutral": 0.5,
#     "surprise": 1,
#     "joy": 1.5,

# }
# sentiment_df["Sentiment Score"] = sentiment_df["Sentiment"].map(sentiment_map)

# # Plot sentiment over time
# plt.figure(figsize=(12, 6))
# sns.lineplot(data=sentiment_df, x="Index", y="Sentiment Score", marker="o")

# plt.title("Sentiment Analysis Across Toy Story Subtitles")
# plt.xlabel("Dialogue Index (Ordered)")
# plt.ylabel("Sentiment Score")
# plt.axhline(0, color="gray", linestyle="--")  # Neutral line
# plt.show()


def store_movie_subtitle_files():
    df = pd.read_csv("dataset/movies_subtitles.csv").dropna().drop_duplicates()

    df_toy_story = df[df["imdb_id"] == "tt0114709"].drop(columns=["imdb_id"])
    df_toy_story.to_csv("movies/toy_story_subtitles.csv", index=False)

    df_forrest_gump = df[df["imdb_id"] == "tt0109830"].drop(columns=["imdb_id"])
    df_forrest_gump.to_csv("movies/forrest_gump_subtitles.csv", index=False)

    df_the_aristocats = df[df["imdb_id"] == "tt0065421"].drop(columns=["imdb_id"])
    df_the_aristocats.to_csv("movies/arristocats_subtitles.csv", index=False)


def analyze_toy_story_sentiments():
    window_size="60s"

    df = pd.read_csv("movies/toy_story_subtitles.csv")

    df['start_time'] = pd.to_timedelta(df['start_time'], unit='s')
    df['end_time'] = pd.to_timedelta(df['end_time'], unit='s')

    df = df.sort_values("start_time")  # Ensure chronological order
    df['window_start'] = (df['start_time'] // pd.Timedelta(window_size)) * pd.Timedelta(window_size)

    df_clips = df.groupby('window_start').agg({
        'text': ' '.join,  # Concatenate subtitles within the window
        'start_time': 'first',  # Keep the first timestamp in the window
        'end_time': 'last'  # Keep the last timestamp in the window
    }).reset_index()

    df_clips['sentiment'] = df_clips['text'].apply(lambda text: classifier(text[:500]))

    df_clips['max_emotion_score'] = df_clips['sentiment'].apply(
    lambda x: max(
        [e for e in x if e['label'] != 'neutral'],  # Exclude "neutral"
        key=lambda e: e['score'],  # Pick highest score from remaining emotions
        default={'score': 0}  # Default in case all emotions are "neutral"
    )['score']
)
    
    best_clip = df_clips.loc[df_clips['max_emotion_score'].idxmax()]

    print(f"Best Clip: {best_clip['text']}")
    
    print(f"Start Time: {best_clip['start_time']}, End Time: {best_clip['end_time']}")
    
    print(f"Emotion: {best_clip['sentiment']}")



analyze_toy_story_sentiments()


