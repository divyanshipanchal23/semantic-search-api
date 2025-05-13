# Semantic Company Search API

A FastAPI-based semantic search API that enables users to find relevant public companies based on natural language queries. The system leverages vector embeddings and similarity search to match conceptually related terms, going beyond simple keyword matching.

## Features

- Natural language search queries for company information
- Vector-based semantic similarity matching
- Support for various query formats (names, sectors, descriptions, stock symbols)
- Fast and efficient API responses
- Well-documented endpoints with Swagger UI

## Example Use Cases

- Search for "AI" to find tech companies working on artificial intelligence
- Search for "banking" to find financial institutions
- Search for stock symbols like "TSLA" to find Tesla, Inc.

## Tech Stack

- **FastAPI**: API framework
- **Sentence-Transformers**: For generating text embeddings
- **Chroma**: Vector database for similarity search
- **Pandas**: Data processing
- **Python 3.9+**: Core language

## Project Structure

```
semanticsearchapi/
├── app/
│   ├── api/              # API routes and endpoints
│   ├── core/             # Core configurations and models
│   ├── data/             # Data processing utilities
│   ├── services/         # Business logic services
│   └── main.py           # Application entry point
├── data/                 # Data files
│   ├── newdata.csv       # Company dataset with 500+ companies
│   └── vectordb/         # Vector database storage directory
├── data_embedding_setup.py  # Script to set up vector database
├── .gitignore
├── README.md
└── requirements.txt      # Dependencies
```

## Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/divyanshipanchal23/semantic-search-api.git
cd semanticsearchapi
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up the vector database**

This is a one-time process that converts the CSV data into vector embeddings and stores them in ChromaDB:

```bash
python data_embedding_setup.py
```

If you need to rebuild the vector database (e.g., after updating your dataset), use:

```bash
python data_embedding_setup.py --force
```

5. **Run the application**

```bash
uvicorn app.main:app --reload
```

6. **Access the API**

- API documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
- API endpoints: [http://localhost:8000/api/v1/search](http://localhost:8000/api/v1/search)

## API Usage

### Search Endpoint

```
GET /api/v1/search?query=<search_term>
```

Example request:

```bash
curl -X 'GET' \
  'http://localhost:8000/api/v1/search?query=AI%20technology' \
  -H 'accept: application/json'
```

Example response:

```json
{
  "results": [
    {
      "company_name": "NVIDIA Corporation",
      "stock_symbol": "NVDA",
      "sector": "Information Technology",
      "description": "NVIDIA designs and manufactures graphics processing units (GPUs) for gaming, professional visualization, data centers, and automotive markets. The company is a leader in AI computing hardware and software.",
      "score": 0.89
    },
    {
      "company_name": "Microsoft Corporation",
      "stock_symbol": "MSFT",
      "sector": "Information Technology",
      "description": "Microsoft develops, licenses, and supports software, services, devices, and solutions worldwide. Its products include Windows operating systems, Office productivity suite, Azure cloud platform, and gaming consoles like Xbox.",
      "score": 0.75
    }
  ],
  "count": 2,
  "query": "AI technology"
}
```

## Development

### Data Pipeline

The system uses a two-phase approach for optimal performance:

1. **Data Embedding Setup (One-time Process)**:
   - The `data_embedding_setup.py` script loads company data from CSV
   - Generates vector embeddings using the Sentence-Transformers model
   - Stores embeddings in a persistent ChromaDB database
   - Only needs to be run once or after updating the dataset

2. **Search Process (Runtime)**:
   - API loads only company metadata (not generating embeddings)
   - User query is converted to a vector embedding
   - Vector similarity search is performed against the pre-built database
   - Results are returned based on semantic similarity

This approach separates the computationally intensive embedding generation from the search API, ensuring optimal performance.

## Performance Optimizations

### Vector Database Efficiency

The system has been optimized for production use:

1. **One-time Embedding Generation**: The most computationally intensive task (generating embeddings) is done once during setup, not on application startup.

2. **Persistent Vector Storage**: Company embeddings and all metadata are stored in a persistent vector database (ChromaDB) at `data/vectordb/` and reused across application restarts.

3. **Zero CSV Dependency at Runtime**: After initial setup, the application operates completely independent of the original CSV file, retrieving all necessary data from the vector database.

4. **Minimal Runtime Loading**: The application only loads:
   - The embedding model for processing search queries
   - The pre-built vector database connection with company metadata

5. **Singleton Pattern**: Both `SearchService` and `EmbeddingService` use a singleton pattern to ensure only one instance exists throughout the application lifecycle.

6. **Smart Refresh Logic**: The setup script checks if vectors already exist and only regenerates them when explicitly requested.

## License

[MIT License](LICENSE) 