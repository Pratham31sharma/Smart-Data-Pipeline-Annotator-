# Smart Data Pipeline Annotator 🚀

An intelligent ETL pipeline with AI-powered data enrichment capabilities, built with Python, Streamlit, and Groq LLM API.

## ✨ Features

### 🔧 Core ETL Pipeline
- **Extract**: Upload and process CSV files with automatic validation
- **Transform**: AI-powered data enrichment using Groq LLM models
- **Load**: SQLite database integration with SQLAlchemy
- **Query**: Natural language to SQL conversion for easy data exploration

### 🤖 AI-Powered Enrichment
- **Sentiment Analysis**: Automatic sentiment classification (positive/negative/neutral)
- **Keyword Extraction**: Intelligent keyword identification from text data
- **Text Summarization**: Concise summaries (max 20 words)
- **Text Cleaning**: Normalized and cleaned text output

### 📊 Advanced Analytics Dashboard
- **Interactive Visualizations**: Sentiment distribution charts, keyword analysis
- **Real-time Metrics**: Processing statistics and performance indicators
- **Data Export**: Multiple format support (CSV, Excel, JSON)
- **Natural Language Queries**: Ask questions in plain English

### 🚀 Performance Features
- **Smart Caching**: On-disk LLM response caching for faster processing
- **Batch Processing**: Configurable batch sizes for optimal performance
- **Model Selection**: Choose between speed vs. quality models
- **Progress Tracking**: Real-time processing status and ETA

## 🛠️ Technology Stack

- **Backend**: Python 3.11+, FastAPI, SQLAlchemy
- **Frontend**: Streamlit, Plotly
- **AI/ML**: Groq LLM API, PyTorch, Scikit-learn
- **Data Processing**: Pandas, NumPy
- **Database**: SQLite
- **Deployment**: Docker

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Groq API key (get one at [groq.com](https://groq.com))

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd Smart-Data-Pipeline-Annotator
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up your Groq API key**
```bash
export GROQ_API_KEY="your_api_key_here"
```

4. **Run the application**
```bash
streamlit run dashboard.py
```

### Docker Deployment

1. **Build the image**
```bash
docker build -t smart-pipeline-annotator .
```

2. **Run the container**
```bash
docker run -p 8501:8501 -e GROQ_API_KEY="your_api_key" smart-pipeline-annotator
```

## 📖 Usage Guide

### 1. Data Upload
- Upload your CSV file through the sidebar
- Select the text column for enrichment
- View data preview and column information

### 2. AI Enrichment
- Choose your preferred model (speed vs. quality)
- Set batch size for processing
- Run enrichment and monitor progress
- View real-time metrics and performance

### 3. Data Analysis
- Browse enriched data in the database
- Use natural language queries
- Export results in multiple formats
- Visualize sentiment distributions and trends

### 4. Performance Optimization
- Use smaller models for faster processing
- Adjust batch sizes based on your needs
- Monitor API usage and latency
- Leverage caching for repeated data

## 🔧 Configuration

### Environment Variables
- `GROQ_API_KEY`: Your Groq API key (required)
- `BATCH_SIZE`: Default batch size for processing
- `CACHE_ENABLED`: Enable/disable LLM response caching

### Model Options
- **llama3-8b-8192**: Fast processing (8B model)
- **llama3-70b-8192**: Balanced quality (70B model)
- **mixtral-8x7b-32768**: Fast with good quality (8x7B model)
- **gemma2-9b-it**: Very fast processing (9B model)

## 📊 Supported Data Formats

### Input
- CSV files with text columns
- UTF-8 encoding
- Maximum file size: 100MB

### Output
- Enriched CSV with new columns
- SQLite database tables
- Multiple export formats (CSV, Excel, JSON)

## 🎯 Use Cases

- **Customer Feedback Analysis**: Sentiment analysis of reviews and comments
- **Content Classification**: Automatic tagging and categorization
- **Data Quality Improvement**: Text cleaning and normalization
- **Business Intelligence**: Natural language querying of structured data
- **Research Data Processing**: Automated annotation and enrichment

## 🔒 Security Features

- **API Key Management**: Secure storage and validation
- **SQL Injection Protection**: Parameterized queries
- **Input Validation**: File type and size restrictions
- **Error Handling**: Graceful failure with detailed logging

## 📈 Performance Metrics

- **Processing Speed**: ~0.5 seconds per row (varies by model)
- **Cache Hit Rate**: Significantly improves performance for repeated data
- **API Efficiency**: Optimized batch processing reduces API calls
- **Memory Usage**: Efficient pandas operations with minimal overhead

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Groq**: For providing fast and reliable LLM inference
- **Streamlit**: For the excellent web app framework
- **Open Source Community**: For the amazing Python ecosystem

## 📞 Support

For questions, issues, or contributions:
- Create an issue on GitHub
- Contact: prathamsharma31002@gmail.com
- LinkedIn: [Pratham Sharma](your-linkedin-url)

---

**Built with ❤️ by Pratham Sharma**
