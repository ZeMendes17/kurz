import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from transformers import pipeline

# Load sentiment analysis model
classifier = pipeline("sentiment-analysis", model="michellejieli/emotion_text_classifier") #top_k=None

# Load and clean dataset
df = pd.read_csv("src/kurz/dataset/movies_subtitles.csv").dropna().drop_duplicates()

# Filter Toy Story subtitles
df_toy_story = df[df["imdb_id"] == "tt0114709"].drop(columns=["imdb_id"])

# Extract instances
instances = df_toy_story["text"].tolist()

# Perform sentiment analysis
sentiment_analysis = []
for i, instance in enumerate(instances):
    sentiment = classifier(instance)[0]['label']
    sentiment_analysis.append((i, sentiment))

# Convert to DataFrame
sentiment_df = pd.DataFrame(sentiment_analysis, columns=["Index", "Sentiment"])

# Assign numerical values to sentiments
sentiment_map = {
    "anger": -1.5,
    "disgust": -1,
    "fear": -0.5,
    "sadness": 0,
    "neutral": 0.5,
    "surprise": 1,
    "joy": 1.5,

}
sentiment_df["Sentiment Score"] = sentiment_df["Sentiment"].map(sentiment_map)

# Plot sentiment over time
plt.figure(figsize=(12, 6))
sns.lineplot(data=sentiment_df, x="Index", y="Sentiment Score", marker="o")

plt.title("Sentiment Analysis Across Toy Story Subtitles")
plt.xlabel("Dialogue Index (Ordered)")
plt.ylabel("Sentiment Score")
plt.axhline(0, color="gray", linestyle="--")  # Neutral line
plt.show()
