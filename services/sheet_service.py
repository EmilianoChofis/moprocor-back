"""Sheet service module for interacting with the sheets' repository."""
from typing import List
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
    async def get_sheet_by_id(sheet_id: str) -> Sheet:
        """Get a sheet by its ID."""
        sheet = await SheetRepository.get_by_id(sheet_id)
        if not sheet:
            raise HTTPException(status_code=404, detail="Sheet not found")
        return await SheetRepository.get_by_id(sheet_id)

    @staticmethod
    async def create_sheet(sheet: Sheet) -> Sheet:
        """Create a sheet."""
        existing_sheet = await SheetRepository.get_by_id(str(sheet.id))
        if existing_sheet:
            raise HTTPException(
                status_code=400, detail=f"Sheet with ID {sheet.id} already exists"
            )
        return await SheetRepository.create(sheet)
