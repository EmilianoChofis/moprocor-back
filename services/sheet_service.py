"""Sheet service module for interacting with the sheets' repository."""

from typing import List, Dict, Optional

from beanie import PydanticObjectId
from fastapi import HTTPException
from repositories.sheet_repository import SheetRepository
from models.sheet import Sheet


class SheetService:
    """Class for Sheet service."""

    @staticmethod
    async def get_all_sheets() -> List[Sheet]:
        """Get all sheets from the database."""
        return await SheetRepository.get_all()

    @staticmethod
    async def get_sheet_by_id(sheet_id: PydanticObjectId) -> Sheet:
        """Get a sheet by its ID."""
        sheet = await SheetRepository.get_by_id(sheet_id)
        if not sheet:
            raise HTTPException(status_code=404, detail="Sheet not found")
        return sheet

    @staticmethod
    async def create_sheet(sheet: Sheet) -> Sheet:
        """Create a sheet."""
        return await SheetRepository.create(sheet)

    @staticmethod
    async def get_filtered_sheets(
        query: str, page: int, items_per_page: int
    ) -> Dict[str, list[Sheet]]:
        """Get all sheets with pagination and total."""
        offset = (page - 1) * items_per_page

        return await SheetRepository.get_filtered_sheets(query, offset, items_per_page)

    @staticmethod
    async def get_pages(query: str, items_per_page: int) -> int:
        """Get the total number of sheets."""
        total_items = await SheetRepository.get_total_count(query)
        total_pages = (total_items + items_per_page - 1) // items_per_page
        return total_pages

    @staticmethod
    async def update_sheet(
        sheet_id: PydanticObjectId, update_data: dict
    ) -> Optional[Sheet]:
        """Update a sheet."""
        sheet = await SheetRepository.update_sheet(sheet_id, update_data)
        if not sheet:
            raise HTTPException(status_code=404, detail="Sheet not found")
        return sheet

    @staticmethod
    async def change_status(sheet_id: PydanticObjectId) -> Optional[Sheet]:
        """Change the status of a sheet."""
        try:
            sheet = await SheetRepository.get_by_id(sheet_id)
            if not sheet:
                raise HTTPException(status_code=404, detail="Sheet not found")

            sheet.status = not sheet.status
            await sheet.save()

            return sheet
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
