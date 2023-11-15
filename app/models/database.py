from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient

async def get_database() -> AsyncIOMotorDatabase:
    mongodb_uri = "mongodb://localhost:27017"
    client = AsyncIOMotorClient(mongodb_uri)
    db = client.get_database()
    return db
