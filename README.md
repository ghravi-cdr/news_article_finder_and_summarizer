# 📰 NewsHub Enhanced - AI-Powered News Summarization Platform

NewsHub is a modern, AI-powered news aggregation and summarization platform that helps you stay informed with intelligent article summaries and seamless sharing capabilities.

## 🌟 Enhanced Features

### ✨ Advanced AI Summarization
- **Multilingual Support**: Uses T5-small model for better multilingual summarization
- **Smart Fallback**: Automatically falls back to BART-large-CNN if T5 fails
- **Text Preprocessing**: Advanced text cleaning and preprocessing for better results
- **Language Detection**: Improved handling of articles in various languages
- **Extractive Fallback**: Simple extractive summarization as ultimate fallback

### 🚀 Enhanced Article Extraction
- **Paywall Bypass**: Multiple extraction methods to handle paywalled sites like Times of India
- **Smart Content Detection**: Uses multiple CSS selectors to find article content
- **Browser Simulation**: Mimics real browser headers to bypass simple blocking
- **Newspaper3k Integration**: Primary extraction using newspaper3k library
- **Fallback Methods**: Multiple extraction strategies for maximum compatibility

### 📱 Social Media Sharing
- **Multiple Platforms**: Share to Twitter, Facebook, LinkedIn, WhatsApp, Email
- **Copy Link**: One-click link copying functionality
- **Share URLs**: Generate shareable links for article summaries
- **Social Media Integration**: Properly formatted sharing with titles and descriptions
- **Mobile Optimized**: Share buttons work seamlessly on mobile devices

### 🎨 Modern UI/UX
- **Card-Based Design**: Clean, modern article cards with hover effects
- **Responsive Layout**: Optimized for desktop, tablet, and mobile
- **Loading States**: Beautiful loading animations and progress indicators
- **Error Handling**: User-friendly error messages and fallback options
- **Statistics Display**: Shows word count and summary length
- **Smooth Animations**: Hover effects and smooth transitions

### 🔧 Performance Improvements
- **Lightweight Models**: Optimized model loading for faster startup
- **Better Caching**: Improved caching strategies for repeated requests
- **Error Recovery**: Robust error handling with multiple fallback mechanisms
- **Mobile Performance**: Optimized for mobile devices and slower connections

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- News API key (free from [newsapi.org](https://newsapi.org/))

### Installation

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd newshub
   python setup_and_test.py
   ```

2. **Configure API Key**
   - Edit the `.env` file created during setup
   - Add your News API key:
     ```
     NEWS_API_KEY=your_actual_api_key_here
     ```

3. **Run the Application**
   ```bash
   python app.py
   ```

4. **Access NewsHub**
   - Open http://localhost:5000 in your browser
   - Start searching and summarizing news!

## 🛠 Manual Installation

If you prefer manual setup:

```bash
pip install flask transformers torch newspaper3k beautifulsoup4 python-dotenv nltk sentencepiece scikit-learn requests
```

## 🎯 How to Use

### Basic News Search
1. Enter keywords in the search bar
2. Browse through the curated articles
3. Click "Summarize" to get AI-generated summaries
4. Use "Read Full" to access the original article

### Advanced Features
- **Share Articles**: Use the share buttons to spread news on social media
- **Copy Links**: Quickly copy article URLs for sharing
- **Responsive Design**: Works perfectly on all devices
- **Multi-language**: Summarizes articles in various languages

### Handling Paywalled Articles
The enhanced extraction system automatically:
- Tries multiple extraction methods
- Uses browser-like headers
- Employs different CSS selectors
- Provides fallback extraction options

## 🔧 Technical Details

### AI Models Used
- **Primary**: T5-small (Google's Text-to-Text Transfer Transformer)
- **Fallback**: BART-large-CNN (Facebook's BART model)
- **Extraction**: newspaper3k + BeautifulSoup + custom selectors

### Supported Article Sources
- Major news websites (CNN, BBC, Reuters, etc.)
- Regional news sites (Times of India, etc.)
- Blog articles and online publications
- Most websites with proper article structure

### Browser Compatibility
- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers

## 🎨 Customization

### Theme Support
- Light and dark themes available
- Automatic theme detection
- Customizable CSS variables

### Styling
Edit `static/style.css` to customize:
- Colors and themes
- Layout and spacing
- Animation speeds
- Mobile breakpoints

## 🐛 Troubleshooting

### Common Issues

1. **Summarization Not Working**
   - Check internet connection
   - Verify model downloads completed
   - Try running `python setup_and_test.py`

2. **Article Extraction Fails**
   - Some sites have strong anti-bot measures
   - Try different articles or sources
   - Check if the site requires JavaScript

3. **Sharing Not Working**
   - Ensure popup blockers are disabled
   - Check browser permissions
   - Try different sharing platforms

### Performance Issues
- First-time model loading takes time
- Subsequent requests are much faster
- Consider using a GPU for better performance

## 📊 Features Comparison

| Feature | Original | Enhanced |
|---------|----------|----------|
| Summarization Model | BART only | T5 + BART fallback |
| Language Support | English only | Multilingual |
| Article Extraction | Basic | Advanced with fallbacks |
| Sharing | None | Full social media integration |
| UI/UX | Basic | Modern, responsive |
| Error Handling | Limited | Comprehensive |
| Mobile Support | Basic | Fully optimized |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google T5 team for the transformer model
- Facebook for BART model
- newspaper3k library developers
- Flask community
- All contributors and testers

## 📞 Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Check the troubleshooting section
- Run the test script: `python setup_and_test.py`

---

**NewsHub Enhanced** - Stay informed, stay connected! 📰✨ 
