"""
This module contains the PurchaseService class, which is responsible for interacting with the purchase repository.
"""

import json
from datetime import datetime
from typing import List
from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError
from starlette.datastructures import UploadFile
from models.purchase import Purchase
from repositories.purchase_repository import PurchaseRepository
from utils.extract_purchases import read_excel_to_json


class PurchaseService:
    """Class for Purchase service."""

    @staticmethod
    async def get_all_purchases():
        """Get all purchases from the database."""
        return await PurchaseRepository.get_all()

    @staticmethod
    async def get_purchase_by_arapack_lot(purchase_arapack_lot: str):
        """Get a purchase by its ID."""
        purchase = await PurchaseRepository.get_by_arapack_lot(purchase_arapack_lot)
        if not purchase:
            raise HTTPException(status_code=404, detail="Purchase not found")
        return purchase

    @staticmethod
    async def load_purchases(excel_file: UploadFile, sheet_name: str):
        """Extract and load purchases from an Excel file."""
        if not excel_file.filename.endswith(".xlsx"):
            raise HTTPException(
                status_code=400,
                detail="Formato de archivo inválido. Solo se permiten archivos .xlsx.",
            )
        if not sheet_name:
            raise HTTPException(
                status_code=400, detail="Se requiere el nombre de la hoja."
            )

        # Leer el archivo Excel y convertirlo a bytes
        excel_file.file.seek(0)
        excel_file_bytes = excel_file.file.read()

        # Utilizar la función de utilidad para extraer los datos
        data = read_excel_to_json(excel_file_bytes, sheet_name)

        return data

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
        # Validate uniqueness of 'arapack_lot'
        for purchase in purchases:
            existing_purchase = await Purchase.find_one(
                {"arapack_lot": purchase.arapack_lot}
            )
            if existing_purchase:
                raise HTTPException(
                    status_code=400,
                    detail=f"A purchase with the 'arapack_lot' {purchase.arapack_lot} already exists.",
                )

        # First insert the documents
        result = await PurchaseRepository.create_bundle(purchases)
        inserted_count = 0

        json_purchases = [
            {
                "order_number": purchase.order_number,
                "symbol": purchase.symbol,
                "quantity": purchase.quantity,
                "flute": purchase.flute,
                "ect": purchase.ect,
                "liner": purchase.liner,
                "type": purchase.type,
                "estimated_delivery_date": purchase.estimated_delivery_date,
                "arapack_lot": purchase.arapack_lot,
            }
            for purchase in purchases
        ]
        json_boxes = ""
        json_sheets = ""

        if result.acknowledged:
            inserted_count = len(result.inserted_ids)

            # Extract symbols from purchases for filtering boxes
            purchase_symbols = [purchase.symbol for purchase in purchases]

            # Get filtered boxes based on purchase symbols
            filtered_boxes = await PurchaseRepository.get_filtered_boxes(
                purchase_symbols
            )

            # Get compatible sheets based on filtered boxes
            filtered_sheets = await PurchaseRepository.get_filtered_sheets(
                filtered_boxes
            )

            # Define a custom JSON encoder to handle datetime objects
            class DateTimeEncoder(json.JSONEncoder):
                def default(self, obj):
                    from bson import ObjectId

                    if isinstance(obj, datetime):
                        return obj.isoformat()
                    # Handle MongoDB ObjectId and PydanticObjectId
                    if (
                        isinstance(obj, ObjectId)
                        or str(type(obj)) == "<class 'bson.objectid.ObjectId'>"
                    ):
                        return str(obj)
                    try:
                        # This handles other non-serializable types
                        return super().default(obj)
                    except TypeError:
                        return str(obj)  # Fall back to string representation

            # Convert all three data sets to JSON strings
            json_purchases = json.dumps(json_purchases, cls=DateTimeEncoder)
            json_boxes = json.dumps(
                [b.model_dump() for b in filtered_boxes], cls=DateTimeEncoder
            )
            json_sheets = json.dumps(
                [s.model_dump() for s in filtered_sheets], cls=DateTimeEncoder
            )

        print(json_purchases, json_boxes, json_sheets)
        return inserted_count, json_purchases, json_boxes, json_sheets

    @staticmethod
    async def get_filtered_purchases(
        query: str, page: int, items_per_page: int
    ) -> List[Purchase]:
        """Obtiene las compras con paginación"""

        # Calcula el offset
        offset = (page - 1) * items_per_page

        # Obtiene las compras paginadas y el total
        return await PurchaseRepository.get_filtered_purchases(
            query, offset, items_per_page
        )

    @staticmethod
    async def get_pages(query: str, items_per_page: int) -> int:
        """Obtiene el total de páginas"""
        total_items = await PurchaseRepository.get_total_count(query)
        total_pages = (total_items + items_per_page - 1) // items_per_page
        return total_pages

    @staticmethod
    async def create_purchase(purchase: Purchase):
        """Create a new purchase in the database."""
        # Validate uniqueness of 'arapack_lot'
        existing_purchase = await Purchase.find_one(
            {"arapack_lot": purchase.arapack_lot}
        )
        if existing_purchase:
            raise HTTPException(
                status_code=400,
                detail=f"A purchase with the 'arapack_lot' {purchase.arapack_lot} already exists.",
            )

        # Calculate the week of the year using delivery date
        if purchase.estimated_delivery_date:
            purchase.week_of_year = purchase.estimated_delivery_date.isocalendar()[1]

        try:
            return await PurchaseRepository.create(purchase)
        except DuplicateKeyError:
            raise HTTPException(
                status_code=400,
                detail="A purchase with the same 'arapack_lot' already exists.",
            )

    @staticmethod
    async def get_null_delivery_dates():
        """Get purchases with null delivery dates."""
        return await PurchaseRepository.get_null_delivery_dates()

