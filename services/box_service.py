"""Box service module for interacting with the box repository."""
import os
import dotenv
# Import the required libraries
from typing import List, Optional, Dict
from fastapi import HTTPException, UploadFile, File
from models.box import Box
from repositories.box_repository import BoxRepository

dotenv.load_dotenv()

FILES_PATH = os.getenv("FILES_PATH")


class BoxService:
    """Class for Box service."""

    @staticmethod
    async def get_all_boxes() -> List[Box]:
        """Get all boxes from the database."""
        return await BoxRepository.get_all()

    @staticmethod
    async def get_box_by_symbol(symbol: str) -> Optional[Box]:
        """Get a box by its symbol"""
        box = await BoxRepository.get_by_symbol(symbol)
        if not box:
            raise HTTPException(status_code=404, detail="Box not found")
        return await BoxRepository.get_by_symbol(symbol)

    @staticmethod
    async def create_box(box: Box, pdf_file: UploadFile = File(...)) -> Box:
        """Create a box."""
        # Validate box data if needed
        existing_box = await BoxRepository.get_by_symbol(box.symbol)
        if existing_box:
            raise HTTPException(
                status_code=400, detail=f"Box with symbol {box.symbol} already exists"
            )
        # Save the PDF file to the server
        pdf_path = f"../{FILES_PATH}/{box.symbol}.pdf"
        with open(pdf_path, "wb") as pdf_file_obj:
            pdf_file_obj.write(pdf_file.file.read())
            box.pdf_link = pdf_path

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

    @staticmethod
    async def get_filtered_boxes(query: str, page: int, items_per_page: int) -> Dict[str, List[Box]]:
        """Obtiene las cajas con paginación"""

        # Calcula el offset
        offset = (page - 1) * items_per_page

        # Obtiene las cajas paginadas y el total
        return await BoxRepository.get_filtered_boxes(query, offset, items_per_page)

    @staticmethod
    async def get_pages(query: str, items_per_page: int) -> int:
        """Obtiene el total de páginas"""
        total_items = await BoxRepository.get_total_count(query)
        total_pages = (total_items + items_per_page - 1) // items_per_page  # Redondeo hacia arriba
        return total_pages

