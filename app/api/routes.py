from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional

from app.core.models import SearchResponse, CompanyResult
from app.services.search import SearchService

router = APIRouter()

# Create a single global instance of SearchService
search_service_instance = SearchService()

# Dependency to get the search service instance
def get_search_service():
    """
    Dependency for getting the search service instance.
    Returns the singleton instance rather than creating a new one each time.
    """
    return search_service_instance

@router.get("/search", response_model=SearchResponse)
async def search_companies(
    query: str = Query(..., description="Search query string"),
    limit: Optional[int] = Query(5, description="Maximum number of results to return"),
    sector: Optional[str] = Query(None, description="Filter results by sector"),
    search_service: SearchService = Depends(get_search_service)
):
    """
    Search for companies using semantic search.
    
    This endpoint performs a vector similarity search on company data based on the input query.
    Results are ordered by relevance to the query.
    
    Examples:
    - Search for AI companies: `/search?query=AI`
    - Search for banking: `/search?query=banking`
    - Search for Tesla: `/search?query=TSLA`
    """
    try:
        # Call the search service to find matching companies
        results = search_service.search(query, limit=limit, sector=sector)
        
        # Return the search response
        return SearchResponse(
            results=results,
            count=len(results),
            query=query
        )
    except Exception as e:
        # Log the error
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}") 