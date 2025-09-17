# 🏢 MIDC Land Bank Chatbot

A modern, AI-powered chatbot for the Maharashtra Industrial Development Corporation (MIDC) Land Bank, providing intelligent assistance for land plot queries in both English and Marathi.

![MIDC Logo](static/images/midc-logo.jpg)

## 🌟 Features

- **🤖 AI-Powered Responses**: Uses Google Gemini AI for intelligent, contextual responses
- **🔍 RAG Technology**: Retrieval-Augmented Generation with Pinecone vector database
- **🌐 Multilingual Support**: English and Marathi language support
- **📱 Modern UI**: Responsive web interface with professional MIDC branding
- **🏗️ Real-time Data**: Access to current MIDC land bank information
- **💬 Interactive Chat**: Natural conversation flow with suggestion buttons

## 🚀 Live Demo

**Access the chatbot**: [http://localhost:8080](http://localhost:8080)

## 📋 What You Can Ask

The chatbot can help you with:

- **🏠 Residential Plots**: Available residential land plots and pricing
- **🏭 Industrial Plots**: Industrial land availability and specifications  
- **🏪 Commercial Plots**: Commercial plot details and tendering status
- **💰 Pricing Information**: Current plot prices and payment terms
- **📍 Location Details**: Specific locations and plot specifications
- **📊 Tendering Status**: Information about plots under tender

### Example Queries

```
English:
- "Show me available commercial plots in Pune"
- "What are the current residential plot prices?"
- "Tell me about industrial plots in Dhule"

Marathi:
- "पुणे मध्ये व्यावसायिक प्लॉट दाखवा"
- "सध्याच्या निवासी प्लॉट किंमती काय आहेत?"
- "धुळे मध्ये औद्योगिक प्लॉट बद्दल सांगा"
```

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **AI/ML**: Google Gemini AI, Sentence Transformers
- **Vector Database**: Pinecone
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Modern CSS with custom design system
- **Language Detection**: Custom language detection module

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- Git
- Pinecone account
- Google AI API key

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/Yash-Amrutkar/MIDC-BOT-.git
   cd MIDC-BOT-
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API keys**
   
   Update `config.py` with your API keys:
   ```python
   # Pinecone Configuration
   PINECONE_API_KEY = 'your-pinecone-api-key'
   PINECONE_INDEX_NAME = 'midc-plots-index'
   
   # Google Gemini Configuration
   GOOGLE_API_KEY = 'your-google-api-key'
   ```

4. **Run the application**
   ```bash
   python3 app.py
   ```

5. **Access the chatbot**
   
   Open your browser and go to: `http://localhost:8080`

## 📁 Project Structure

```
MIDC-BOT-/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── final_rag_service.py        # RAG service implementation
├── language_detector.py        # Language detection module
├── requirements.txt            # Python dependencies
├── static/                     # Web assets
│   ├── css/
│   │   └── style.css          # Custom styling
│   ├── images/
│   │   └── midc-logo.jpg      # MIDC logo
│   └── js/
│       └── script.js          # Frontend JavaScript
├── templates/
│   └── index.html             # Main HTML template
├── csv_output/                # Processed CSV data
├── json_output/               # Processed JSON data
└── README.md                  # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file (optional):
```env
PINECONE_API_KEY=your_pinecone_api_key
GOOGLE_API_KEY=your_google_api_key
PINECONE_INDEX_NAME=midc-plots-index
```

### API Keys Setup

1. **Pinecone**: Get your API key from [Pinecone Console](https://app.pinecone.io/)
2. **Google AI**: Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## 🎨 Customization

### Branding
- Update `static/images/midc-logo.jpg` with your logo
- Modify colors in `static/css/style.css` (CSS variables)
- Update company information in `templates/index.html`

### Data
- Add new plot data to `csv_output/` or `json_output/` directories
- Update the RAG service to include new data sources

## 🚀 Deployment

### Local Development
```bash
python3 app.py
```

### Production Deployment
For production, use a WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8080 app:app
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
```

## 📊 API Endpoints

- `GET /` - Main chatbot interface
- `POST /api/chat` - Chat endpoint for user queries
- `GET /api/health` - Health check endpoint

### Chat API Example
```bash
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me residential plots in Pune"}'
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Yash Amrutkar**
- GitHub: [@Yash-Amrutkar](https://github.com/Yash-Amrutkar)
- Project Link: [https://github.com/Yash-Amrutkar/MIDC-BOT-](https://github.com/Yash-Amrutkar/MIDC-BOT-)

## 🙏 Acknowledgments

- Maharashtra Industrial Development Corporation (MIDC)
- Google AI for Gemini API
- Pinecone for vector database services
- Flask community for the excellent web framework

## 📞 Support

For support, email your-email@example.com or create an issue in this repository.

---

**Made with ❤️ for MIDC Land Bank Services**
