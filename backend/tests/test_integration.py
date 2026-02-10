import pytest
import httpx
import os


BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


@pytest.mark.asyncio
@pytest.mark.integration
async def test_health_check_integration():
    """Test real HTTP request to /health endpoint. Requires server running."""
    try:
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=5.0) as client:
            response = await client.get("/health")
        
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
    except httpx.ConnectError:
        pytest.skip(f"Server not running at {BASE_URL}. Start with: uvicorn app.main:app --host 127.0.0.1 --port 8000")


@pytest.mark.asyncio
@pytest.mark.integration
async def test_root_integration():
    """Test real HTTP request to / endpoint. Requires server running."""
    try:
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=5.0) as client:
            response = await client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
    except httpx.ConnectError:
        pytest.skip(f"Server not running at {BASE_URL}. Start with: uvicorn app.main:app --host 127.0.0.1 --port 8000")
