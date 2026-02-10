import pytest
import httpx

from app.main import app
import app.api.routes.damages as damages_module


@pytest.mark.asyncio
async def test_get_damages_empty(monkeypatch):
    def mock_execute_query(*args, **kwargs):
        return []

    monkeypatch.setattr(damages_module, "execute_query", mock_execute_query)

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/damages/")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_damages_with_data(monkeypatch):
    def mock_execute_query(*args, **kwargs):
        return [
            (1, "Bumper", "LOW", "http://img.jpg", 100.0, 5, 1),
            (2, "Door", "HIGH", "http://img2.jpg", 500.0, 9, 1),
        ]

    monkeypatch.setattr(damages_module, "execute_query", mock_execute_query)

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/damages/")

    assert r.status_code == 200
    assert len(r.json()) == 2


@pytest.mark.asyncio
async def test_create_damage_success(monkeypatch):
    def mock_execute_one(*args, **kwargs):
        query = args[0] if args else ""
        if "SELECT id, status FROM claims" in query:
            return (1, "PENDING")
        elif "INSERT INTO damages" in query:
            return (1,)
        return None

    monkeypatch.setattr(damages_module, "execute_one", mock_execute_one)

    payload = {
        "part": "Bumper",
        "severity": "LOW",
        "image_url": "http://img.jpg",
        "price": 100.0,
        "score": 5
    }

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post("/api/v1/damages/?claim_id=1", json=payload)

    assert r.status_code == 200
    assert r.json()["part"] == "Bumper"


@pytest.mark.asyncio
async def test_create_damage_claim_not_found(monkeypatch):
    def mock_execute_one(*args, **kwargs):
        return None

    monkeypatch.setattr(damages_module, "execute_one", mock_execute_one)

    payload = {
        "part": "Bumper",
        "severity": "LOW",
        "image_url": "http://img.jpg",
        "price": 100.0,
        "score": 5
    }

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post("/api/v1/damages/?claim_id=999", json=payload)

    assert r.status_code == 404


@pytest.mark.asyncio
async def test_create_damage_claim_not_pending(monkeypatch):
    def mock_execute_one(*args, **kwargs):
        return (1, "FINALIZED")

    monkeypatch.setattr(damages_module, "execute_one", mock_execute_one)

    payload = {
        "part": "Bumper",
        "severity": "LOW",
        "image_url": "http://img.jpg",
        "price": 100.0,
        "score": 5
    }

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post("/api/v1/damages/?claim_id=1", json=payload)

    assert r.status_code == 409


@pytest.mark.asyncio
async def test_update_damage_success(monkeypatch):
    def mock_execute_one(*args, **kwargs):
        query = args[0] if args else ""
        if "SELECT d.claim_id, c.status" in query:
            return (1, "PENDING")
        elif "UPDATE damages" in query:
            return (1,)
        return None

    monkeypatch.setattr(damages_module, "execute_one", mock_execute_one)

    payload = {
        "part": "Updated Bumper",
        "severity": "MEDIUM",
        "image_url": "http://updated.jpg",
        "price": 200.0,
        "score": 7
    }

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.put("/api/v1/damages/1", json=payload)

    assert r.status_code == 200
    assert r.json()["part"] == "Updated Bumper"


@pytest.mark.asyncio
async def test_update_damage_not_found(monkeypatch):
    def mock_execute_one(*args, **kwargs):
        return None

    monkeypatch.setattr(damages_module, "execute_one", mock_execute_one)

    payload = {
        "part": "Bumper",
        "severity": "LOW",
        "image_url": "http://img.jpg",
        "price": 100.0,
        "score": 5
    }

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.put("/api/v1/damages/999", json=payload)

    assert r.status_code == 404


@pytest.mark.asyncio
async def test_update_damage_claim_not_pending(monkeypatch):
    def mock_execute_one(*args, **kwargs):
        return (1, "IN_REVIEW")

    monkeypatch.setattr(damages_module, "execute_one", mock_execute_one)

    payload = {
        "part": "Bumper",
        "severity": "LOW",
        "image_url": "http://img.jpg",
        "price": 100.0,
        "score": 5
    }

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.put("/api/v1/damages/1", json=payload)

    assert r.status_code == 409


@pytest.mark.asyncio
async def test_delete_damage_success(monkeypatch):
    def mock_execute_one(*args, **kwargs):
        query = args[0] if args else ""
        if "SELECT d.claim_id, c.status" in query:
            return (1, "PENDING")
        elif "DELETE FROM damages" in query:
            return (1,)
        return None

    monkeypatch.setattr(damages_module, "execute_one", mock_execute_one)

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.delete("/api/v1/damages/1")

    assert r.status_code == 204


@pytest.mark.asyncio
async def test_delete_damage_not_found(monkeypatch):
    def mock_execute_one(*args, **kwargs):
        return None

    monkeypatch.setattr(damages_module, "execute_one", mock_execute_one)

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.delete("/api/v1/damages/999")

    assert r.status_code == 404


@pytest.mark.asyncio
async def test_delete_damage_claim_not_pending(monkeypatch):
    def mock_execute_one(*args, **kwargs):
        return (1, "CANCELED")

    monkeypatch.setattr(damages_module, "execute_one", mock_execute_one)

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.delete("/api/v1/damages/1")

    assert r.status_code == 409


@pytest.mark.asyncio
async def test_create_damage_error(monkeypatch):
    def mock_execute_one(*args, **kwargs):
        query = args[0] if args else ""
        if "SELECT id, status FROM claims" in query:
            return (1, "PENDING")
        return None

    monkeypatch.setattr(damages_module, "execute_one", mock_execute_one)

    payload = {
        "part": "Bumper",
        "severity": "LOW",
        "image_url": "http://img.jpg",
        "price": 100.0,
        "score": 5
    }

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post("/api/v1/damages/?claim_id=1", json=payload)

    assert r.status_code == 500


@pytest.mark.asyncio
async def test_update_damage_error(monkeypatch):
    def mock_execute_one(*args, **kwargs):
        query = args[0] if args else ""
        if "SELECT d.claim_id, c.status" in query:
            return (1, "PENDING")
        return None

    monkeypatch.setattr(damages_module, "execute_one", mock_execute_one)

    payload = {
        "part": "Bumper",
        "severity": "LOW",
        "image_url": "http://img.jpg",
        "price": 100.0,
        "score": 5
    }

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.put("/api/v1/damages/1", json=payload)

    assert r.status_code == 500


@pytest.mark.asyncio
async def test_delete_damage_error(monkeypatch):
    def mock_execute_one(*args, **kwargs):
        query = args[0] if args else ""
        if "SELECT d.claim_id, c.status" in query:
            return (1, "PENDING")
        return None

    monkeypatch.setattr(damages_module, "execute_one", mock_execute_one)

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.delete("/api/v1/damages/1")

    assert r.status_code == 500
