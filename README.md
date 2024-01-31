# Sentiment Analysis Flask API

## Overview
This Flask API performs sentiment analysis on various types of text input, including movie reviews, tweets, and generic text. It employs two LSTM models for movie reviews and tweets, along with a machine learning model for generic text analysis.

## Project Structure
|-- flask_app
| |-- templates
| | |-- index.html
| |-- static
| | |-- styles
| | |-- style.css
| |-- init.py
| |-- main.py
|-- models
| |-- sentiment_rnn_movie.model
| |-- sentiment_rnn_tweet.model
| |-- ml_sentiment_model.pkl
|-- requirements.txt
|-- README.md


### File Descriptions

- **flask_app**: Contains the Flask application files.
  - `templates`: HTML templates for rendering web pages.
  - `static`: Static files like stylesheets.
  - `__init__.py`: Initialization file for the Flask app.
  - `main.py`: Main file containing the Flask routes and logic.

- **models**: Directory for storing pre-trained sentiment analysis models.
  - `sentiment_rnn_movie.model`: LSTM model for movie review sentiment analysis and it is not inculded due to its large size.
  - `sentiment_rnn_tweet.model`: LSTM model for tweet sentiment analysis.
  - `ml_sentiment_model.pkl`: Machine learning model for generic text sentiment analysis.

- **requirements.txt**: File specifying project dependencies.

## Setup
1. Clone the repository:
```bash
git clone https://github.com/yourusername/sentiment-analysis-models.git
cd sentiment-analysis-models
2. Install dependencies: `pip install -r requirements.txt`
3. Run the Flask app: `python flask_app/main.py`
4. Access the API at `http://localhost:5000` in your browser.

## Usage
1. Choose the type of input: text, movie review, or tweet.
2. Enter the input in the provided text area.
3. Click "Find Sentiment" to see the sentiment analysis results.


