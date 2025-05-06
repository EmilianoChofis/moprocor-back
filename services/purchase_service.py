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

