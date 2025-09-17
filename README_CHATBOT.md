# 🏢 MIDC Land Bank Chatbot

A local conversational AI assistant for Maharashtra Industrial Development Corporation (MIDC) land bank information. This chatbot helps users find information about industrial, commercial, and residential plots using advanced RAG (Retrieval-Augmented Generation) technology.

## 🚀 Features

- **🤖 AI-Powered Conversations**: Natural language interactions about MIDC plots
- **🔍 Semantic Search**: Find relevant plots using natural language queries
- **📊 Comprehensive Data**: Access to 1,174+ plot records across Maharashtra
- **💬 Chat Interface**: User-friendly web-based chat interface
- **📱 Responsive Design**: Works on desktop and mobile devices
- **🔄 Real-time Responses**: Instant answers to your queries

## 📋 Prerequisites

- Python 3.8 or higher
- Pinecone API key (required)
- Google API key (optional but recommended for better responses)

## 🛠️ Installation

### Option 1: Quick Setup (Recommended)

1. **Run the setup script:**
   ```bash
   python setup_chatbot.py
   ```
   This will guide you through the configuration process.

2. **Launch the chatbot:**
   ```bash
   python run_chatbot.py
   ```

### Option 2: Manual Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API keys:**
   Edit `config.py` and add your API keys:
   ```python
   PINECONE_API_KEY = 'your-pinecone-api-key'
   GOOGLE_API_KEY = 'your-google-api-key'  # Optional
   ```

3. **Run the chatbot:**
   ```bash
   streamlit run midc_chatbot.py
   ```

## 🔑 Getting API Keys

### Pinecone API Key (Required)
1. Go to [Pinecone Console](https://app.pinecone.io/)
2. Sign up or log in
3. Create a new project
4. Get your API key from the dashboard

### Google API Key (Optional)
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key for use in config.py

## 💬 How to Use

1. **Launch the chatbot** using one of the methods above
2. **Open your browser** to `http://localhost:8501`
3. **Start chatting** with questions like:
   - "Show me commercial plots in Mumbai"
   - "What are the cheapest industrial plots?"
   - "Find plots in Pune"
   - "Show me vacant residential plots"

## 🎯 Example Queries

### Location-Based Queries
- "plots available in pune"
- "industrial plots in mumbai"
- "commercial plots in thane"
- "residential plots in nashik"

### Type-Based Queries
- "commercial plots"
- "industrial plots"
- "residential plots"
- "vacant plots"

### Price-Based Queries
- "cheapest industrial plots"
- "plots under 2000 rs per square meter"
- "expensive commercial plots"
- "affordable residential plots"

### Availability Queries
- "plots with high availability"
- "plots with more than 50 units"
- "limited availability plots"

## 📁 Project Structure

```
MIDC BOT MANUAL/
├── midc_chatbot.py          # Main Streamlit chatbot application
├── final_rag_service.py     # RAG service with Pinecone integration
├── config.py                # Configuration file
├── run_chatbot.py           # Chatbot launcher script
├── setup_chatbot.py         # Setup script
├── requirements.txt         # Python dependencies
├── README_CHATBOT.md        # This file
├── json_output/             # JSON data files
├── csv_output/              # CSV data files
└── embed_and_upsert_to_pinecone.py  # Data embedding script
```

## 🔧 Configuration

The `config.py` file contains all configuration settings:

```python
# Pinecone Configuration
PINECONE_API_KEY = 'your-pinecone-api-key'
PINECONE_INDEX_NAME = 'midc-plots-index'

# Embedding Model
EMBEDDING_MODEL = 'sentence-transformers/all-mpnet-base-v2'

# Google Gemini Configuration
GOOGLE_API_KEY = 'your-google-api-key'
GENERATION_MODEL = 'gemini-pro'

# Search Configuration
TOP_K_RESULTS = 10
SIMILARITY_THRESHOLD = 0.3
```

## 🐛 Troubleshooting

### Common Issues

1. **"Pinecone API key not set"**
   - Make sure you've added your Pinecone API key to `config.py`
   - Verify the key is correct and active

2. **"No results found"**
   - Try rephrasing your question
   - Use more specific location names
   - Check if the Pinecone index is properly populated

3. **"Error initializing RAG service"**
   - Check your internet connection
   - Verify all required packages are installed
   - Make sure the Pinecone index exists

4. **"Streamlit not found"**
   - Install Streamlit: `pip install streamlit`
   - Or install all requirements: `pip install -r requirements.txt`

### Performance Tips

- **First run**: The embedding model download may take a few minutes
- **Subsequent runs**: Should be much faster as the model is cached
- **Memory usage**: The chatbot uses about 2-3GB RAM for optimal performance

## 📊 Data Information

- **Total Records**: 1,174+ plot records
- **Categories**: Industrial, Commercial, Residential
- **Regions**: Multiple regional offices across Maharashtra
- **Status**: Vacant plots and plots under tendering
- **Embedding Model**: sentence-transformers/all-mpnet-base-v2 (768 dimensions)

## 🤝 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Verify your API keys are correct
3. Ensure all dependencies are installed
4. Check your internet connection

## 📝 License

This project is for educational and demonstration purposes. Please ensure you have proper permissions to use the MIDC data and API services.

## 🔄 Updates

To update the chatbot with new data:

1. Update your JSON files in the `json_output/` directory
2. Run the embedding script: `python embed_and_upsert_to_pinecone.py`
3. Restart the chatbot

---

**Happy Plot Hunting! 🏢✨**
