"""
Sheet repository for interacting with the sheets collection in MongoDB.
"""

from typing import List, Optional, Dict

from bson import ObjectId

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
        return await Sheet.find_one({"_id": ObjectId(sheet_id)})

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

    @staticmethod
    async def get_filtered_sheets(query: str, offset: int, limit: int) -> Dict[str, list[Sheet]]:
        """Obtiene todas las hojas con paginación y total"""

        # Filtro de búsqueda
        filters = {
            "$or": [
                {"grams": {"$in": [int(query)]}} if query.isdigit() else {},
                {"ect": {"$in": [int(query)]}} if query.isdigit() else {},
                {"roll_width": {"$in": [int(query)]}} if query.isdigit() else {},
                {"p1": {"$in": [int(query)]}} if query.isdigit() else {},
                {"p2": {"$in": [int(query)]}} if query.isdigit() else {},
                {"p3": {"$in": [int(query)]}} if query.isdigit() else {},
                {"description": {"$regex": query, "$options": "i"}}
            ]
        }

        # Obtener las hojas con paginación
        sheets = await Sheet.find(filters).skip(offset).limit(limit).to_list()

        return sheets

    @staticmethod
    async def get_total_count(query: str) -> int:
        """Obtiene el total de hojas filtradas"""

        filters = {
            "$or": [
                {"grams": {"$in": [int(query)]}} if query.isdigit() else {},
                {"ect": {"$in": [int(query)]}} if query.isdigit() else {},
                {"roll_width": {"$in": [int(query)]}} if query.isdigit() else {},
                {"p1": {"$in": [int(query)]}} if query.isdigit() else {},
                {"p2": {"$in": [int(query)]}} if query.isdigit() else {},
                {"p3": {"$in": [int(query)]}} if query.isdigit() else {},
                {"description": {"$regex": query, "$options": "i"}}
            ]
        }

        total_count = await Sheet.find(filters).count()
        return total_count
