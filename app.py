from flask import Flask, render_template, request, jsonify, flash, url_for, redirect
import requests
from bs4 import BeautifulSoup
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
from datetime import datetime
import urllib.parse
import re
from newspaper import Article
import hashlib
import json

# Load environment variables
load_dotenv()

# Initialize lightweight summarization using transformers pipeline
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

# Use a better multilingual model for summarization
try:
    # Try to use T5-small for better multilingual support and lighter footprint
    summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")
except Exception as e:
    print(f"Error loading T5 model, falling back to BART: {e}")
    # Fallback to BART if T5 is not available
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text, max_length=150, min_length=30):
    """
    Improved summarization function with better language support
    """
    try:
        # Clean and prepare text
        text = clean_text(text)
        
        # Limit text length to avoid memory issues
        max_input_length = 1024
        if len(text) > max_input_length:
            text = text[:max_input_length]
        
        # Generate summary using the pipeline
        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print(f"Summarization error: {e}")
        # Fallback to simple extractive summarization
        return extractive_summary(text, max_length)

def clean_text(text):
    """Clean and preprocess text for better summarization"""
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    return text

def extractive_summary(text, max_length=150):
    """Simple extractive summary as fallback"""
    sentences = text.split('. ')
    if len(sentences) <= 2:
        return text
    
    # Take first few sentences up to max_length
    summary = ""
    for sentence in sentences[:3]:
        if len(summary + sentence) < max_length:
            summary += sentence + ". "
        else:
            break
    
    return summary.strip()

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

def extract_article_content(url):
    """
    Enhanced article extraction with multiple fallback methods
    to handle paywall sites like Times of India
    """
    try:
        # Method 1: Try newspaper3k library (better for complex sites)
        try:
            article = Article(url)
            article.download()
            article.parse()
            if article.text and len(article.text) > 100:
                return article.text
        except Exception as e:
            print(f"Newspaper3k failed: {e}")
        
        # Method 2: Direct requests with headers to mimic browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            raise Exception(f"HTTP {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
            script.decompose()
        
        # Try different content selectors for various news sites
        content_selectors = [
            'div[class*="article-content"]',
            'div[class*="story-content"]',
            'div[class*="post-content"]',
            'div[class*="entry-content"]',
            'article',
            'div.content',
            'div.story',
            '[data-module="ArticleBody"]',
            '.story-element-text'
        ]
        
        article_text = ""
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                article_text = " ".join(elem.get_text().strip() for elem in elements)
                if len(article_text) > 100:
                    break
        
        # Fallback: get all paragraph text
        if not article_text or len(article_text) < 100:
            paragraphs = soup.find_all("p")
            article_text = " ".join(para.get_text().strip() for para in paragraphs)
        
        return article_text if article_text else "Unable to extract article content."
        
    except Exception as e:
        return f"Error extracting article: {str(e)}"

def find_best_matches(text, keyword):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    lines.insert(0, keyword)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(lines)
    scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    return [(lines[i+1], round(score * 100, 2)) for i, score in enumerate(scores) if score > 0.1]

def generate_share_links(title, url, summary):
    """Generate social media sharing links"""
    encoded_title = urllib.parse.quote(title)
    encoded_url = urllib.parse.quote(url)
    encoded_text = urllib.parse.quote(f"{title[:100]}... {summary[:100]}...")
    
    return {
        'twitter': f"https://twitter.com/intent/tweet?text={encoded_text}&url={encoded_url}",
        'facebook': f"https://www.facebook.com/sharer/sharer.php?u={encoded_url}",
        'linkedin': f"https://www.linkedin.com/sharing/share-offsite/?url={encoded_url}",
        'whatsapp': f"https://wa.me/?text={encoded_text}%20{encoded_url}",
        'telegram': f"https://t.me/share/url?url={encoded_url}&text={encoded_text}",
        'email': f"mailto:?subject={encoded_title}&body={encoded_text}%20{encoded_url}"
    }

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
    title = request.form.get("title", "")
    
    try:
        article_text = extract_article_content(url)
        
        if "Error extracting" in article_text or "Unable to extract" in article_text:
            return jsonify({"error": article_text})

        summary = summarize_text(article_text)
        
        # Generate share links
        share_links = generate_share_links(title, url, summary)
        
        return jsonify({
            "summary": summary,
            "share_links": share_links,
            "word_count": len(article_text.split()),
            "summary_length": len(summary.split())
        })
    except Exception as e:
        return jsonify({"error": f"Failed to process article: {str(e)}"})

@app.route("/share/<path:article_url>")
def share_article(article_url):
    """Generate a shareable page for an article"""
    try:
        # Decode the URL
        decoded_url = urllib.parse.unquote(article_url)
        
        # Extract and summarize the article
        article_text = extract_article_content(decoded_url)
        summary = summarize_text(article_text)
        
        return render_template("share.html", 
                             url=decoded_url, 
                             summary=summary,
                             current_date=datetime.now().strftime("%A, %B %d, %Y"))
    except Exception as e:
        flash(f"Error creating shareable link: {str(e)}")
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)