"""
Sheet repository for interacting with the sheets collection in MongoDB.
"""

from typing import List, Optional

from models.sheet import Sheet


class SheetRepository:
    """Sheet repository for MongoDB using Beanie ORM functions."""

    @staticmethod
    async def get_all() -> List[Sheet]:
        """
        Get all sheets from the database.

        :return: List of all Sheet documents.
        :rtype: List[Sheet]
        """
        return await Sheet.all().to_list()

    @staticmethod
    async def get_by_id(sheet_id: str) -> Optional[Sheet]:
        """
        Get a sheet by its ID.

        :param sheet_id: The ID of the sheet to retrieve.
        :type sheet_id: str
        :return: The Sheet document with the given ID, or None if not found.
        :rtype: Optional[Sheet]
        """
        return await Sheet.find_one(Sheet.id == sheet_id)

    @staticmethod
    async def create(sheet: Sheet) -> Sheet:
        """
        Create a new sheet in the database.

        :param sheet: The Sheet document to create.
        :type sheet: Sheet
        :return: The created Sheet document.
        :rtype: Sheet
        """
        return await Sheet.insert_one(sheet)
