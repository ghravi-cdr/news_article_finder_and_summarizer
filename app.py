from flask import Flask, render_template, request, jsonify, flash
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import requests
from bs4 import BeautifulSoup
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize summarization model
model_name = "facebook/bart-large-cnn"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def summarize_text(text):
    inputs = tokenizer.encode("summarize: " + text[:1024], return_tensors="pt", truncation=True)
    summary_ids = model.generate(inputs, max_new_tokens=150, min_new_tokens=50,
                                 length_penalty=2.0, num_beams=4, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# Flask App Setup
app = Flask(__name__)
app.secret_key = "supersecretkey"

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "YOUR_REAL_API_KEY_HERE")

# Helper Functions
def get_news_articles(keyword):
    if not keyword or not NEWS_API_KEY:
        return []

    url = f"https://newsapi.org/v2/everything?q={keyword}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        return data.get("articles", [])
    except Exception as e:
        print(f"API Error: {e}")
        return []

def find_best_matches(text, keyword):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    lines.insert(0, keyword)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(lines)
    scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    return [(lines[i+1], round(score * 100, 2)) for i, score in enumerate(scores) if score > 0.1]

# Routes    
@app.route("/", methods=["GET", "POST"])
def index():
    keyword = ""
    news_results = []
    current_date = datetime.now().strftime("%A, %B %d, %Y")

    if request.method == "POST":
        keyword = request.form.get("keyword")
        if keyword:
            news_results = get_news_articles(keyword)
        else:
            flash("Please enter a keyword.")

    elif request.args.get("q"):  # Popular tag search
        keyword = request.args.get("q")
        news_results = get_news_articles(keyword)

    return render_template("index.html",
                           keyword=keyword,
                           news_results=news_results,
                           current_date=current_date)

@app.route("/summarize-ajax", methods=["POST"])
def summarize_ajax():
    url = request.form.get("url")
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("Failed to fetch article")

        soup = BeautifulSoup(response.text, "html.parser")
        article_text = " ".join(para.get_text() for para in soup.find_all("p"))

        if not article_text:
            raise Exception("No content extracted")

        summary = summarize_text(article_text)
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)