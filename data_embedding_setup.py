#!/usr/bin/env python3
"""
Data Embedding Setup Script

This script performs a one-time process to:
1. Load company data from a CSV file
2. Generate embeddings for each company
3. Store the embeddings in a vector database (ChromaDB)

Run this script before starting the API server to prepare the vector database.
"""

import os
import sys
import logging
import argparse
import chromadb
from pathlib import Path

# Add the project root to the path so we can import app modules
sys.path.append(str(Path(__file__).resolve().parent))

from app.core.config import settings
from app.data.processor import DataProcessor
from app.services.embedding import EmbeddingService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

# Set lower log level for noisy libraries
logging.getLogger("chromadb").setLevel(logging.WARNING)
logging.getLogger("sentence_transformers").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

def setup_vector_db():
    """
    Set up the vector database connection.
    
    Returns:
        The ChromaDB collection object.
    """
    logger.info(f"Setting up vector database at {settings.VECTOR_DB_PATH}")
    
    # Ensure the vector DB directory exists
    os.makedirs(settings.VECTOR_DB_PATH, exist_ok=True)
    
    # Initialize ChromaDB client
    vector_db = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)
    
    # Create or get collection
    collection = vector_db.get_or_create_collection(
        name="companies",
        metadata={"hnsw:space": "cosine"}  # Use cosine similarity for vector matching
    )
    
    return collection

def populate_vector_db(collection, companies, embedding_service):
    """
    Populate the vector database with company embeddings.
    
    Args:
        collection: The ChromaDB collection
        companies: List of Company objects
        embedding_service: The embedding service to generate embeddings
    """
    logger.info("Generating embeddings for companies")
    
    # Generate embeddings for all companies
    embeddings_dict = embedding_service.generate_embeddings(companies)
    
    # Prepare data for insertion
    ids = [company.stock_symbol for company in companies]
    embeddings = [embeddings_dict[symbol].tolist() for symbol in ids]
    metadatas = [
        {
            "company_name": company.company_name,
            "sector": company.sector,
            "description": company.description
        } 
        for company in companies
    ]
    
    logger.info(f"Adding {len(ids)} company embeddings to vector database")
    
    # Add embeddings to collection
    collection.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=metadatas
    )
    
    logger.info(f"Successfully added {len(ids)} embeddings to vector database")

def main(force_reload=False):
    """
    Main function to set up the vector database with company embeddings.
    
    Args:
        force_reload: Whether to force reload data even if the DB already has entries
    """
    try:
        # Set up vector DB
        collection = setup_vector_db()
        
        # Check if DB already has entries
        count = collection.count()
        if count > 0 and not force_reload:
            logger.info(f"Vector database already contains {count} entries")
            logger.info("Use --force to reload the data if needed")
            return
        
        # Clear existing data if force reload is enabled
        if force_reload and count > 0:
            logger.info(f"Force reload requested. Clearing {count} existing entries...")
            collection.delete(where={})
        
        # Initialize services
        data_processor = DataProcessor()
        embedding_service = EmbeddingService()
        
        # Load and process company data
        logger.info(f"Loading company data from {settings.DATA_PATH}")
        companies = data_processor.get_companies()
        logger.info(f"Loaded {len(companies)} companies")
        
        # Generate embeddings and populate DB
        populate_vector_db(collection, companies, embedding_service)
        
        logger.info("Vector database setup complete!")
        
    except Exception as e:
        logger.error(f"Error setting up vector database: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set up the vector database with company embeddings")
    parser.add_argument("--force", action="store_true", help="Force reload data even if DB already has entries")
    args = parser.parse_args()
    
    main(force_reload=args.force) 