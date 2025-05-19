"""
This module contains the PurchaseService class, which is responsible for interacting with the purchase repository.
"""

import json
from datetime import datetime
from typing import List, Dict, Any
from fastapi import HTTPException, BackgroundTasks
from pymongo.errors import DuplicateKeyError
from starlette.datastructures import UploadFile
from models.purchase import Purchase, DeliveryDate
from models.box import Box
from models.sheet import Sheet
from repositories.purchase_repository import PurchaseRepository
from repositories.box_repository import BoxRepository
from repositories.sheet_repository import SheetRepository
from repositories.program_planning_repository import ProgramPlanningRepository
from services.ia_service import IAService
from services.updaters.register_updater import RegisterUpdater
from services.updaters.quantity_updater import QuantityUpdater
from services.updaters.delivery_date_updater import DeliveryDateUpdater


class PurchaseService:
    """Class for Purchase service."""

    # Initialize the IAService
    _ia_service = IAService()

    # Initialize the updaters
    _register_updater = RegisterUpdater(_ia_service)
    _quantity_updater = QuantityUpdater(_ia_service)
    _delivery_date_updater = DeliveryDateUpdater(_ia_service)

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

        purchase.missing_quantity = purchase.quantity

        try:
            return await PurchaseRepository.create(purchase)
        except DuplicateKeyError:
            raise HTTPException(
                status_code=400,
                detail="A purchase with the same 'arapack_lot' already exists.",
            )

    @staticmethod
    async def create_purchase_with_ai(
        purchase: Purchase, background_tasks: BackgroundTasks
    ):
        """
        Create a new purchase and trigger AI processing in the background.

        Args:
            purchase: The purchase to create.
            background_tasks: FastAPI background tasks for asynchronous processing.

        Returns:
            Purchase: The created purchase.
        """
        # First, create the purchase normally
        created_purchase = await PurchaseService.create_purchase(purchase)

        # Then, trigger AI processing in the background
        background_tasks.add_task(
            PurchaseService._process_new_purchase_with_ai, created_purchase
        )

        return created_purchase

    @staticmethod
    async def _process_new_purchase_with_ai(purchase: Purchase):
        """
        Process a new purchase with AI in the background.

        Args:
            purchase: The purchase to process.
        """
        # Get the box associated with the purchase
        box = await BoxRepository.get_by_symbol(purchase.symbol)
        if not box:
            return

        # Get available sheets
        sheets = await SheetRepository.get_all()

        # Get the program planning for the purchase's week
        program_planning = await ProgramPlanningRepository.get_by_week(
            purchase.week_of_year
        )

        # Prepare input data for the updater
        input_data = {
            "purchase": purchase.dict(),
            "box": box.dict(),
            "sheets": [sheet.dict() for sheet in sheets],
            "program_planning": program_planning.dict() if program_planning else {},
        }

        # Call the register updater
        await PurchaseService._register_updater.update(input_data)

    @staticmethod
    async def update_purchase_quantity(
        arapack_lot: str, new_quantity: int, background_tasks: BackgroundTasks
    ) -> Purchase:
        """
        Update the quantity of a purchase and trigger AI processing in the background.

        Args:
            arapack_lot: The arapack lot of the purchase to update.
            new_quantity: The new quantity.
            background_tasks: FastAPI background tasks for asynchronous processing.

        Returns:
            Purchase: The updated purchase.
        """
        # Get the purchase
        purchase = await PurchaseRepository.get_by_arapack_lot(arapack_lot)
        if not purchase:
            raise HTTPException(status_code=404, detail="Purchase not found")

        # Update the quantity
        purchase.quantity = new_quantity
        await purchase.save()

        # Trigger AI processing in the background
        background_tasks.add_task(
            PurchaseService._process_quantity_update_with_ai, purchase
        )

        return purchase

    @staticmethod
    async def _process_quantity_update_with_ai(purchase: Purchase):
        """
        Process a quantity update with AI in the background.

        Args:
            purchase: The purchase with updated quantity.
        """
        # Get the program planning for the purchase's week
        program_planning = await ProgramPlanningRepository.get_by_week(
            purchase.week_of_year
        )
        if not program_planning:
            return

        # Prepare input data for the updater
        input_data = {
            "purchase": purchase.dict(),
            "program_planning": program_planning.dict(),
        }

        # Call the quantity updater
        await PurchaseService._quantity_updater.update(input_data)

    @staticmethod
    async def update_delivery_date(
        arapack_lot: str, new_delivery_date: datetime, new_quantity: int, background_tasks: BackgroundTasks
    ) -> Purchase:
        """
        Update the delivery date of a purchase and trigger AI processing in the background.

        Args:
            arapack_lot: The arapack lot of the purchase to update.
            new_delivery_date: The new delivery date.
            new_quantity: The new quantity.
            background_tasks: FastAPI background tasks for asynchronous processing.

        Returns:
            Purchase: The updated purchase.
        """
        # Get the purchase
        purchase = await PurchaseRepository.get_by_arapack_lot(arapack_lot)
        if not purchase:
            raise HTTPException(status_code=404, detail="Purchase not found")

        # Store the original week
        original_week = purchase.week_of_year

        # Update the delivery date if provided
        if new_delivery_date:
            purchase.estimated_delivery_date = new_delivery_date

        # Update the quantity if provided
        if new_quantity:
            purchase.quantity = new_quantity

        # Calculate the new week of the year
        purchase.week_of_year = new_delivery_date.isocalendar()[1]

        # Save the updated purchase
        await purchase.save()

        # Trigger AI processing in the background
        background_tasks.add_task(
            PurchaseService._process_delivery_date_update_with_ai,
            purchase,
            original_week,
        )

        return purchase

    @staticmethod
    async def _process_delivery_date_update_with_ai(
        purchase: Purchase, original_week: int
    ):
        """
        Process a delivery date update with AI in the background.

        Args:
            purchase: The purchase with updated delivery date.
            original_week: The original week of the year.
        """
        # Get the original program planning
        original_program = await ProgramPlanningRepository.get_by_week(original_week)
        if not original_program:
            print("purchase service: Original program planning not found - Breaking")
            return

        # Get the new program planning if the week changed
        new_program = None
        if purchase.week_of_year != original_week:
            print("Original week of the year:", original_week)
            print("New week of the year:", purchase.week_of_year)
            new_program = await ProgramPlanningRepository.get_by_week(
                purchase.week_of_year
            )

        # Prepare input data for the updater
        input_data = {
            "purchase": purchase.model_dump(),
            "programs": {
                "original_program_planning": original_program.model_dump(),
                "new_program_planning": new_program.model_dump() if new_program else {},
            },
        }

        # Call the delivery date updater
        await PurchaseService._delivery_date_updater.update(input_data)

    @staticmethod
    async def get_null_delivery_dates():
        """Get purchases with null delivery dates."""
        return await PurchaseRepository.get_null_delivery_dates()

    @staticmethod
    async def update_delivery_info(arapack_lot: str, new_delivery_date: datetime, new_quantity: int):
        """
        Update the delivery information of a purchase. if not contains new_delivery_date or new_quantity, update only the one that is not None.

        Args:
            arapack_lot (str): The arapack lot of the purchase to update.
            new_delivery_date (datetime): The new delivery date.
            new_quantity (int): The new quantity.

        Returns:
            Purchase: The updated purchase.
        """

        # Get the purchase
        purchase = await PurchaseRepository.get_by_arapack_lot(arapack_lot)
        if not purchase:
            raise HTTPException(status_code=404, detail="Purchase not found")

        # Update the delivery date if provided
        if new_delivery_date:
            purchase.estimated_delivery_date = new_delivery_date

        # Update the quantity if provided
        if new_quantity:
            # Update the missing quantity as well
            purchase.missing_quantity = (
                purchase.missing_quantity + (new_quantity - purchase.quantity)
            )
            purchase.quantity = new_quantity

            # Calculate the new subtotal and total invoice
            purchase.subtotal = purchase.unit_cost * new_quantity
            purchase.total_invoice = purchase.subtotal * 1.16  # Assuming a 16% tax rate

        # Save the updated purchase
        await purchase.save()

        return purchase

    @staticmethod
    async def create_shipping(arapack_lot: str, initial_shipping_date: datetime, quantity: int, comment: str, finish_shipping_date: datetime = None):
        """
        Create a shipping for a purchase.

        Args:
            arapack_lot (str): The arapack lot of the purchase to update.
            initial_shipping_date (datetime): The initial shipping date.
            quantity (int): The quantity to ship.
            comment (str): A comment for the shipping.
            finish_shipping_date (datetime, optional): The finish shipping date. Defaults to None.

        Returns:
            Purchase: The updated purchase.
        """
        # Get the purchase
        purchase = await PurchaseRepository.get_by_arapack_lot(arapack_lot)
        if not purchase:
            raise HTTPException(status_code=404, detail="Purchase not found")

        # Create the new delivery date
        new_delivery_date: DeliveryDate = DeliveryDate(
            initial_shipping_date=initial_shipping_date,
            quantity=quantity,
            comment=comment,
            finish_shipping_date=finish_shipping_date,
        )

        purchase.missing_quantity = purchase.missing_quantity - quantity

        # Add the new delivery date to the purchase
        if not purchase.delivery_dates:
            purchase.delivery_dates = []
        purchase.delivery_dates.append(new_delivery_date)

        # Save the updated purchase
        await purchase.save()

        return purchase

    @staticmethod
    async def complete_shipping(arapack_lot: str, index: int):
        """
        Complete a shipping for a purchase.

        Args:
            arapack_lot (str): The arapack lot of the purchase to update.
            index (int): The index of the delivery date to complete.

        Returns:
            Purchase: The updated purchase.
        """
        # Get the purchase
        purchase = await PurchaseRepository.get_by_arapack_lot(arapack_lot)
        if not purchase:
            raise HTTPException(status_code=404, detail="Purchase not found")

        # Check if the index is valid
        if index < 0 or index >= len(purchase.delivery_dates):
            raise HTTPException(status_code=400, detail="Invalid delivery date index")

        # Complete the shipping
        purchase.delivery_dates[index].finish_shipping_date = datetime.now()

        # Save the updated purchase
        await purchase.save()
        return purchase

    @staticmethod
    async def get_monthly_invoice():
        """
        Get the monthly invoice for purchases.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing the monthly invoice data.
        """
        # Get all purchases
        purchases = await PurchaseRepository.get_all()

        # Get the current month
        current_month = datetime.now().month

        # Initialize the invoice data
        total_monthly_invoice = 0

        # Iterate through each purchase and extract relevant data
        for purchase in purchases:
            if purchase.total_invoice and purchase.receipt_date.month == current_month:
                total_monthly_invoice += purchase.total_invoice

        # Return the monthly invoice data
        return total_monthly_invoice

    @staticmethod
    async def get_backorders():
        """
        Get the backorders for purchases.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing the backorder data.
        """
        # Get all purchases
        purchases = await PurchaseRepository.get_all()

        # Initialize the backorder data
        backorders = []

        # Iterate through each purchase and extract relevant data
        for purchase in purchases:
            if purchase.estimated_delivery_date < datetime.now():
                backorder_data = {
                    "arapack_lot": purchase.arapack_lot,
                    "estimated_delivery_date": purchase.estimated_delivery_date,
                    "missing_quantity": purchase.missing_quantity,
                    "delivery_delay_days": (datetime.now() - purchase.estimated_delivery_date).days,
                }
                backorders.append(backorder_data)

        # Return the backorder data
        return backorders

