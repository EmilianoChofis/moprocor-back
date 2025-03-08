"""
mongodb.py
"""
#Import the required libraries
import dotenv
import os
import logging

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

#Import the required models
from models.box import Box

#Load the environment variables
dotenv.load_dotenv()

#Get the environment variables
MONGO_URL = os.getenv("MONGO_URL")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME")

#Connect to the MongoDB
async def init_db():
    try:
        logging.info("Connecting to MongoDB...")
        client = AsyncIOMotorClient(MONGO_URL)
        db = client[MONGODB_DB_NAME]
        logging.info("Initializing Beanie ODM...")
        await init_beanie(database=db, document_models=[Box])
        logging.info("Database initialization complete.")
    except Exception as e:
        logging.error(f"An error occurred while initializing the database: {e}")
        raise

if __name__ == "__main__":
    import asyncio
    asyncio.run(init_db())