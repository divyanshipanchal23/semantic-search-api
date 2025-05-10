import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test that the root endpoint returns correct response."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "docs" in response.json()
    assert "search_endpoint" in response.json()

def test_search_endpoint_with_ai_query():
    """Test that the search endpoint works with 'AI' query."""
    response = client.get("/api/v1/search?query=AI")
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert "count" in data
    assert "query" in data
    assert data["query"] == "AI"
    
    # We expect some tech companies in the results
    tech_companies = [r for r in data["results"] if r["sector"] == "Information Technology"]
    assert len(tech_companies) > 0

def test_search_endpoint_with_banking_query():
    """Test that the search endpoint works with 'banking' query."""
    response = client.get("/api/v1/search?query=banking")
    assert response.status_code == 200
    data = response.json()
    
    # We expect financial companies in the results
    financial_companies = [r for r in data["results"] if r["sector"] == "Financials"]
    assert len(financial_companies) > 0

def test_search_endpoint_with_stock_symbol():
    """Test that the search endpoint works with stock symbol query."""
    response = client.get("/api/v1/search?query=TSLA")
    assert response.status_code == 200
    data = response.json()
    
    # Expect Tesla in the results
    tesla_results = [r for r in data["results"] if r["stock_symbol"] == "TSLA"]
    assert len(tesla_results) > 0
    
    if tesla_results:
        tesla = tesla_results[0]
        assert tesla["company_name"] == "Tesla Inc."
        assert tesla["sector"] == "Consumer Discretionary"

def test_search_endpoint_with_limit():
    """Test that the search endpoint respects the limit parameter."""
    limit = 3
    response = client.get(f"/api/v1/search?query=tech&limit={limit}")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["results"]) <= limit
    assert data["count"] <= limit

def test_search_endpoint_with_sector_filter():
    """Test that the search endpoint works with sector filter."""
    response = client.get("/api/v1/search?query=company&sector=Health Care")
    assert response.status_code == 200
    data = response.json()
    
    # All results should be from Health Care sector
    for result in data["results"]:
        assert result["sector"] == "Health Care" 