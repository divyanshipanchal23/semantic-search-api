import logging
import numpy as np
import chromadb
import os
from typing import List, Optional

from app.core.config import settings
from app.core.models import Company, CompanyResult
from app.data.processor import DataProcessor
from app.services.embedding import EmbeddingService

logger = logging.getLogger(__name__)

class SearchService:
    """
    Service for semantic search functionality.
    Designed to work efficiently with a pre-populated vector database.
    """
    
    _instance = None
    
    def __new__(cls):
        """
        Ensure only one instance of SearchService is created (Singleton pattern).
        """
        if cls._instance is None:
            logger.info("Creating SearchService singleton instance")
            cls._instance = super(SearchService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """
        Initialize the search service with data processing and embedding components.
        This will only execute its code once due to the singleton pattern.
        """
        if not hasattr(self, '_initialized') or not self._initialized:
            logger.info("Initializing SearchService components")
            self.data_processor = DataProcessor()
            self.embedding_service = EmbeddingService()
            self.companies = {}
            self.vector_db = None
            self.collection = None
            
            # Initialize components
            self._initialize()
            self._initialized = True
        else:
            logger.debug("SearchService already initialized, skipping initialization")
    
    def _initialize(self):
        """
        Initialize the search service by setting up the vector DB connection
        and loading company metadata (without re-embedding).
        """
        logger.info("Initializing search service")
        
        # Set up vector DB connection
        self._setup_vector_db()
        
        # Check if vector DB exists and has data
        vector_count = self.collection.count()
        if vector_count == 0:
            logger.warning(
                "Vector database is empty! You should run the data_embedding_setup.py script "
                "to populate the vector database before using the search functionality."
            )
        else:
            logger.info(f"Vector database contains {vector_count} entries")
        
        # Load only company metadata for result formatting (no embeddings)
        self._load_company_metadata()
        
        logger.info("Search service initialization complete")
    
    def _load_company_metadata(self):
        """
        Load only the company metadata needed for search results,
        without generating or storing embeddings.
        """
        logger.info("Loading company metadata for search results")
        companies_list = self.data_processor.get_companies()
        self.companies = {company.stock_symbol: company for company in companies_list}
        logger.info(f"Loaded metadata for {len(self.companies)} companies")
    
    def _setup_vector_db(self):
        """
        Set up the Chroma vector database client and collection.
        """
        logger.info("Setting up vector database connection")
        
        # Ensure the vector DB directory exists
        os.makedirs(settings.VECTOR_DB_PATH, exist_ok=True)
        
        # Initialize ChromaDB client
        self.vector_db = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)
        
        # Create or get collection
        self.collection = self.vector_db.get_or_create_collection(
            name="companies",
            metadata={"hnsw:space": "cosine"}  # Use cosine similarity for vector matching
        )
        
        logger.info(f"Connected to vector database at {settings.VECTOR_DB_PATH}")
    
    def preload_all_components(self):
        """
        Explicitly preload components needed for search.
        """
        logger.info("Preloading search components")
        
        # Preload the embedding model for query processing
        _ = self.embedding_service.generate_embedding("preload")
        
        logger.info("All components preloaded and ready for queries")
        return self
    
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