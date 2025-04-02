import matplotlib.pyplot as plt
import seaborn as sns
import sys
import pandas as pd
from transformers import pipeline
import time
import ollama
from tag_extraction import extract_keywords, extract_keyword_from_text
from log_util import logger, separator, log_section, log_subsection

classifier = pipeline("sentiment-analysis", model="michellejieli/emotion_text_classifier")
ollama.Client(host="http://host.docker.internal:11434")

def store_movie_subtitle_files(id):
    logger.info(f"Storing movie subtitles for {id}")
    try:
        df = pd.read_csv("src/kurz/dataset/movies_subtitles.csv").dropna().drop_duplicates()
    except FileNotFoundError:
        logger.error("File not found. Please check the dataset path.")
        return

    df_movie = df[df["imdb_id"] == id].drop(columns=["imdb_id"])
    df_movie.to_csv(f"src/kurz/movies/{id}.csv", index=False)


def get_sentiment(text):
    """Classify the sentiment of a given text."""
    return classifier(text[:500])  # Adjust the text length if necessary

def get_max_emotion_score(sentiment):
    """Extract the max emotion score from sentiment analysis."""
    return max(
        [e for e in sentiment if e['label'] != 'neutral'],
        key=lambda e: e['score'],
        default={'score': 0}
    )['score']
    
def get_clip_strings(top_5_clips, start_time, end_time):
    # Initialize a list to store the result strings for the top 5 clips
    result_strings = []
    
    # Format the results for each of the top 5 clips
    for _, clip in top_5_clips.iterrows():
        result_string = (
            f"Best Clip: {clip['text']}\n"
            f"Start Time: {clip['start_time']}, End Time: {clip['end_time']}\n"
            f"Emotion: {clip['sentiment']}\n"
            f"Max Emotion Score: {clip['max_emotion_score']:.2f}\n"
            "-------------------------\n"
        )
        result_strings.append(result_string)

    # Combine the results into a final string
    final_result = (
        "------------------------------------------------------\n"
        "------------------------START------------------------\n"
        + ''.join(result_strings) +
        f"Sentiment analysis took {end_time - start_time:.2f} seconds.\n"
        "-------------------------END----------------------------\n"
        "--------------------------------------------------------"
    )
    return final_result

def analyze_movie_sentiments(id):
    log_section(f"Analyzing movie sentiment for {id}")
    window_size = "60s"

    # Read the data from the CSV file
    df = pd.read_csv(f"src/kurz/movies/{id}.csv")
    
    logger.debug("Reading movie subtitles...")
    try:
        df = pd.read_csv(f"src/kurz/movies/{id}.csv")
    except FileNotFoundError:
        logger.error(f"File not found for {id}. Please run store_movie_subtitle_files first.")
        return

    
    logger.debug("Preparing movie sentiment analysis...")
    
    # Convert start_time and end_time to timedelta
    df['start_time'] = pd.to_timedelta(df['start_time'], unit='s')
    df['end_time'] = pd.to_timedelta(df['end_time'], unit='s')

    # Sort the dataframe by start_time
    df = df.sort_values("start_time")
    df['window_start'] = (df['start_time'] // pd.Timedelta(window_size)) * pd.Timedelta(window_size)

    # Group by the window_start and aggregate the text
    df_clips = df.groupby('window_start').agg({
        'text': ' '.join,
        'start_time': 'first',
        'end_time': 'last'
    }).reset_index()
 
    logger.debug("Clipped movie sentiment analysis started")
    
    # Track sentiment analysis time
    start_time = time.time()

    # Get sentiment for each clip
    df_clips['sentiment'] = df_clips['text'].apply(get_sentiment)

    # Calculate max emotion score for each clip
    df_clips['max_emotion_score'] = df_clips['sentiment'].apply(get_max_emotion_score)

    # End the timer for sentiment analysis
    end_time = time.time()

    logger.debug("Sentiment analysis completed")
    
    df_clips['max_emotion_score'] = df_clips['sentiment'].apply(
    lambda x: max(
        [e for e in x if e['label'] != 'neutral'], 
        key=lambda e: e['score'], 
        default={'score': 0}
    )['score']
)
    
    best_clip = df_clips.loc[df_clips['max_emotion_score'].idxmax()]
    log_subsection("ANALYSIS RESULTS")
    logger.info(f"Best Clip: {best_clip['text']}")

    logger.info(f"Tags from Best Clip: {extract_keyword_from_text(best_clip['text'])}")
    
    logger.debug(f"Start Time: {best_clip['start_time']}, End Time: {best_clip['end_time']}")
    
    logger.info(f"Emotion: {best_clip['sentiment']}")

    elapsed_time = end_time - start_time
    logger.debug(f"Sentiment analysis took {elapsed_time:.2f} seconds.")

    # Get the top 5 clips based on max_emotion_score
    top_5_clips = df_clips.nlargest(5, 'max_emotion_score')

    return get_clip_strings(top_5_clips, start_time, end_time)


def ask_ollama(model='mistral', prompt='Hello!'):
    start_time = time.time()
    response = ollama.chat(model=model, messages=[{'role': 'user', 'content': prompt}])
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.debug(f"Ollama analysis took {elapsed_time:.2f} seconds.")
    return response

# movie_list = ["arristocats_subtitles", "forrest_gump_subtitles", "toy_story_subtitles"]
#, tt0076759, tt0117008, tt0055277, tt0067992, tt0120762
movie_list = ["pocahontas_subtitles"]
sentiment_list = []

for movie in movie_list:
    sentiment_list.append(analyze_movie_sentiments(movie))

#store_movie_subtitle_files("tt0114148")


ollama_base_prompt = (
    "Hello, I am conducting a sentiment analysis on the subtitles of the following movie."
    "Based on your knowledge on the movie and on movie reviews please select the movie clip that has the most intense emotion."
    "At the end, please select the id of the subtitle section"
    )
ollama_responses = []

for sentiment in sentiment_list:
    ollama_responses.append(ask_ollama(prompt=ollama_base_prompt + sentiment))
    
#extract_keywords("arristocats_subtitles")

with open("src/kurz/ollama_responses.txt", "w") as f:
    for i in range(len(movie_list)):
        f.write(f"Movie: {movie_list[i]}\n")
        f.write(ollama_responses[i].message['content'])
        f.write("\n\n")

sys.exit(0)