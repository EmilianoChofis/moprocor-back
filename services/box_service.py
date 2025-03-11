"""Box service for MongoDB using Beanie ORM functions."""

# Import the required libraries
from typing import List, Optional
from fastapi import HTTPException
from models.box import Box
from repositories.box_repository import BoxRepository


class BoxService:
    """Class for Box service."""

    @staticmethod
    async def get_all_boxes() -> List[Box]:
        """Get all boxes from the database."""
        return await BoxRepository.get_all()

    @staticmethod
    async def get_box_by_symbol(symbol: str) -> Optional[Box]:
        """Get a box by its symbol"""
        return await BoxRepository.get_by_symbol(symbol)

    @staticmethod
    async def create_box(box: Box) -> Box:
        """Create a box."""
        # Validate box data if needed
        existing_box = await BoxRepository.get_by_symbol(box.symbol)
        if existing_box:
            raise HTTPException(
                status_code=400, detail=f"Box with symbol {box.symbol} already exists"
            )

        return await BoxRepository.create(box)

    @staticmethod
    async def update_box(symbol: str, box_data: dict) -> Optional[Box]:
        """Update a box."""
        # Implementation for updating a box
        pass

    @staticmethod
    async def delete_box(symbol: str) -> bool:
        """Delete a box."""
        # Implementation for deleting a box
        pass
