from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
from app.models.document import Document
from app.models.analysis import Analysis


class Database:
    client: AsyncIOMotorClient = None


db = Database()


async def connect_to_mongo():
    """Connect to MongoDB and initialize Beanie ODM."""
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    await init_beanie(
        database=db.client[settings.DATABASE_NAME],
        document_models=[Document, Analysis]
    )
    print("✅ Connected to MongoDB")


async def close_mongo_connection():
    """Close MongoDB connection."""
    db.client.close()
    print("❌ Closed MongoDB connection")
