# News Article Finder & Summarizer

> A Python-based application that fetches the latest news articles from various sources and summarizes them using NLP techniques.

This project allows users to:
- Fetch top/latest news from trusted sources via APIs (e.g., NewsAPI).
- Filter news by keywords, categories, or sources.
- Automatically summarize long articles for quick reading.
- Optionally run via a simple web interface using Flask or Streamlit.

It's ideal for developers looking to explore real-time data fetching, NLP summarization, and API integrations.

---
 Features

-  Fetch news from multiple sources
-  Keyword/category-based filtering
-  Text summarization using NLP models
-  Optional web interface (Flask/Streamlit)
-  Easy-to-use and customizable

---
 Technologies Used

- **Python**
- **NewsAPI** (or other APIs like GNews, RSS feeds)
- **Natural Language Processing (NLP)** libraries:
  - `nltk`
  - `sumy` / `transformers` / `spaCy` (based on your implementation)
- **Web Framework (Optional):**
  - `Flask`
  **Model Used**
  - Hugging face "facebook/bart-large-cnn" model
---

## 📦 Requirements

Install dependencies using pip:

Flask==3.0.0
newsapi-python==0.2.7
transformers==4.35.0
torch==2.1.0
requests==2.31.0
beautifulsoup4==4.12.0
scikit-learn==1.3.0
python-dotenv==1.0.1 
