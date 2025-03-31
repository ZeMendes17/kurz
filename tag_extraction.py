import pandas as pd
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer

# # Sentence Transformers Model (Used in KeyBERT)
model = SentenceTransformer("all-mpnet-base-v2")
kw_model = KeyBERT(model)

def extract_keywords(id):
    df = pd.read_csv(f"movies/{id}.csv")

    df['start_time'] = pd.to_timedelta(df['start_time'], unit='s')
    df['end_time'] = pd.to_timedelta(df['end_time'], unit='s')

    df = df.sort_values("start_time")
    df['window_start'] = (df['start_time'] // pd.Timedelta("60s")) * pd.Timedelta("60s")

    df_clips = df.groupby('window_start').agg({
        'text': ' '.join,
        'start_time': 'first',
        'end_time': 'last'
    }).reset_index()

    clip_scores = []

    for i, row in df_clips.iterrows():
        keywords = kw_model.extract_keywords(
            row['text'],
            keyphrase_ngram_range=(1, 3), # This specifies the range of n-grams to consider for keyword extraction. (1, 3) means unigrams, bigrams, and trigrams.
            use_mmr=True, # Maximal Marginal Relevance (MMR) is a method to select keywords that balance relevance and diversity.
            diversity=0.8, # This parameter controls the diversity of the keywords extracted. A higher value means more diverse keywords.
            top_n=5, # This specifies the number of keywords to extract.
            stop_words="english" # This filters out common English stop words (e.g., “the”, “is”, “in”, “on”, etc.) which are not meaningful for keyword extraction.
        )
        print(f"Clip {i}: {keywords}")

        # Compute clip score (sum of keyword relevance scores)
        score = sum([score for _, score in keywords])

        # Store clip data with score
        clip_scores.append({
            "clip_index": i,
            "start_time": row['start_time'],
            "end_time": row['end_time'],
            "keywords": keywords,
            "score": score
        })

    top_clips = sorted(clip_scores, key=lambda x: x["score"], reverse=True)[:3]

    # Print top 3 clips
    print("\nTop 3 Clips:")
    for clip in top_clips:
        print(f"Clip {clip['clip_index']} ({clip['start_time']} - {clip['end_time']}):")
        print(f"Keywords: {clip['keywords']}")
        print(f"Score: {clip['score']}\n")