"""
mongodb.py
"""

# Import the required libraries
from beanie import init_beanie

from motor.motor_asyncio import AsyncIOMotorClient
from config.logging import logger

# Import the required models
from models.box import Box
from models.sheet import Sheet


# Connect to the MongoDB
async def init_db():
    """Initialize the MongoDB connection."""
    try:
        logger.info("Connecting to MongoDB...")
        client = AsyncIOMotorClient("mongodb://localhost:27017")

        # Test the connection
        await client.admin.command("ping")
        logger.info("MongoDB connection successful")

        db = client["moprocor"]
        await init_beanie(database=db, document_models=[Box,Sheet])
        logger.info("Database initialization complete.")
    except Exception as e:
        logger.error("An error occurred while initializing the database %e", e)
        raise e
