# MIDC Plots Embedding with Pinecone

This project converts MIDC plot data from ODS files to embeddings and stores them in Pinecone for semantic search capabilities.

## 🚀 Quick Start

### 1. Setup Pinecone API Key

First, you need a Pinecone API key. If you don't have one:

1. Go to [Pinecone Console](https://app.pinecone.io/)
2. Sign up or log in
3. Create a new project
4. Get your API key from the dashboard

### 2. Set Environment Variable

```bash
export PINECONE_API_KEY='your-api-key-here'
```

Or run the setup script:
```bash
python3 setup_pinecone.py
```

### 3. Run the Embedding Script

```bash
python3 embed_and_upsert_to_pinecone.py
```

## 📁 File Structure

```
MIDC BOT MANUAL/
├── *.ods                           # Original ODS files
├── csv_output/                     # Converted CSV files
│   ├── VACANT PLOTS *.csv         # Combined multi-sheet data
│   └── TENDERING IN PROGRESS *.csv # Single sheet data
├── json_output/                    # Converted JSON files
│   ├── VACANT PLOTS *.json        # Combined multi-sheet data
│   └── TENDERING IN PROGRESS *.json # Single sheet data
├── convert_ods_to_csv.py          # ODS to CSV converter
├── convert_csv_to_json.py         # CSV to JSON converter
├── embed_and_upsert_to_pinecone.py # Main embedding script
├── setup_pinecone.py              # Pinecone setup helper
└── README_PINECONE_SETUP.md       # This file
```

## 🔧 Technical Details

### Model Used
- **Model**: `sentence-transformers/all-mpnet-base-v2`
- **Dimensions**: 768
- **Purpose**: High-quality semantic embeddings for text similarity

### Pinecone Configuration
- **Index Name**: `midc-plots-index`
- **Dimensions**: 768
- **Metric**: Cosine similarity
- **Cloud**: AWS (us-east-1)
- **Type**: Serverless

### Data Processing
1. **Text Representation**: Each plot record is converted to descriptive text
2. **Embedding Generation**: Text is embedded using the MPNet model
3. **Metadata Storage**: Original data is preserved as metadata
4. **Batch Processing**: Vectors are upserted in batches of 100

### Sample Text Representation
```
Regional Office: RO Ahilyanagar | Industrial Area: Shirdi | Total Plots Available: 45 | Current Rate: 1700.0 Rs per square meter | Category: Commercial 1 | Status: Vacant plots available for allocation
```

## 📊 Data Statistics

- **Total Records**: ~1,180 plot records
- **VACANT Plots**: 1,077 records (3 files × ~359 records each)
- **TENDERING Plots**: 97 records (3 files with varying sizes)
- **Embedding Dimensions**: 768 per record
- **Total Vectors**: ~1,180 vectors in Pinecone

## 🔍 Usage Examples

### Query the Index
```python
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

# Initialize
pc = Pinecone(api_key="your-key")
index = pc.Index("midc-plots-index")
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

# Search for similar plots
query = "commercial plots in Mumbai with low rates"
query_embedding = model.encode([query]).tolist()[0]

results = index.query(
    vector=query_embedding,
    top_k=10,
    include_metadata=True
)

for match in results.matches:
    print(f"Score: {match.score}")
    print(f"Data: {match.metadata}")
```

## 🛠️ Troubleshooting

### Common Issues

1. **API Key Not Set**
   ```
   Error: PINECONE_API_KEY environment variable not set
   ```
   **Solution**: Set the environment variable or run `setup_pinecone.py`

2. **Model Download Issues**
   ```
   Error: Failed to download model
   ```
   **Solution**: Check internet connection, model will be cached after first download

3. **Pinecone Connection Issues**
   ```
   Error: Failed to connect to Pinecone
   ```
   **Solution**: Verify API key and check Pinecone service status

4. **Memory Issues**
   ```
   Error: Out of memory during embedding generation
   ```
   **Solution**: Process files in smaller batches or use a machine with more RAM

### Performance Tips

- The embedding process may take 5-10 minutes for all data
- Model download happens only on first run
- Use batch processing for large datasets
- Monitor Pinecone usage in the dashboard

## 📈 Monitoring

Check your Pinecone dashboard to monitor:
- Index size and performance
- Query usage and costs
- Vector count and storage
- Index health and status

## 🔄 Re-running the Process

To update the data:
1. Update your JSON files
2. Run the embedding script again
3. The script will upsert new vectors (existing ones will be updated)

## 📞 Support

For issues with:
- **Pinecone**: Check [Pinecone Documentation](https://docs.pinecone.io/)
- **Sentence Transformers**: Check [Hugging Face Documentation](https://huggingface.co/sentence-transformers)
- **This Script**: Review the code and error messages
