# Tech Stack: Semantic Company Search API

## Backend Framework
- **FastAPI**: Modern, fast web framework for building APIs with Python 3.7+ based on standard Python type hints
  - Fast performance with automatic Swagger UI documentation
  - Data validation using Pydantic models
  - Async support for handling concurrent requests

## Data Processing
- **Pandas**: Python library for data manipulation and analysis
  - Used for CSV data loading and preprocessing
  - Data cleaning and transformation capabilities

## Vector Embeddings
- **Sentence-Transformers**: Framework for state-of-the-art sentence embeddings
  - Pre-trained models for generating high-quality text embeddings
  - Support for various embedding models (e.g., all-MiniLM-L6-v2)
  - Efficient computation of semantic similarity

## Vector Database
- **Chroma**: Lightweight, in-memory vector database for development
  - Efficient similarity search
  - Simple API for inserting and querying embeddings
  - Support for metadata filtering

## Development Tools
- **Python 3.9+**: Latest stable version of Python
- **Poetry/Pip**: Dependency management
- **Pytest**: For testing API functionality
- **Black/isort**: Code formatting
- **Uvicorn**: ASGI server for running FastAPI applications

## Project Structure
```
semanticsearchapi/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── models.py
│   ├── data/
│   │   ├── __init__.py
│   │   └── processor.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── embedding.py
│   │   └── search.py
│   └── main.py
├── data/
│   └── newdata.csv
├── docs/
│   ├── PRD.md
│   ├── TECH_STACK.md
│   └── IMPLEMENTATION_STRATEGY.md
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── .gitignore
├── README.md
├── requirements.txt
└── pyproject.toml
```

## Deployment Considerations
- Local development via Uvicorn
- Containerization with Docker (future consideration)
- API documentation via automatic Swagger UI 