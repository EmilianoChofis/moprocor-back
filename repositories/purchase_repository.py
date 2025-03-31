"""
Repository for Purchase documents in the database.
"""
from typing import List

from models.box import Box
from models.purchase import Purchase
from models.sheet import Sheet


class PurchaseRepository:
    """ Purchase repository for MongoDB using Beanie ORM functions. """

    @staticmethod
    async def get_all():
        """
        Get all purchases from the database.
        :return: List of all Purchase documents.
        :rtype: List[Purchase]
        """
        return await Purchase.all().to_list()

    @staticmethod
    async def create_bundle(purchases):
        """
        Create a new list of purchases in the database.
        :param purchases: The Purchase documents to create.
        :type purchases: Purchases
        :return: The created Purchase document.
        :rtype: Purchase
        """
        return await Purchase.insert_many(purchases)

    @staticmethod
    async def get_filtered_boxes(purchase_bundle: List[str]):
        """
        Get all boxes from the database that match the symbols in purchase_bundle.
        :param purchase_bundle: List of symbols to filter by.
        :type purchase_bundle: List[str]
        :return: List of Box documents that match the symbols.
        :rtype: List[Box]
        """
        # Filter boxes by symbol in purchase_bundle
        collection = Box.get_motor_collection()
        cursor = collection.find({"symbol": {"$in": purchase_bundle}, "ect": 1, "liner": 1, "flute": 1, "weight": 1, "length": 1, "width": 1, "treatment": 1})
        result = await cursor.to_list()
        boxes = await Box.find({"symbol": {"$in": purchase_bundle}}).to_list()
        return boxes

    @staticmethod
    async def get_filtered_sheets(filtered_boxes: List[Box]):
        """
        Get sheets that are compatible with the filtered boxes in terms of ECT
        and whose boxes include the symbols of the filtered boxes.
        :param filtered_boxes: List of filtered Box documents.
        :type filtered_boxes: List[Box]
        :return: List of compatible Sheet documents.
        :rtype: List[Sheet]
        """
        # Extract symbols and ECT from the filtered boxes
        symbols = [box.symbol for box in filtered_boxes]
        ects = [box.ect for box in filtered_boxes]

        # Filter sheets by ECT and symbols
        filter_sheets = {
            "$or": [
                {"ect": {"$in": ects}},
                {"boxes": {"$in": symbols}}
            ]
        }
        collection = Sheet.get_motor_collection()
        cursor = collection.find(filter_sheets,  {"_id": 0, "description": 0, "p1":0, "p2":0, "p3":0})
        compatible_sheets = await cursor.to_list()
        compatible_sheets = await Sheet.find(filter_sheets).to_list()
        return compatible_sheets


