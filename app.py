from flask import Flask, render_template, request, redirect, url_for
from transformers import T5Tokenizer, T5ForConditionalGeneration
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import torch
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Initialize the pretrained model, tokenizer, and sentiment analyzer
model = T5ForConditionalGeneration.from_pretrained('t5-small')
tokenizer = T5Tokenizer.from_pretrained('t5-small')
analyzer = SentimentIntensityAnalyzer()
device = torch.device('cpu')

# Connect to the MySQL database
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="text_summarization"
    )
    print("Database connected successfully!")
except mysql.connector.Error as err:
    print(f"Error: {err}")

cursor = db.cursor()

@app.route('/', methods=['GET', 'POST'])
def index():
    text = ""
    summary = None
    sentiment = None
    sentiment_score = None
    history = []

    if request.method == 'POST':
        # Get text input from the form
        text = request.form['text']

        # Preprocess the input text
        preprocessed_text = text.strip().replace('\n', ' ')
        t5_input_text = 'summarize: ' + preprocessed_text

        # Tokenize the input text
        tokenized_text = tokenizer.encode(t5_input_text, return_tensors='pt', max_length=512, truncation=True).to(device)

        # Generate the summary
        summary_ids = model.generate(
            tokenized_text,
            min_length=10,
            max_length=150,
            num_beams=4,
            repetition_penalty=2.5,
            early_stopping=True
        )
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True).capitalize()

        # Perform sentiment analysis on the summary
        sentiment_result = analyzer.polarity_scores(summary)
        sentiment_score = sentiment_result['compound']
        if sentiment_score >= 0.05:
            sentiment = "Positive"
        elif sentiment_score <= -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        # Save the result to the database
        cursor.execute(
            "INSERT INTO summaries (original_text, summary, sentiment, sentiment_score, timestamp) VALUES (%s, %s, %s, %s, %s)",
            (text, summary, sentiment, sentiment_score, datetime.now())
        )
        db.commit()

    # Retrieve history from the database
    cursor.execute("SELECT id, summary, sentiment FROM summaries ORDER BY timestamp DESC")
    history = cursor.fetchall()

    return render_template('index.html', original_text=text, summary=summary, sentiment=sentiment, sentiment_score=sentiment_score, history=history)

@app.route('/delete_summary', methods=['POST'])
def delete_summary():
    summary_id = request.form['summary_id']

    # Delete the summary from the database
    cursor.execute("DELETE FROM summaries WHERE id = %s", (summary_id,))
    db.commit()

    return redirect(url_for('index'))

@app.route('/show_original', methods=['POST'])
def show_original():
    summary_id = request.form['summary_id']

    # Fetch the original text using the summary ID
    cursor.execute("SELECT original_text FROM summaries WHERE id = %s", (summary_id,))
    result = cursor.fetchone()

    if result:
        original_text = result[0]
    else:
        original_text = "Original text not found."

    return render_template('original_text.html', original_text=original_text)

if __name__ == '__main__':
    app.run(debug=True)
