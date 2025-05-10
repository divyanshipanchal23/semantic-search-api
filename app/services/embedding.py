import numpy as np
from typing import List, Dict, Any, Optional
import logging
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

from app.core.config import settings
from app.core.models import Company, EmbeddingConfig

logger = logging.getLogger(__name__)

class EmbeddingService:
    """
    Service for generating and managing embeddings for company data.
    """
    
    def __init__(self, config: Optional[EmbeddingConfig] = None):
        """
        Initialize the embedding service.
        
        Args:
            config: Configuration for the embedding model.
        """
        self.config = config or EmbeddingConfig(model_name=settings.EMBEDDING_MODEL)
        self._model = None
        self.embeddings = {}
    
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
        return self._model
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text.
        
        Args:
            text: The text to generate embedding for.
            
        Returns:
            Numpy array of the embedding vector.
        """
        return self.model.encode(text, show_progress_bar=False)
    
    def generate_embeddings(self, companies: List[Company]) -> Dict[str, np.ndarray]:
        """
        Generate embeddings for a list of companies.
        
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
        embeddings = self.model.encode(
            texts, 
            batch_size=self.config.batch_size,
            show_progress_bar=True
        )
        
        # Create mapping from stock symbol to embedding
        self.embeddings = {symbol: embedding for symbol, embedding in zip(stock_symbols, embeddings)}
        
        logger.info(f"Successfully generated {len(self.embeddings)} embeddings")
        return self.embeddings
    
    def get_embedding(self, stock_symbol: str) -> Optional[np.ndarray]:
        """
        Get the embedding for a specific company by stock symbol.
        
        Args:
            stock_symbol: The stock symbol of the company.
            
        Returns:
            Numpy array of the embedding vector, or None if not found.
        """
        return self.embeddings.get(stock_symbol) 