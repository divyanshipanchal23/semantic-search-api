from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
import logging
import os

from app.api.routes import router as api_router, search_service_instance
from app.core.config import settings

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
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    """
    Create the FastAPI application with all routes and middleware.
    """
    logger.info("Initializing FastAPI application")
    app = FastAPI(
        title="Semantic Company Search API",
        description="API for semantic search of company information",
        version="1.0.0",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(api_router, prefix="/api/v1")

    # Register startup event to check and initialize search service
    @app.on_event("startup")
    def initialize_services():
        """Initialize services at application startup."""
        logger.info("Application starting: Pre-initializing search service")
        
        # Check if vector database directory exists
        if not os.path.exists(settings.VECTOR_DB_PATH):
            logger.warning(
                "Vector database directory not found! Please run: \n"
                "python data_embedding_setup.py\n"
                "to set up the vector database before using the search functionality."
            )
        
        # Preload the embedding model for query processing
        search_service_instance.preload_all_components()
        
        logger.info("All services initialized and ready")

    return app

app = create_app()

@app.get("/")
async def root():
    """
    Root endpoint for the API.
    """
    return {
        "message": "Welcome to the Semantic Company Search API",
        "docs": "/docs",
        "search_endpoint": "/api/v1/search?query=your_search_query",
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 