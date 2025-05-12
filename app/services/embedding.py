import numpy as np
from typing import List, Dict, Optional
import logging
from sentence_transformers import SentenceTransformer

from app.core.config import settings
from app.core.models import Company, EmbeddingConfig

logger = logging.getLogger(__name__)

class EmbeddingService:
    """
    Service for generating embeddings for queries and during setup.
    Uses lazy loading to only initialize the model when needed.
    """
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        """
        Ensure only one instance of EmbeddingService is created (Singleton pattern).
        """
        if cls._instance is None:
            logger.info("Creating EmbeddingService singleton instance")
            cls._instance = super(EmbeddingService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, config: Optional[EmbeddingConfig] = None):
        """
        Initialize the embedding service.
        
        Args:
            config: Configuration for the embedding model.
        """
        if not hasattr(self, '_initialized') or not self._initialized:
            logger.info("Initializing EmbeddingService")
            self.config = config or EmbeddingConfig(model_name=settings.EMBEDDING_MODEL)
            self._model = None
            self._initialized = True
        else:
            logger.debug("EmbeddingService already initialized, skipping initialization")
    
    @property
    def model(self) -> SentenceTransformer:
        """
        Lazy-load the embedding model.
        
        Returns:
            SentenceTransformer model.
        """
        if self._model is None:
            logger.info(f"Loading embedding model: {self.config.model_name}")
            self._model = SentenceTransformer(self.config.model_name)
            logger.info(f"Model loaded with embedding dimension: {settings.EMBEDDING_DIMENSION}")
        return self._model
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for a query text.
        Used for converting search queries to vectors.
        
        Args:
            text: The query text to generate embedding for.
            
        Returns:
            Numpy array of the embedding vector.
        """
        return self.model.encode(text, show_progress_bar=False)
    
    def generate_embeddings(self, companies: List[Company]) -> Dict[str, np.ndarray]:
        """
        Generate embeddings for a list of companies.
        Used by the data_embedding_setup.py script to populate the vector database.
        
        Args:
            companies: List of Company objects.
            
        Returns:
            Dictionary mapping company stock symbols to their embeddings.
        """
        logger.info(f"Generating embeddings for {len(companies)} companies")
        
        # Extract texts to encode
        texts = [company.combined_text for company in companies]
        stock_symbols = [company.stock_symbol for company in companies]
        
        # Generate embeddings in batches
        logger.info(f"Encoding {len(texts)} company texts with batch size {self.config.batch_size}")
        embeddings = self.model.encode(
            texts, 
            batch_size=self.config.batch_size,
            show_progress_bar=True
        )
        
        # Create mapping from stock symbol to embedding
        embeddings_dict = {symbol: embedding for symbol, embedding in zip(stock_symbols, embeddings)}
        
        logger.info(f"Successfully generated {len(embeddings_dict)} embeddings")
        return embeddings_dict 