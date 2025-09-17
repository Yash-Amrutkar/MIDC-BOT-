# Configuration file for RAG Service

# Pinecone Configuration
PINECONE_API_KEY = 'pcsk_7QV7Xo_KDE1D54JX94rBXgvUBhjPwd5yqtYm1zyhT11S4CSZSH2v2tXi4Ja1EEwypYUfQK'
PINECONE_INDEX_NAME = 'midc-plots-index'

# Embedding Model Configuration
EMBEDDING_MODEL = 'sentence-transformers/all-mpnet-base-v2'

# Google Gemini Configuration
GOOGLE_API_KEY = 'AIzaSyCQpo_8CfjgPEvakuemrbLRBGjiW051uKE'  # Replace with your actual Google API key
GENERATION_MODEL = 'gemini-1.5-flash'

# Search Configuration
TOP_K_RESULTS = 10  # Increased to get more results
SIMILARITY_THRESHOLD = 0.3  # Lowered threshold to get more results
