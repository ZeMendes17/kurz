# Movie Sentiment Analysis and Clip Extraction

This project performs sentiment analysis on movie subtitles and provides a way to extract clips based on the analyzed sentiments. It uses a pre-trained sentiment analysis model to classify emotions in subtitles and visualizes the sentiment trends over time.

## Features

- **Sentiment Analysis**: Analyzes subtitles to classify emotions such as joy, sadness, anger, etc.
- **Visualization**: Plots sentiment scores over time to show emotional trends in the movie.
- **Clip Extraction**: Enables identification of specific scenes or clips based on sentiment.

## Technologies Used

- **Python**: Core programming language.
- **Transformers**: For sentiment analysis using the `michellejieli/emotion_text_classifier` model.
- **Pandas**: For data manipulation and analysis.
- **Matplotlib & Seaborn**: For data visualization.
- **MoviePy**: (Planned) For extracting video clips based on sentiment.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ZeMendes17/kurz.git
   ```

2. Run Docker Compose
   ```bash
   docker compose up --build
   ```

3. Ensure you have the subtitle dataset (both .csv files) in the `dataset/` folder inside `kurz/src/kurz` and `kurz-recommendation-api/src/`. The dataset should include a CSV file with subtitles and their corresponding movie IDs. The dataset is: `https://www.kaggle.com/datasets/adiamaan/movie-subtitle-dataset`.

## Example Output

- A line plot showing sentiment scores across the movie's subtitles.
- Sentiment trends that can help identify emotional highs and lows in the movie.

## Acknowledgments

- Hugging Face for the sentiment analysis model.
- Open-source libraries like Pandas, Matplotlib, and Seaborn for data processing and visualization.
