"""
Box repository for MongoDB.
"""

from typing import List, Optional, Dict
from models.box import Box


class BoxRepository:
    """Box repository for MongoDB using Beanie ORM functions."""

    @staticmethod
    async def get_all() -> List[Box]:
        """
        Get all boxes from the database.

        :return: List of all Box documents.
        :rtype: List[Box]
        """
        return await Box.all().to_list()

    @staticmethod
    async def get_by_symbol(symbol: str) -> Optional[Box]:
        """
        Get a box by its symbol.

        :param symbol: The symbol of the box to retrieve.
        :type symbol: str
        :return: The Box document with the given symbol, or None if not found.
        :rtype: Optional[Box]
        """
        return await Box.find_one(Box.symbol == symbol)

    @staticmethod
    async def create(box: Box) -> Box:
        """
        Create a new box in the database.

        :param box: The Box document to create.
        :type box: Box
        :return: The created Box document.
        :rtype: Box
        """
        return await Box.insert_one(box)

    @staticmethod
    async def get_filtered_boxes(query: str, offset: int, limit: int) -> Dict[str, list[Box]]:
        """
        Get filtered boxes with pagination.

        :param query: The search query to filter boxes.
        :type query: str
        :param offset: The number of documents to skip.
        :type offset: int
        :param limit: The maximum number of documents to return.
        :type limit: int
        :return: A dictionary containing the filtered boxes.
        :rtype: Dict[str, list[Box]]
        """
        # Filtro de búsqueda
        filters = {
            "$or": [
                {"symbol": {"$regex": query, "$options": "i"}},
                {"liner": {"$regex": query, "$options": "i"}},
                {"flute": {"$regex": query, "$options": "i"}},
                {"client": {"$regex": query, "$options": "i"}},
                {"status": {"$regex": query, "$options": "i"}}
            ]
        }

        # Obtiene las cajas con paginación
        boxes = await Box.find(filters).skip(offset).limit(limit).to_list()

        return boxes

    @staticmethod
    async def get_total_count(query: str) -> int:
        """
        Get the total count of filtered boxes.

        :param query: The search query to filter boxes.
        :type query: str
        :return: The total count of filtered boxes.
        :rtype: int
        """
        filters = {
            "$or": [
                {"symbol": {"$regex": query, "$options": "i"}},
                {"liner": {"$regex": query, "$options": "i"}},
                {"flute": {"$regex": query, "$options": "i"}},
                {"client": {"$regex": query, "$options": "i"}},
                {"status": {"$regex": query, "$options": "i"}}
            ]
        }

        total_count = await Box.find(filters).count()
        return total_count

    @staticmethod
    async def get_all_symbols() -> List[str]:
        """
        Get all box symbols from the database.

        :return: List of all box symbols.
        :rtype: List[str]
        """
        # For raw MongoDB queries with projection, use the motor client directly
        collection = Box.get_motor_collection()
        cursor = collection.find({}, {"symbol": 1, "_id": 0})
        result = await cursor.to_list(length=None)
        return [doc["symbol"] for doc in result]