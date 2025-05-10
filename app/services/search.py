import logging
import numpy as np
import chromadb
import os
from typing import List, Dict, Any, Optional
from sklearn.metrics.pairwise import cosine_similarity

from app.core.config import settings
from app.core.models import Company, CompanyResult
from app.data.processor import DataProcessor
from app.services.embedding import EmbeddingService

logger = logging.getLogger(__name__)

class SearchService:
    """
    Service for semantic search functionality.
    """
    
    def __init__(self):
        """
        Initialize the search service with data processing and embedding components.
        """
        self.data_processor = DataProcessor()
        self.embedding_service = EmbeddingService()
        self.companies = {}
        self.vector_db = None
        self.collection = None
        
        # Initialize components
        self._initialize()
    
    def _initialize(self):
        """
        Initialize the search service by loading data, generating embeddings, and setting up the vector DB.
        """
        logger.info("Initializing search service")
        
        # Load and process company data as objects
        companies_list = self.data_processor.get_companies()
        
        # Create a dictionary lookup of companies by stock symbol
        self.companies = {company.stock_symbol: company for company in companies_list}
        
        # Generate embeddings
        self.embedding_service.generate_embeddings(companies_list)
        
        # Set up Chroma vector DB
        self._setup_vector_db(companies_list)
        
        logger.info("Search service initialization complete")
    
    def _setup_vector_db(self, companies: List[Company]):
        """
        Set up the Chroma vector database.
        
        Args:
            companies: List of Company objects.
        """
        logger.info("Setting up vector database")
        
        # Ensure the vector DB directory exists
        os.makedirs(settings.VECTOR_DB_PATH, exist_ok=True)
        
        # Initialize ChromaDB client
        self.vector_db = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)
        
        # Create or get collection
        self.collection = self.vector_db.get_or_create_collection(
            name="companies",
            metadata={"hnsw:space": "cosine"}  # Use cosine similarity for vector matching
        )
        
        # Check if we need to add data to the collection
        if self.collection.count() == 0:
            # Prepare data for insertion
            ids = [company.stock_symbol for company in companies]
            embeddings = [self.embedding_service.get_embedding(symbol).tolist() for symbol in ids]
            metadatas = [
                {
                    "company_name": company.company_name,
                    "sector": company.sector,
                    "description": company.description
                } 
                for company in companies
            ]
            
            # Add embeddings to collection
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                metadatas=metadatas
            )
            
            logger.info(f"Added {len(ids)} embeddings to vector database")
    
    def search(self, query: str, limit: int = 5, sector: Optional[str] = None) -> List[CompanyResult]:
        """
        Perform semantic search for companies based on query.
        
        Args:
            query: Search query text.
            limit: Maximum number of results to return.
            sector: Optional sector filter.
            
        Returns:
            List of CompanyResult objects with matching companies and similarity scores.
        """
        logger.info(f"Searching for: '{query}' (limit: {limit}, sector: {sector})")
        
        # Generate embedding for the query
        query_embedding = self.embedding_service.generate_embedding(query).tolist()
        
        # Prepare the filter
        where_clause = None
        if sector:
            where_clause = {"sector": sector}
        
        # Search the vector database
        search_results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit,
            where=where_clause
        )
        
        # Process results
        results = []
        if search_results["ids"]:
            for i, stock_symbol in enumerate(search_results["ids"][0]):
                company = self.companies.get(stock_symbol)
                if company:
                    # Create company result with similarity score
                    score = search_results["distances"][0][i] if "distances" in search_results else 1.0
                    # Convert distance to similarity score (1 - distance for cosine)
                    normalized_score = 1 - score
                    
                    result = CompanyResult(
                        company_name=company.company_name,
                        stock_symbol=company.stock_symbol,
                        sector=company.sector,
                        description=company.description,
                        score=normalized_score
                    )
                    
                    results.append(result)
        
        logger.info(f"Found {len(results)} results for query: '{query}'")
        return results 