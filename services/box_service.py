"""Box service module for interacting with the box repository."""

import os
import shutil

import dotenv

# Import the required libraries
from typing import List, Optional, Dict, Any, Coroutine, Mapping

from beanie import PydanticObjectId
from fastapi import HTTPException, UploadFile
from models.box import Box
from repositories.box_repository import BoxRepository

dotenv.load_dotenv()

# Define the path where files will be stored
FILES_PATH = os.getenv("FILES_PATH", "../files")

# Ensure the directory for storing files exists
if not os.path.exists(FILES_PATH):
    os.makedirs(FILES_PATH, exist_ok=True)


class BoxService:
    """Class for Box service. Provides methods to interact with the box repository."""

    @staticmethod
    async def get_all_boxes() -> List[Box]:
        """
        Retrieve all boxes from the database.

        Returns:
            List[Box]: A list of all boxes.
        """
        return await BoxRepository.get_all()

    @staticmethod
    async def get_box_by_symbol(symbol: str) -> Optional[Box]:
        """
        Retrieve a box by its symbol.

        Args:
            symbol (str): The symbol of the box to retrieve.

        Returns:
            Optional[Box]: The box with the given symbol, or None if not found.

        Raises:
            HTTPException: If the box is not found.
        """
        box = await BoxRepository.get_by_symbol(symbol)
        if not box:
            raise HTTPException(status_code=404, detail="Caja no encontrada")
        return await BoxRepository.get_by_symbol(symbol)

    @staticmethod
    async def create_box(box: Box, pdf_file: UploadFile) -> Box:
        """
        Create a new box and save an associated PDF file.

        Args:
            box (Box): The box data to create.
            pdf_file (UploadFile): The PDF file to associate with the box.

        Returns:
            Box: The created box.

        Raises:
            HTTPException: If the box already exists, the file is not a PDF, or the file cannot be saved.
        """
        # Validate box data
        existing_box = await BoxRepository.get_by_symbol(box.symbol)
        if existing_box:
            raise HTTPException(
                status_code=400,
                detail=f"Ya existe una caja con el simbolo {box.symbol}",
            )

        # Validate file type
        if not pdf_file.content_type == "application/pdf":
            raise HTTPException(status_code=400, detail="El archivo debe ser un PDF")

        # If pdf_link is empty, use the original filename or create one from the symbol
        if not box.pdf_link:
            box.pdf_link = f"{box.symbol.replace(' ', '_')}.pdf"

        # Ensure the directory exists
        os.makedirs(FILES_PATH, exist_ok=True)

        # Save the PDF file
        file_path = os.path.join(FILES_PATH, box.pdf_link)

        # Create the file with proper exception handling
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(pdf_file.file, buffer)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error al guardar achivo PDF: {str(e)}"
            )

        return await BoxRepository.create(box)

    @staticmethod
    async def delete_box(symbol: str) -> bool:
        """
        Delete a box by its symbol.

        Args:
            symbol (str): The symbol of the box to delete.

        Returns:
            bool: True if the box was successfully deleted, False otherwise.
        """
        # Implementation for deleting a box
        pass

    @staticmethod
    async def get_filtered_boxes(
        query: str, page: int, items_per_page: int
    ) -> List[Mapping[str, Any] | Any]:
        """
        Retrieve filtered boxes with pagination.

        Args:
            query (str): The search query to filter boxes.
            page (int): The page number to retrieve.
            items_per_page (int): The number of items per page.

        Returns:
            Dict[str, List[Box]]: A dictionary containing the filtered boxes.
        """
        # Calculate the offset
        offset = (page - 1) * items_per_page

        # Retrieve paginated boxes and the total count
        return await BoxRepository.get_filtered_boxes(query, offset, items_per_page)

    @staticmethod
    async def get_pages(query: str, items_per_page: int) -> int:
        """
        Calculate the total number of pages for a given query.

        Args:
            query (str): The search query to filter boxes.
            items_per_page (int): The number of items per page.

        Returns:
            int: The total number of pages.
        """
        total_items = await BoxRepository.get_total_count(query)
        total_pages = (total_items + items_per_page - 1) // items_per_page  # Round up
        return total_pages

    @staticmethod
    async def get_all_symbols() -> list[str]:
        """
        Retrieve all box symbols from the database.

        Returns:
            list[str]: A list of all box symbols.
        """
        return await BoxRepository.get_all_symbols()

    @staticmethod
    async def update_box(
        box_id: PydanticObjectId,
        symbol: str,
        ect: int,
        liner: str,
        width: float,
        length: float,
        flute: str,
        treatment: int,
        client: str,
        crease1: float,
        crease2: float,
        crease3: float,
        gcmi_1: str,
        gcmi_2: str,
        gcmi_3: str,
        gcmi_4: str,
        weight: float,
        box_status: str,
        box_type: str,
        pdf_file: Optional[UploadFile],
    ) -> Optional[Box]:
        """
        Update a box and optionally replace its associated PDF file.

        Args:
            box_id (PydanticObjectId): The ID of the box to update.
            symbol (str): The updated symbol of the box.
            ect (int): The updated ECT value.
            liner (str): The updated liner value.
            width (float): The updated width of the box.
            length (float): The updated length of the box.
            flute (str): The updated flute type.
            treatment (int): The updated treatment value.
            client (str): The updated client name.
            crease1 (float): The updated first crease value.
            crease2 (float): The updated second crease value.
            crease3 (float): The updated third crease value.
            gcmi_1 (str): The updated first GCMI ink value.
            gcmi_2 (str): The updated second GCMI ink value.
            gcmi_3 (str): The updated third GCMI ink value.
            gcmi_4 (str): The updated fourth GCMI ink value.
            weight (float): The updated weight of the box.
            box_status (str): The updated status of the box.
            box_type (str): The updated type of the box.
            pdf_file (Optional[UploadFile]): The new PDF file to replace the existing one.

        Returns:
            Optional[Box]: The updated box, or None if not found.

        Raises:
            HTTPException: If the box is not found, the file is not a PDF, or the file cannot be saved.
        """
        # Retrieve the existing box
        box = await BoxRepository.get_by_id(id=box_id)
        if not box:
            raise HTTPException(status_code=404, detail="Caja no encontrada")

        # Prepare the update data
        update_data = {
            "symbol": symbol,
            "ect": ect,
            "liner": liner,
            "width": width,
            "length": length,
            "flute": flute,
            "treatment": treatment,
            "client": client,
            "creases": {"r1": crease1, "r2": crease2, "r3": crease3},
            "inks": {
                "gcmi_1": gcmi_1,
                "gcmi_2": gcmi_2,
                "gcmi_3": gcmi_3,
                "gcmi_4": gcmi_4,
            },
            "weight": weight,
            "status": box_status,
            "type": box_type,
        }

        # Handle PDF file replacement
        if pdf_file:
            if not pdf_file.content_type == "application/pdf":
                raise HTTPException(
                    status_code=400, detail="El archivo debe ser un PDF"
                )

            # Path for the new file
            new_file_path = os.path.join(FILES_PATH, pdf_file.filename)

            # Remove the old file if it exists
            old_file_path = os.path.join(FILES_PATH, box.pdf_link)
            if os.path.exists(old_file_path):
                os.remove(old_file_path)

            # Save the new file
            try:
                with open(new_file_path, "wb") as buffer:
                    shutil.copyfileobj(pdf_file.file, buffer)
                update_data["pdf_link"] = pdf_file.filename
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Error al guardar el archivo PDF: {str(e)}"
                )

        # Update the box in the database
        updated_box = await BoxRepository.update_box(box_id, update_data)
        if not updated_box:
            raise HTTPException(status_code=404, detail="Caja no encontrada")
        return updated_box

    @staticmethod
    async def change_status(box_id: PydanticObjectId, status: str) -> Optional[Box]:
        """
        Change the status of a box.

        Args:
            box_id (PydanticObjectId): The ID of the box to update.
            status (str): The new status to set.

        Returns:
            Optional[Box]: The updated box, or None if not found.

        Raises:
            HTTPException: If the box is not found or the status is invalid.
        """
        try:
            box = await BoxRepository.change_status(box_id, status)
            if not box:
                raise HTTPException(status_code=404, detail="Caja no encontrada")
            return box
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
