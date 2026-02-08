import pytest
import httpx
import os


BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


@pytest.mark.asyncio
async def test_health_check_integration():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_root_integration():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
