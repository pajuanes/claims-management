from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from app.core.config import settings
from typing import Optional, List, Dict, Any


class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    db = None


mongodb = MongoDB()


def get_database():
    """Get database instance"""
    return mongodb.db


def get_collection(collection_name: str):
    """Get collection instance"""
    return mongodb.db[collection_name]


async def connect_to_mongo():
    """Connect to MongoDB"""
    mongodb.client = AsyncIOMotorClient(settings.MONGO_URI)
    mongodb.db = mongodb.client.get_default_database()
    print("✅ Connected to MongoDB")


async def close_mongo_connection():
    """Close MongoDB connection"""
    if mongodb.client:
        mongodb.client.close()
        print("🛑 MongoDB connection closed")


# Legacy compatibility functions
async def execute_query(collection: str, filter_query: Dict[str, Any] = None) -> List[Dict]:
    """Execute a find query and return results"""
    coll = get_collection(collection)
    cursor = coll.find(filter_query or {})
    return await cursor.to_list(length=None)


async def execute_one(collection: str, filter_query: Dict[str, Any]) -> Optional[Dict]:
    """Execute a find_one query and return single result"""
    coll = get_collection(collection)
    return await coll.find_one(filter_query)


# MongoDB-oriented API
async def insert_one(collection: str, document: Dict[str, Any]) -> str:
    """Insert a document and return its ID"""
    coll = get_collection(collection)
    result = await coll.insert_one(document)
    return str(result.inserted_id)


async def insert_many(collection: str, documents: List[Dict[str, Any]]) -> List[str]:
    """Insert multiple documents and return their IDs"""
    coll = get_collection(collection)
    result = await coll.insert_many(documents)
    return [str(id) for id in result.inserted_ids]


async def find_one(collection: str, filter_query: Dict[str, Any]) -> Optional[Dict]:
    """Find a single document"""
    coll = get_collection(collection)
    return await coll.find_one(filter_query)


async def find_many(collection: str, filter_query: Dict[str, Any] = None, limit: int = 0) -> List[Dict]:
    """Find multiple documents"""
    coll = get_collection(collection)
    cursor = coll.find(filter_query or {})
    if limit > 0:
        cursor = cursor.limit(limit)
    return await cursor.to_list(length=None)


async def update_one(collection: str, filter_query: Dict[str, Any], update_data: Dict[str, Any]) -> int:
    """Update a single document"""
    coll = get_collection(collection)
    result = await coll.update_one(filter_query, {"$set": update_data})
    return result.modified_count


async def update_many(collection: str, filter_query: Dict[str, Any], update_data: Dict[str, Any]) -> int:
    """Update multiple documents"""
    coll = get_collection(collection)
    result = await coll.update_many(filter_query, {"$set": update_data})
    return result.modified_count


async def delete_one(collection: str, filter_query: Dict[str, Any]) -> int:
    """Delete a single document"""
    coll = get_collection(collection)
    result = await coll.delete_one(filter_query)
    return result.deleted_count


async def delete_many(collection: str, filter_query: Dict[str, Any]) -> int:
    """Delete multiple documents"""
    coll = get_collection(collection)
    result = await coll.delete_many(filter_query)
    return result.deleted_count