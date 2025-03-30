from transformers import pipeline
import pandas as pd


classifier = pipeline("sentiment-analysis", model="michellejieli/emotion_text_classifier")
# print(classifier("I love this!"))

# Load the dataset
df = pd.read_csv("dataset/movies_subtitles.csv")
df = df.dropna()
df = df.drop_duplicates()

# Get all the ToyStory subtitles (imdb_id tt0114709)
df_toy_story = df[df["imdb_id"] == "tt0114709"]
df_toy_story = df_toy_story.drop(columns=["imdb_id"])

# Get all the instances and store in a list
instances = []
for index, row in df_toy_story.iterrows():
    instances.append(row["text"])

# Run sentiment analysis on the instances
sentiment_analysis = []
for instance in instances:
    sentiment = classifier(instance)
    sentiment_analysis.append((instance, sentiment[0]['label']))
    print(f"Instance: {instance}")
    print(f"Sentiment: {sentiment[0]['label']}")