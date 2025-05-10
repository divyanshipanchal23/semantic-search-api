import os
from pathlib import Path
from pydantic_settings import BaseSettings

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Set data path to newdata.csv
DATA_PATH = os.path.join(BASE_DIR, "data", "newdata.csv")

class Settings(BaseSettings):
    """
    Application settings.
    """
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Semantic Company Search API"
    
    # Data settings
    DATA_PATH: str = DATA_PATH
    
    # Embeddings settings
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384  # Dimension of the all-MiniLM-L6-v2 model
    
    # Vector DB settings path where the vector database will store its files
    VECTOR_DB_PATH: str = os.path.join(BASE_DIR, "data", "vectordb")
    
    # API settings
    DEFAULT_RESULTS_LIMIT: int = 5
    
    model_config = {
        "case_sensitive": True,
        "env_file": os.path.join(BASE_DIR, ".env"),
        "env_file_encoding": "utf-8"
    }

settings = Settings() 