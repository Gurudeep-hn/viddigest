# 🎥 VidDigest

**Transform YouTube videos into concise, actionable summaries with AI**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A modern web application that uses AI to generate intelligent summaries of YouTube videos, complete with key takeaways and timestamps.

![VidDigest Screenshot](https://via.placeholder.com/800x400/667eea/ffffff?text=VidDigest+Screenshot)

## ✨ Features

- **🤖 AI-Powered Summaries** - Generate concise summaries using Groq's lightning-fast LLM API
- **🎯 Key Points Extraction** - Automatically extract main takeaways and insights
- **⏱️ Smart Timestamps** - Generate chapter-like timestamps for easy navigation
- **📱 Modern UI** - Beautiful, responsive design with smooth animations
- **⚡ Fast Processing** - 2-5 second analysis time (no more waiting!)
- **📋 Copy & Share** - One-click copy functionality for all content
- **🔧 Robust Fallbacks** - Works even without API keys using intelligent rule-based processing

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Internet connection

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/viddigest.git
   cd viddigest
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys (see Configuration section)
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8000`

## 🔧 Configuration

### Required Setup
1. **Get a free Groq API key**: https://console.groq.com/
2. **Add to `.env`**:
   ```bash
   GROQ_API_KEY=your_groq_api_key_here
   ```

### Optional Enhancements
1. **YouTube API key** (for better video metadata): https://console.cloud.google.com/
2. **Add to `.env`**:
   ```bash
   YOUTUBE_API_KEY=your_youtube_api_key_here
   ```

## 📋 Usage

1. **Enter a YouTube URL** in the input field
2. **Click "Analyze Video"**
3. **Wait 2-5 seconds** for AI processing
4. **View results**:
   - Concise AI-generated summary
   - Key takeaways and insights
   - Smart timestamps for navigation
5. **Copy content** with one-click copy buttons

### Supported Videos
- Videos with auto-generated captions
- Videos with manual captions/subtitles
- Public videos (not private or restricted)

## 🏗️ Project Structure

```
viddigest/
├── app.py                   # Main application entry point
├── config/
│   └── settings.py          # Configuration management
├── src/
│   └── services/
│       ├── youtube.py       # YouTube video information
│       ├── transcript.py    # Transcript extraction
│       └── summarizer.py    # AI summarization
├── static/                  # CSS, JS, images
├── templates/               # HTML templates
├── requirements.txt         # Python dependencies
└── .env.example            # Environment template
```

## 🔌 API Endpoints

- `GET /` - Main web interface
- `POST /api/analyze` - Analyze video (JSON API)
- `GET /api/health` - Health check

### API Usage Example
```bash
curl -X POST "http://localhost:8000/api/analyze" \
     -H "Content-Type: application/json" \
     -d '{"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

## 🧠 How It Works

1. **URL Processing** - Extract video ID from YouTube URL
2. **Metadata Extraction** - Get video title, duration, channel info
3. **Transcript Retrieval** - Fetch captions using YouTube Transcript API
4. **AI Summarization** - Process with Groq's Llama 3 model
5. **Content Generation** - Create summary, key points, and timestamps
6. **Fallback Processing** - Use rule-based methods if AI unavailable

## 🎯 Performance

- **Analysis Time**: 2-5 seconds average
- **API Calls**: ~2-3 per video analysis
- **Memory Usage**: < 100MB typical
- **Concurrent Users**: Supports multiple simultaneous requests

## 🔒 Privacy & Security

- **No data storage** - All processing is real-time
- **API keys** - Stored securely in environment variables
- **No video downloads** - Only processes publicly available transcripts
- **CORS enabled** - For frontend API access

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Groq** - For providing fast AI inference
- **YouTube Transcript API** - For transcript extraction
- **FastAPI** - For the excellent web framework
- **Modern web technologies** - For the beautiful UI

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/viddigest/issues)
- **Documentation**: This README and inline code comments
- **API Documentation**: Available at `/docs` when running the app

---

**Built with ❤️ for efficient learning**