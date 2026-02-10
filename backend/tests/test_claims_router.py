import pytest
import httpx

from app.main import app
import app.api.routes.claims as claims_module

@pytest.mark.asyncio
async def test_get_claims_empty(monkeypatch):
    async def mock_execute_query(*args, **kwargs):
        return []

    monkeypatch.setattr(claims_module, "execute_query", mock_execute_query)

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/claims/")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_claims_with_data(monkeypatch):
    call_count = [0]
    
    async def mock_execute_query(*args, **kwargs):
        call_count[0] += 1
        if call_count[0] == 1:
            return [
                (1, "Claim 1", "Desc", "PENDING"),
                (2, "Claim 2", None, "IN_REVIEW"),
            ]
        else:
            return []

    monkeypatch.setattr(claims_module, "execute_query", mock_execute_query)

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/claims/")

    assert r.status_code == 200
    assert len(r.json()) == 2


@pytest.mark.asyncio
async def test_create_claim(monkeypatch):
    async def mock_execute_one(*args, **kwargs):
        return (1,)

    payload = {
        "title": "New claim",
        "description": "Desc",
        "status": "PENDING"
    }

    monkeypatch.setattr(claims_module, "execute_one", mock_execute_one)

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post("/api/v1/claims/", json=payload)

    assert r.status_code == 201
    assert r.json()["title"] == "New claim"


@pytest.mark.asyncio
async def test_update_claim_status(monkeypatch):
    call_count = [0]
    
    async def mock_execute_one(*args, **kwargs):
        call_count[0] += 1
        if call_count[0] == 1:
            return (1, "Claim 1", "Long description " * 20, "PENDING")
        elif call_count[0] == 2:
            return None
        elif call_count[0] == 3:
            return (1,)
        else:
            return (1, "Claim 1", "Long description " * 20, "FINALIZED")
    
    async def mock_execute_query(*args, **kwargs):
        return []

    monkeypatch.setattr(claims_module, "execute_one", mock_execute_one)
    monkeypatch.setattr(claims_module, "execute_query", mock_execute_query)

    payload = {"status": "FINALIZED"}

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.patch("/api/v1/claims/1/status", json=payload)

    assert r.status_code == 200


@pytest.mark.asyncio
async def test_get_claim_not_found(monkeypatch):
    async def mock_execute_one(*args, **kwargs):
        return None

    monkeypatch.setattr(claims_module, "execute_one", mock_execute_one)

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/claims/999")

    assert r.status_code == 404


@pytest.mark.asyncio
async def test_update_claim_not_found(monkeypatch):
    async def mock_execute_one(*args, **kwargs):
        return None

    monkeypatch.setattr(claims_module, "execute_one", mock_execute_one)

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.patch("/api/v1/claims/999/status", json={"status": "FINALIZED"})

    assert r.status_code == 404


@pytest.mark.asyncio
async def test_cancel_non_pending_claim(monkeypatch):
    async def mock_execute_one(*args, **kwargs):
        return (1, "Claim 1", "Desc", "IN_REVIEW")

    monkeypatch.setattr(claims_module, "execute_one", mock_execute_one)

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.patch("/api/v1/claims/1/status", json={"status": "CANCELED"})

    assert r.status_code == 409


@pytest.mark.asyncio
async def test_finalize_high_damage_short_description(monkeypatch):
    call_count = [0]
    
    async def mock_execute_one(*args, **kwargs):
        call_count[0] += 1
        if call_count[0] == 1:
            return (1, "Claim 1", "Short", "PENDING")
        else:
            return (1,)

    monkeypatch.setattr(claims_module, "execute_one", mock_execute_one)

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.patch("/api/v1/claims/1/status", json={"status": "FINALIZED"})

    assert r.status_code == 409
