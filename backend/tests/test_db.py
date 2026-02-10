import pytest
from unittest.mock import Mock, MagicMock, AsyncMock, patch
from app.core.db import (
    MongoDB, mongodb, get_database, get_collection,
    connect_to_mongo, close_mongo_connection,
    execute_query, execute_one,
    insert_one, insert_many,
    find_one, find_many,
    update_one, update_many,
    delete_one, delete_many
)


@pytest.fixture
def mock_db():
    """Setup mock database"""
    mongodb.db = MagicMock()
    yield mongodb.db
    mongodb.db = None
    mongodb.client = None


def test_get_database(mock_db):
    """Test get_database returns database instance"""
    result = get_database()
    assert result == mock_db


def test_get_collection(mock_db):
    """Test get_collection returns collection instance"""
    mock_collection = Mock()
    mock_db.__getitem__.return_value = mock_collection
    
    result = get_collection("test_collection")
    
    mock_db.__getitem__.assert_called_once_with("test_collection")
    assert result == mock_collection


@pytest.mark.asyncio
async def test_connect_to_mongo(capsys):
    """Test MongoDB connection"""
    mock_client = Mock()
    mock_db = Mock()
    mock_client.get_default_database.return_value = mock_db
    
    with patch('app.core.db.AsyncIOMotorClient', return_value=mock_client):
        await connect_to_mongo()
    
    assert mongodb.client == mock_client
    assert mongodb.db == mock_db
    captured = capsys.readouterr()
    assert "Connected to MongoDB" in captured.out


@pytest.mark.asyncio
async def test_close_mongo_connection(capsys):
    """Test MongoDB connection close"""
    mock_client = Mock()
    mongodb.client = mock_client
    
    await close_mongo_connection()
    
    mock_client.close.assert_called_once()
    captured = capsys.readouterr()
    assert "MongoDB connection closed" in captured.out


@pytest.mark.asyncio
async def test_close_mongo_connection_no_client():
    """Test close when no client exists"""
    mongodb.client = None
    await close_mongo_connection()
    # Should not raise exception


@pytest.mark.asyncio
async def test_execute_query(mock_db):
    """Test execute_query returns list of documents"""
    mock_collection = Mock()
    mock_cursor = Mock()
    mock_cursor.to_list = AsyncMock(return_value=[{"id": 1}, {"id": 2}])
    mock_collection.find.return_value = mock_cursor
    mock_db.__getitem__.return_value = mock_collection
    
    result = await execute_query("test_collection", {"status": "active"})
    
    mock_collection.find.assert_called_once_with({"status": "active"})
    assert result == [{"id": 1}, {"id": 2}]


@pytest.mark.asyncio
async def test_execute_query_no_filter(mock_db):
    """Test execute_query with no filter"""
    mock_collection = Mock()
    mock_cursor = Mock()
    mock_cursor.to_list = AsyncMock(return_value=[])
    mock_collection.find.return_value = mock_cursor
    mock_db.__getitem__.return_value = mock_collection
    
    result = await execute_query("test_collection")
    
    mock_collection.find.assert_called_once_with({})
    assert result == []


@pytest.mark.asyncio
async def test_execute_one(mock_db):
    """Test execute_one returns single document"""
    mock_collection = Mock()
    mock_collection.find_one = AsyncMock(return_value={"id": 1})
    mock_db.__getitem__.return_value = mock_collection
    
    result = await execute_one("test_collection", {"id": 1})
    
    mock_collection.find_one.assert_called_once_with({"id": 1})
    assert result == {"id": 1}


@pytest.mark.asyncio
async def test_insert_one(mock_db):
    """Test insert_one returns document ID"""
    mock_collection = Mock()
    mock_result = Mock()
    mock_result.inserted_id = "507f1f77bcf86cd799439011"
    mock_collection.insert_one = AsyncMock(return_value=mock_result)
    mock_db.__getitem__.return_value = mock_collection
    
    result = await insert_one("test_collection", {"name": "test"})
    
    mock_collection.insert_one.assert_called_once_with({"name": "test"})
    assert result == "507f1f77bcf86cd799439011"


@pytest.mark.asyncio
async def test_insert_many(mock_db):
    """Test insert_many returns list of IDs"""
    mock_collection = Mock()
    mock_result = Mock()
    mock_result.inserted_ids = ["id1", "id2", "id3"]
    mock_collection.insert_many = AsyncMock(return_value=mock_result)
    mock_db.__getitem__.return_value = mock_collection
    
    docs = [{"name": "doc1"}, {"name": "doc2"}, {"name": "doc3"}]
    result = await insert_many("test_collection", docs)
    
    mock_collection.insert_many.assert_called_once_with(docs)
    assert result == ["id1", "id2", "id3"]


