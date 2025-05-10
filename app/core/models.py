from pydantic import BaseModel, Field
from typing import List, Optional

class CompanyBase(BaseModel):
    """Base model for company information."""
    company_name: str
    stock_symbol: str
    sector: str
    description: str

class Company(CompanyBase):
    """Model representing a company with all its data."""
    combined_text: Optional[str] = None
    
    class Config:
        from_attributes = True

class CompanyResult(CompanyBase):
    """Model representing a company search result with similarity score."""
    score: float = Field(..., description="Similarity score (0-1)")

class SearchResponse(BaseModel):
    """Model for the search endpoint response."""
    results: List[CompanyResult]
    count: int
    query: str

class EmbeddingConfig(BaseModel):
    """Configuration for the embedding service."""
    model_name: str = "all-MiniLM-L6-v2"
    batch_size: int = 32
    max_seq_length: int = 256 