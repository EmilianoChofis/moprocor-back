"""
Repository for Purchase documents in the database.
"""

from typing import List

from models.box import Box
from models.purchase import Purchase
from models.sheet import Sheet


class PurchaseRepository:
    """Purchase repository for MongoDB using Beanie ORM functions."""

    @staticmethod
    async def get_all():
        """
        Get all purchases from the database.
        :return: List of all Purchase documents.
        :rtype: List[Purchase]
        """
        return await Purchase.all().to_list()

    @staticmethod
    async def get_by_arapack_lot(purchase_arapack_lot: str):
        """
        Get a purchase by its ID.
        :param purchase_arapack_lot: The ID of the Purchase document.
        :return: The Purchase document with the given ID, or None if not found.
        :rtype: Purchase
        """
        return await Purchase.find_one({"arapack_lot": purchase_arapack_lot})

    @staticmethod
    async def get_filtered_purchases(
        query: str, offset: int, limit: int
    ) -> List[Purchase]:
        # Filtro de búsqueda
        filters = {
            "$or": [
                {"symbol": {"$regex": query, "$options": "i"}},
                {"order_number": {"$regex": query, "$options": "i"}},
                {"client": {"$regex": query, "$options": "i"}},
                {"arapack_lot": {"$regex": query, "$options": "i"}},
            ]
        }

        collection = Purchase.get_motor_collection()
        cursor = (
            collection.find(filters).sort("receipt_date", -1).skip(offset).limit(limit)
        )
        # purchases = await Purchase.find(filters).sort("receipt_date", 1).skip(offset).limit(limit).to_list()
        purchases = await cursor.to_list(length=None)

        return purchases

    @staticmethod
    async def get_total_count(query: str) -> int:
        """
        Get the total count of filtered purchases.

        :param query: The search query to filter purchases.
        :type query: str
        :return: The total count of filtered purchases.
        :rtype: int
        """
        filters = {
            "$or": [
                {"symbol": {"$regex": query, "$options": "i"}},
                {"order_number": {"$regex": query, "$options": "i"}},
                {"client": {"$regex": query, "$options": "i"}},
                {"arapack_lot": {"$regex": query, "$options": "i"}},
            ]
        }

        total_count = await Purchase.find(filters).count()
        return total_count

    @staticmethod
    async def create(purchase: Purchase):
        """
        Create a new purchase in the database.
        :param purchase: The Purchase document to create.
        :type purchase: Purchase
        :return: The created Purchase document.
        :rtype: Purchase
        """
        return await purchase.create()

    @staticmethod
    async def get_null_delivery_dates():
        """
        Get purchases with null delivery dates.
        :return: List of Purchase documents with null delivery dates.
        :rtype: List[Purchase]
        """
        return await Purchase.find({"estimated_delivery_date": None}).to_list()