@pytest.mark.asyncio
async def test_find_one(mock_db):
    """Test find_one returns single document"""
    mock_collection = Mock()
    mock_collection.find_one = AsyncMock(return_value={"id": 1})
    mock_db.__getitem__.return_value = mock_collection
    
    result = await find_one("test_collection", {"id": 1})
    
    mock_collection.find_one.assert_called_once_with({"id": 1})
    assert result == {"id": 1}


@pytest.mark.asyncio
async def test_find_many_no_limit(mock_db):
    """Test find_many without limit"""
    mock_collection = Mock()
    mock_cursor = Mock()
    mock_cursor.to_list = AsyncMock(return_value=[{"id": 1}, {"id": 2}])
    mock_collection.find.return_value = mock_cursor
    mock_db.__getitem__.return_value = mock_collection
    
    result = await find_many("test_collection", {"status": "active"})
    
    mock_collection.find.assert_called_once_with({"status": "active"})
    assert result == [{"id": 1}, {"id": 2}]


@pytest.mark.asyncio
async def test_find_many_with_limit(mock_db):
    """Test find_many with limit"""
    mock_collection = Mock()
    mock_cursor = Mock()
    mock_cursor.limit.return_value = mock_cursor
    mock_cursor.to_list = AsyncMock(return_value=[{"id": 1}])
    mock_collection.find.return_value = mock_cursor
    mock_db.__getitem__.return_value = mock_collection
    
    result = await find_many("test_collection", {"status": "active"}, limit=1)
    
    mock_cursor.limit.assert_called_once_with(1)
    assert result == [{"id": 1}]


@pytest.mark.asyncio
async def test_find_many_no_filter(mock_db):
    """Test find_many with no filter"""
    mock_collection = Mock()
    mock_cursor = Mock()
    mock_cursor.to_list = AsyncMock(return_value=[])
    mock_collection.find.return_value = mock_cursor
    mock_db.__getitem__.return_value = mock_collection
    
    result = await find_many("test_collection")
    
    mock_collection.find.assert_called_once_with({})
    assert result == []


@pytest.mark.asyncio
async def test_update_one(mock_db):
    """Test update_one returns modified count"""
    mock_collection = Mock()
    mock_result = Mock()
    mock_result.modified_count = 1
    mock_collection.update_one = AsyncMock(return_value=mock_result)
    mock_db.__getitem__.return_value = mock_collection
    
    result = await update_one("test_collection", {"id": 1}, {"name": "updated"})
    
    mock_collection.update_one.assert_called_once_with({"id": 1}, {"$set": {"name": "updated"}})
    assert result == 1


@pytest.mark.asyncio
async def test_update_many(mock_db):
    """Test update_many returns modified count"""
    mock_collection = Mock()
    mock_result = Mock()
    mock_result.modified_count = 3
    mock_collection.update_many = AsyncMock(return_value=mock_result)
    mock_db.__getitem__.return_value = mock_collection
    
    result = await update_many("test_collection", {"status": "old"}, {"status": "new"})
    
    mock_collection.update_many.assert_called_once_with({"status": "old"}, {"$set": {"status": "new"}})
    assert result == 3


@pytest.mark.asyncio
async def test_delete_one(mock_db):
    """Test delete_one returns deleted count"""
    mock_collection = Mock()
    mock_result = Mock()
    mock_result.deleted_count = 1
    mock_collection.delete_one = AsyncMock(return_value=mock_result)
    mock_db.__getitem__.return_value = mock_collection
    
    result = await delete_one("test_collection", {"id": 1})
    
    mock_collection.delete_one.assert_called_once_with({"id": 1})
    assert result == 1


@pytest.mark.asyncio
async def test_delete_many(mock_db):
    """Test delete_many returns deleted count"""
    mock_collection = Mock()
    mock_result = Mock()
    mock_result.deleted_count = 5
    mock_collection.delete_many = AsyncMock(return_value=mock_result)
    mock_db.__getitem__.return_value = mock_collection
    
    result = await delete_many("test_collection", {"status": "inactive"})
    
    mock_collection.delete_many.assert_called_once_with({"status": "inactive"})
    assert result == 5
