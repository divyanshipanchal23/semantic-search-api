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
│   └── newdata.csv       # Company dataset with 500+ companies
├── docs/                 # Project documentation
├── tests/                # Test suite
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

4. **Run the application**

```bash
uvicorn app.main:app --reload
```

5. **Access the API**

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

### Running Tests

```bash
pytest tests/
```

### Data Pipeline

The system processes company data from a CSV file, creates embeddings, and stores them in a vector database for efficient similarity search.

## License

[MIT License](LICENSE) 