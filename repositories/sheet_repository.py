"""
Sheet repository for interacting with the sheets collection in MongoDB.
"""

from typing import List, Optional, Dict

from beanie import PydanticObjectId
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

    @staticmethod
    async def update_sheet(sheet_id: PydanticObjectId, update_data: dict) -> Optional[Sheet]:
        """
        Update a sheet in the database.

        :param sheet_id: The ID of the sheet to update.
        :type sheet_id: PydanticObjectId
        :param update_data: The data to update in the sheet.
        :type update_data: dict
        :return: The updated Sheet document, or None if not found.
        :rtype: Optional[Sheet]
        """
        sheet = await Sheet.get(sheet_id)
        if not sheet:
            return None
        await sheet.update({"$set": update_data})
        return await Sheet.get(sheet_id)

    @staticmethod
    async def change_status(sheet_id: PydanticObjectId, status: str) -> Optional[Sheet]:
        """
        Change the status of a sheet.

        :param sheet_id: The ID of the sheet to update.
        :type sheet_id: PydanticObjectId
        :param status: The new status for the sheet.
        :type status: str
        :return: The updated Sheet document, or None if not found.
        :rtype: Optional[Sheet]
        """
        if status not in ["APPROVED", "REVIEW", "DISUSE"]:
            raise ValueError("Invalid status value")
        return await SheetRepository.update_sheet(sheet_id, {"status": status})