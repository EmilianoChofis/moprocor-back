"""
This module contains the PurchaseService class, which is responsible for interacting with the purchase repository.
"""
import json
from datetime import datetime

from repositories.purchase_repository import PurchaseRepository


class PurchaseService:
    """ Class for Purchase service. """

    @staticmethod
    async def get_all_purchases():
        """ Get all purchases from the database. """
        return await PurchaseRepository.get_all()

    @staticmethod
    async def create_bundle(purchases):
        """
        Create a new list of purchases in the database and execute the full pipeline.

        Pipeline steps:
        1. Save purchases to MongoDB
        2. Get filtered boxes based on purchase symbols
        3. Get filtered sheets compatible with those boxes
        4. Transform all three data sets to JSON strings

        Returns:
            Tuple containing:
            - Number of inserted documents
            - JSON string of purchases
            - JSON string of filtered boxes
            - JSON string of filtered sheets
        """
        # First insert the documents
        result = await PurchaseRepository.create_bundle(purchases)
        inserted_count = 0

        json_purchases = ""
        json_boxes = ""
        json_sheets = ""

        if result.acknowledged:
            inserted_count = len(result.inserted_ids)

            # Extract symbols from purchases for filtering boxes
            purchase_symbols = [purchase.symbol for purchase in purchases]

            # Get filtered boxes based on purchase symbols
            filtered_boxes = await PurchaseRepository.get_filtered_boxes(purchase_symbols)

            # Get compatible sheets based on filtered boxes
            filtered_sheets = await PurchaseRepository.get_filtered_sheets(filtered_boxes)

            # Define a custom JSON encoder to handle datetime objects
            class DateTimeEncoder(json.JSONEncoder):
                def default(self, obj):
                    from bson import ObjectId

                    if isinstance(obj, datetime):
                        return obj.isoformat()
                    # Handle MongoDB ObjectId and PydanticObjectId
                    if isinstance(obj, ObjectId) or str(type(obj)) == "<class 'bson.objectid.ObjectId'>":
                        return str(obj)
                    try:
                        # This handles other non-serializable types
                        return super().default(obj)
                    except TypeError:
                        return str(obj)  # Fall back to string representation

            purchase_data = [
                {
                    "order_number": purchase.order_number,
                    "symbol": purchase.symbol,
                    "quantity": purchase.quantity,
                    "price": purchase.price,
                    "date": purchase.date,
                    "description": purchase.description,
                    "flute": purchase.flute,
                    "ect": purchase.ect,
                    "liner": purchase.liner,
                    "type": purchase.type,
                    "estimated_delivery_date": purchase.estimated_delivery_date,
                }
                for purchase in purchases

            ]


            # Convert all three data sets to JSON strings
            json_purchases = json.dumps([p.model_dump() for p in purchases], cls=DateTimeEncoder)
            json_boxes = json.dumps([b.model_dump() for b in filtered_boxes], cls=DateTimeEncoder)
            json_sheets = json.dumps([s.model_dump() for s in filtered_sheets],  cls=DateTimeEncoder)

        print(json_purchases,  json_boxes, json_sheets)
        return inserted_count, json_purchases, json_boxes, json_sheets
