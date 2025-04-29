"""
mongodb.py
"""

# Import the required libraries
import os

import dotenv
from beanie import init_beanie

from motor.motor_asyncio import AsyncIOMotorClient
from config.logging import logger

# Import the required models
from models.box import Box
from models.production_run import ProductionRun
from models.purchase import Purchase
from models.sheet import Sheet


dotenv.load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME")


# Connect to the MongoDB
async def init_db():
    """Initialize the MongoDB connection."""
    try:
        logger.info("Connecting to MongoDB...")
        client = AsyncIOMotorClient(MONGODB_URL)

        # Test the connection
        await client.admin.command("ping")
        logger.info("MongoDB connection successful")

        db = client[MONGODB_DB_NAME]
        await init_beanie(database=db, document_models=[Box, Sheet, Purchase, ProductionRun])
        logger.info("Database initialization complete.")
    except Exception as e:
        logger.error("An error occurred while initializing the database %e", e)
        raise e
