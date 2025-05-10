# Project Requirements Document: Semantic Company Search API

## Overview
The Semantic Company Search API is designed to allow users to find relevant public companies based on natural language queries. The system leverages vector-based search to match conceptually related terms, going beyond simple keyword matching to understand the semantic meaning behind search queries.

## Core Features

### 1. Semantic Search Capability
- Natural language search queries for company information
- Vector-based similarity matching
- Ability to find companies based on conceptual relationships
- Support for various query formats (company names, sectors, descriptions, stock symbols)

### 2. API Endpoints
- `/search` endpoint that accepts natural language queries
- Return relevant company matches with key information
- Optional filtering capabilities by sector, market cap, etc. (stretch goal)

### 3. Data Processing
- Clean and preprocess company data from CSV
- Generate and maintain embeddings for company information
- Combine relevant fields (name, sector, description) for embedding generation

## Example Use Cases
- Search for "AI" to find tech companies working on artificial intelligence
- Search for "banking" to find financial institutions
- Search for stock symbols like "TSLA" to find the specific company (Tesla, Inc.)

## Technical Requirements
- Python 3.x for backend development
- FastAPI for API framework
- Sentence-transformers for vector embeddings
- Vector database (Chroma) for efficient similarity search
- Pandas for data handling
- Proper project structure with documentation

## Success Criteria
- Working semantic search functionality
- Clean, maintainable code organization
- Well-documented API
- Fast response times
- Accurate matching of relevant companies to search queries 