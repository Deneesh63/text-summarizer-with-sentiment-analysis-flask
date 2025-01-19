# Text Summarizer Application

## Project Overview

This project is a **Text Summarizer Application** built using Flask, T5 Transformer Model, and MySQL. The application takes user-provided text, generates a concise summary, analyzes the sentiment of the summary, and stores the data in a MySQL database for later reference. The application includes an intuitive web interface with features like summary history, sentiment-based color-coded entries, and the ability to view or delete summaries.

---

## Key Features

1. **Text Summarization**:

   - Leverages the pre-trained **T5 Transformer Model** for accurate and concise text summaries.

2. **Sentiment Analysis**:

   - Utilizes **VADER Sentiment Analysis** to classify summaries as Positive, Negative, or Neutral.

3. **User-Friendly Interface**:

   - A responsive and visually appealing web UI built with HTML, CSS, and Flask templates.
   - Dynamic, sentiment-based coloring for summary history entries.

4. **Database Integration**:

   - Stores original text, summaries, sentiment, and timestamps in a **MySQL** database.
   - Users can view and delete stored summaries conveniently.

5. **Background Aesthetics**:

   - Includes a background video for a modern and engaging user experience.

---

## How to Run the Project

### Prerequisites

1. **Python** (>=3.8)
2. **MySQL Server**
3. Required Python libraries:
   - `Flask`
   - `transformers`
   - `torch`
   - `vaderSentiment`
   - `mysql-connector-python`
4. A compatible web browser (e.g., Chrome, Firefox).

### Installation Steps

1. **Clone the Repository**:

   ```bash
   git clone <repository-link>
   cd text-summarizer
   ```

2. **Set Up the MySQL Database**:

   - Create a database named `text_summarization`.
   - Create the `summaries` table using the following schema:
     ```sql
     CREATE TABLE summaries (
         id INT AUTO_INCREMENT PRIMARY KEY,
         original_text TEXT,
         summary TEXT,
         sentiment VARCHAR(50),
         sentiment_score FLOAT,
         timestamp DATETIME
     );
     ```

3. **Create a Python Virtual Environment**:

   ```bash
   python -m venv env
   source env/bin/activate   # For Linux/macOS
   env\Scripts\activate    # For Windows
   ```

4. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Flask Application**:

   ```bash
   python app.py
   ```

6. **Access the Application**:

   - Open your browser and navigate to `http://127.0.0.1:5000/`.

---

## Project Structure

```
text-summarizer/
├── app.py                 # Main Flask application
├── static/
│   ├── style.css          # Stylesheet for the web interface
│   └── bg.mp4             # Background video
├── templates/
│   ├── index.html         # Main page
│   └── original_text.html # Original text display page
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## Usage

1. Enter text into the text area and click "Summarize".
2. View the generated summary and sentiment analysis.
3. Check the summary history section for past entries.
4. Click "Show Original Text" to view the original input or "Delete" to remove a summary.

---

## Improvements from Existing Versions

1. **Sentiment-Based Visualization**:

   - Summaries are color-coded based on sentiment for quick interpretation.

2. **Enhanced Responsiveness**:

   - Improved UI design ensures compatibility across devices and screen sizes.

3. **Streamlined Text Preprocessing**:

   - Automated handling of input inconsistencies like extra spaces and newlines.

4. **Database Management**:

   - Added options to view or delete specific summaries from the database.
