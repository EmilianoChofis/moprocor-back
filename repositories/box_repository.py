"""
Box repository for MongoDB.
"""

from typing import List, Optional
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
