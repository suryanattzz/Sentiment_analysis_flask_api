from flask import Flask, render_template, request,session
from keras.utils import pad_sequences
from flask_app import app
import tensorflow as tf
from tensorflow.keras.models import load_model
import re,pickle,warnings
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

warnings.filterwarnings("ignore")

with open('models\\logistic_model_sentiment_30.pkl', 'rb') as model_file:
    loaded_logistic_model = pickle.load(model_file)
with open('models\\count_vectorizer_ML_sentiment_30.pkl', 'rb') as vectorizer_file:
    loaded_count_vectorizer = pickle.load(vectorizer_file)

with open('models\\tokenizer_lstm_10_25.pickle', 'rb') as handle:
    loaded_tokenizer_movie = pickle.load(handle)
with open('models\\tokenizer_lstm_tweet_20_37.pickle', 'rb') as handle:
    loaded_tokenizer_tweet = pickle.load(handle)

tokenizer_tweet = loaded_tokenizer_tweet
tokenizer_movie = loaded_tokenizer_movie


lstm_model_tweet = load_model('models\\sentiment_rnn_tweet_20_37.h5')
lstm_model_movie = load_model('models\\sentiment_rnn_movie_10_25 .h5')
threshold_tweet = 0.37
threshold_movie = 0.25

def func_1(text):
    stop_words=set(stopwords.words('english'))
    lemmatizer=WordNetLemmatizer()
    cleaned_string = re.sub(r'[-_.,;:\'"#<>\/=&@*!)(}{?\d]', '', text)
    cleaned_string = re.sub('https://.*','',cleaned_string) 
    cleaned_string = re.sub(pattern='@[a-zA-Z_0-9]*', repl='@user',string=cleaned_string)
    cleaned_string = cleaned_string.lower()
    cleaned_string = ' '.join([i for i in cleaned_string.split() if i not in stop_words])
    lemmatized_words = [lemmatizer.lemmatize(word) for word in cleaned_string.split()]
    lemmatized_string = ' '.join(lemmatized_words)
    
    return lemmatized_string

def func_2(text):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    cleaned_string = re.sub(r'[-_.,;:\'"#<>\/=&@*!)(}{?\d]', '', text)
    cleaned_string = cleaned_string.lower()
    cleaned_string = ' '.join([i for i in cleaned_string.split() if i not in stop_words])
    lemmatized_words = [lemmatizer.lemmatize(word) for word in cleaned_string.split()]
    lemmatized_string = ' '.join(lemmatized_words)

    return lemmatized_string


def lstm_sentiment_model(text, model, tokenizer, threshold, maxlen):
    if max==400:
        new_text = func_2(text)
    else:
        new_text = func_1(text)
    new_text_sequence = tokenizer.texts_to_sequences([new_text])
    new_text_padded = pad_sequences(new_text_sequence, padding='post', maxlen=maxlen)
    predictions = model.predict(new_text_padded)
    predicted_class_prob = predictions[0][0] 

    output = 'The sentiment is positive.' if predicted_class_prob > threshold else 'The sentiment is negative.'
    return text, output, str(round(float(predicted_class_prob), 4))


def ml_sentiment_model(text, model, vectorizer):
    cleaned_text = func_1(text)
    transformed_text = vectorizer.transform([cleaned_text])
    predictions = model.predict(transformed_text)
    output = 'The sentiment is positive.' if predictions[0] == 1 else 'The sentiment is negative.'

    return text, output, predictions[0]

@app.route('/')
@app.route('/', methods=['GET', 'POST'])
def index():
    text, sentiment, prediction = None, None, None
    if 'predictions' not in session:
        session['predictions'] = []

    if request.method == 'POST':
        input_type = request.form['input_type']

        if input_type == '':
            return render_template('index.html', text=None, sentiment=None, prediction=None, message="Please select one of the three options.")

        if input_type == 'text':
            text, sentiment, prediction = ml_sentiment_model(request.form['form-textarea'], loaded_logistic_model, loaded_count_vectorizer)

        if input_type == 'movie':
            text, sentiment, prediction = lstm_sentiment_model(request.form['form-textarea'], lstm_model_movie, tokenizer_movie, threshold_movie, maxlen=400)
            
        elif input_type == 'tweet':
            text, sentiment, prediction = lstm_sentiment_model(request.form['form-textarea'], lstm_model_tweet, tokenizer_tweet, threshold_tweet, maxlen=25)

        session['predictions'] = {'text': text, 'sentiment': sentiment, 'prediction': prediction}

    stored_prediction = session.get('predictions', {})
    return render_template('index.html', text=stored_prediction.get('text', ''), sentiment=stored_prediction.get('sentiment', ''), prediction=stored_prediction.get('prediction', ''))
