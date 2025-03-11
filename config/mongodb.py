"""
mongodb.py
"""

# Import the required libraries
import logging

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

# Import the required models
from models.box import Box


# Connect to the MongoDB
async def init_db():
    """Initialize the MongoDB connection."""
    try:
        logging.info("Connecting to MongoDB...")
        client = AsyncIOMotorClient("mongodb://localhost:27017")

        # Test the connection
        await client.admin.command("ping")
        logging.info("MongoDB connection successful")

        db = client["moprocor"]
        await init_beanie(database=db, document_models=[Box])
        logging.info("Database initialization complete.")
    except Exception as e:
        logging.error("An error occurred while initializing the database %e", e)
        raise e
